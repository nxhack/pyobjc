/*
 * registry.m -- Storing and finding exception data.
 *
 * This file defines generic functionality to store exception data for
 * a class/method.
 */
#include "pyobjc.h"

BOOL PyObjC_UpdatingMetaData = NO;

PyObject*
PyObjC_NewRegistry(void)
{
    return PyDict_New();
}

int
PyObjC_AddToRegistry(
        PyObject* registry,
        PyObject* class_name, PyObject* selector,
        PyObject* value)
{
    int result;
    PyObject* sublist;
    PyObject* item = Py_BuildValue("(OO)", class_name, value);
    if (item == NULL) {
        return -1;
    }

#if PY_MAJOR_VERSION == 3
    sublist = PyDict_GetItemWithError(registry, selector);
    if (sublist == NULL && PyErr_Occurred()) {
        Py_DECREF(item);
        return -1;
    }
#else
    sublist = PyDict_GetItem(registry, selector);
#endif
    if (sublist == NULL) {
        sublist = PyList_New(0);
        result = PyDict_SetItem(registry, selector, sublist);
        Py_DECREF(sublist);
        if (result == -1) {
            Py_DECREF(item);
            return -1;
        }
    }

    if (!PyObjC_UpdatingMetaData) {
        PyObjC_MappingCount += 1;
    }
    result = PyList_Append(sublist, item);
    Py_DECREF(item);
    return result;
}

PyObject*
PyObjC_FindInRegistry(PyObject* registry, Class cls, SEL selector)
{
    Py_ssize_t i;
    Py_ssize_t len;
    PyObject* cur;
    Class found_class = nil;
    PyObject* found_value = NULL;
    PyObject* sublist;

    if (registry == NULL) {
        return NULL;
    }

    PyObject* k = PyBytes_FromString(sel_getName(selector));

#if PY_MAJOR_VERSION == 3
    sublist = PyDict_GetItemWithError(registry, k);
#else
    sublist = PyDict_GetItem(registry, k);
#endif
    Py_DECREF(k);
    if (sublist == NULL) return NULL;


    len = PyList_Size(sublist);
    for (i = 0; i < len; i++) {
        Class cur_class;

        cur = PyList_GET_ITEM(sublist, i);
        if (cur == NULL) {
            PyErr_Clear();
            continue;
        }

        if (!PyTuple_CheckExact(cur)) {
            PyErr_SetString(PyObjCExc_InternalError,
                "Exception registry element isn't a tuple");
            return NULL;
        }

        PyObject* nm = PyTuple_GET_ITEM(cur, 0);
        if (PyUnicode_Check(nm)) {
            PyObject* bytes = PyUnicode_AsEncodedString(nm, NULL, NULL);
            if (bytes == NULL) {
                return NULL;
            }
            cur_class = objc_lookUpClass(PyBytes_AsString(bytes));
            Py_DECREF(bytes);
#if PY_MAJOR_VERSION == 2
        } else if (PyString_Check(nm)) {
            cur_class = objc_lookUpClass(PyString_AsString(nm));
#else
        } else if (PyBytes_Check(nm)) {
            cur_class = objc_lookUpClass(PyBytes_AsString(nm));

#endif
        } else {
            PyErr_SetString(PyExc_TypeError, "Exception registry class name is not a string");
            return NULL;
        }

        if (cur_class == nil) {
            continue;
        }

        if (!class_isSubclassOf(cls, cur_class) && !class_isSubclassOf(cls, object_getClass(cur_class))) {
            continue;
        }

        if (found_class != NULL && found_class != cur_class) {
            if (class_isSubclassOf(found_class, cur_class)) {
                continue;
            }
        }

        found_class = cur_class;
        Py_INCREF(PyTuple_GET_ITEM(cur, 1));
        Py_XDECREF(found_value);
        found_value = PyTuple_GET_ITEM(cur, 1);
    }

    return found_value;
}

PyObject*
PyObjC_CopyRegistry(PyObject* registry, PyObjC_ItemTransform value_transform)
{
    PyObject* result = PyDict_New();
    PyObject* key;
    PyObject* sublist;
    Py_ssize_t pos = 0;
    if (result == NULL) {
        return NULL;
    }

    while (PyDict_Next(registry, &pos, &key, &sublist)) {
        Py_ssize_t i, len;
        PyObject* sl_new;
        len = PyList_Size(sublist);
        sl_new = PyList_New(len);
        if (sl_new == NULL) goto error;
        if (PyDict_SetItem(result, key, sl_new) == -1) {
            Py_DECREF(sl_new);
            goto error;
        }
        Py_DECREF(sl_new);

        for (i = 0; i < len; i++) {
            PyObject* item;
            PyObject* new_item;

            item = PyList_GET_ITEM(sublist, i);
            new_item = Py_BuildValue("(ON)",
                    PyTuple_GET_ITEM(item, 0),
                    value_transform(PyTuple_GET_ITEM(item, 1)));
            if (new_item == NULL) goto error;

            PyList_SET_ITEM(sl_new, i, new_item);
        }
    }

    return result;

error:
    Py_DECREF(result);
    return NULL;
}
