/*
 * This file implements generic support for CoreFoundation types.
 *
 * CF-based proxy types are implemented as subclasses of the proxy for NSCFType,
 * that way CF-based types fit in nicely with the PyObjC machinery (specifically
 * subclass tests keep working).
 *
 * Major assumption:
 * - NSCFType is the ObjC type that all non-toll-free bridged types inherit
 *   from, toll-free bridged types are not subclasses of NSCFType.
 */
#include "pyobjc.h"

#include <CoreFoundation/CoreFoundation.h>

static PyObject* gTypeid2class = NULL;
PyObject* PyObjC_NSCFTypeClass = NULL;

static PyObject*
cf_repr(PyObject* self)
{
    if (PyObjCObject_GetFlags(self) & PyObjCObject_kMAGIC_COOKIE) {
        return PyText_FromFormat(
            "<%s CoreFoundation magic instance %p>",
            Py_TYPE(self)->tp_name, PyObjCObject_GetObject(self));
    }

    CFStringRef repr = CFCopyDescription(PyObjCObject_GetObject(self));
    if (repr) {
        PyObject* result = pythonify_c_value(@encode(id), &repr);
        CFRelease(repr);
        return result;

    } else {
        char buf[128];
        snprintf(buf, sizeof(buf), "<%s object at %p>",
            Py_TYPE(self)->tp_name,
            PyObjCObject_GetObject(self));

        return PyText_FromString(buf);
    }
}

PyObject*
PyObjC_TryCreateCFProxy(NSObject* value)
{
    PyObject *rval = NULL;

    if (gTypeid2class != NULL) {
        PyObject* cfid;
        PyTypeObject* tp;

        cfid = PyInt_FromLong(CFGetTypeID((CFTypeRef)value));
#if PY_MAJOR_VERSION == 3
        tp = (PyTypeObject*)PyDict_GetItem(gTypeid2class, cfid);
        Py_DECREF(cfid);
        if (tp == NULL && PyErr_Occurred()) {
            return NULL;
        }
#else
        tp = (PyTypeObject*)PyDict_GetItem(gTypeid2class, cfid);
        Py_DECREF(cfid);
#endif

        if (tp != NULL) {
            rval = tp->tp_alloc(tp, 0);
            if (rval == NULL) {
                return NULL;
            }

            ((PyObjCObject*)rval)->objc_object = value;
            ((PyObjCObject*)rval)->flags = PyObjCObject_kDEFAULT | PyObjCObject_kCFOBJECT;
            CFRetain(value);
        }
    }
    return rval;
}

#ifdef PyObjC_ENABLE_CFTYPE_CATEGORY
/* Implementation for: -(PyObject*)__pyobjc_PythonObject__ on NSCFType. We cannot
 * define a category on that type because the class definition isn't public.
 */
static PyObject*
pyobjc_PythonObject(NSObject* self, SEL _sel __attribute__((__unused__)))
{
    PyObject *rval = NULL;

    rval = PyObjC_FindPythonProxy(self);
    if (rval == NULL) {
        rval = PyObjC_TryCreateCFProxy(self);
        if (rval == NULL && PyErr_Occurred()) {
            return NULL;
        }
        if (rval == NULL) {
            /* There is no wrapper for this type, fall back to
             * the generic behaviour.
             */
            rval = (PyObject *)PyObjCObject_New(self,
                PyObjCObject_kDEFAULT, YES);
        }

        if (rval) {
            PyObjC_RegisterPythonProxy(self, rval);
        }
    }

    return rval;
}
#endif


PyObject*
PyObjCCFType_New(char* name, char* encoding, CFTypeID typeID)
{
    PyObject* args;
    PyObject* dict;
    PyObject* result;
    PyObject* bases;
    PyObjCClassObject* info;

    /*
     * First look for an already registerd type
     */
    if (encoding[0] != _C_ID) {
        if (PyObjCPointerWrapper_RegisterID(name, encoding) == -1) {
            return NULL;
        }
    }

    if (typeID == 0) {
        /* Partially registered type, just wrap as a
         * a plain CFTypeRef
         */
        Py_INCREF(PyObjC_NSCFTypeClass);
        return PyObjC_NSCFTypeClass;
    }

    PyObject* cf = PyLong_FromUnsignedLongLong(typeID);
    if (cf == NULL) {
        return NULL;
    }

#if PY_MAJOR_VERSION == 3
    result = PyDict_GetItemWithError(gTypeid2class, cf);
    if (result == NULL && PyErr_Occurred()) {
        Py_DECREF(cf);
        return NULL;
    }
#else

    result = PyDict_GetItem(gTypeid2class, cf);
#endif
    if (result != NULL) {
        /* This type is the same as an already registered type,
         * return that type
         */
        Py_DECREF(cf);
        Py_INCREF(result);
        return result;
    }

    /*
     * If that doesn't exist create a new one.
     */

    dict = PyDict_New();
    if (dict == NULL) {
        Py_DECREF(cf);
        return NULL;
    }

    PyDict_SetItemString(dict, "__slots__", PyTuple_New(0));

    bases = PyTuple_New(1);

    PyTuple_SET_ITEM(bases, 0, PyObjC_NSCFTypeClass);
    Py_INCREF(PyObjC_NSCFTypeClass);

    args = PyTuple_New(3);
    PyTuple_SetItem(args, 0, PyText_FromString(name));
    PyTuple_SetItem(args, 1, bases);
    PyTuple_SetItem(args, 2, dict);

    result = PyType_Type.tp_new(&PyObjCClass_Type, args, NULL);
    Py_DECREF(args);
    if (result == NULL) {
        Py_DECREF(cf);
        return NULL;
    }

    ((PyTypeObject*)result)->tp_repr = cf_repr;
    ((PyTypeObject*)result)->tp_str = cf_repr;

    info = (PyObjCClassObject*)result;
    info->class = PyObjCClass_GetClass(PyObjC_NSCFTypeClass);
    info->sel_to_py = NULL;
    info->dictoffset = 0;
    info->useKVO = 0;
    info->delmethod = NULL;
    info->hasPythonImpl = 0;
    info->isCFWrapper = 1;

    if (PyObject_SetAttrString(result,
            "__module__", PyObjCClass_DefaultModule) < 0) {
        PyErr_Clear();
    }

    if (PyDict_SetItem(gTypeid2class, cf, result) == -1) {
        Py_DECREF(result);
        Py_DECREF(cf);
        return NULL;
    }

    Py_DECREF(cf); cf = NULL;
    return result;
}

static const char* gNames[] = {
    "__NSCFType",
    "NSCFType",
    NULL,
};

int
PyObjCCFType_Setup(void)
{
#ifdef PyObjC_ENABLE_CFTYPE_CATEGORY
    static char encodingBuf[128];
#endif
    Class cls;
    const char** cur;

    gTypeid2class = PyDict_New();
    if (gTypeid2class == NULL) {
        return -1;
    }

#ifdef PyObjC_ENABLE_CFTYPE_CATEGORY
    snprintf(encodingBuf, sizeof(encodingBuf), "%s%c%c", @encode(PyObject*), _C_ID, _C_SEL);
#endif

    for (cur = gNames; *cur != NULL; cur++) {
        cls = objc_lookUpClass(*cur);
        if (cls == Nil) continue;

#ifdef PyObjC_ENABLE_CFTYPE_CATEGORY
        /* Add a __pyobjc_PythonObject__ method to NSCFType. Can't use a
         * category because the type isn't public.
         */
        if (!class_addMethod(cls, @selector(__pyobjc_PythonObject__),
            (IMP)pyobjc_PythonObject, encodingBuf)) {

            return -1;
        }
#endif

        if (PyObjC_NSCFTypeClass == NULL) {
            PyObjC_NSCFTypeClass = PyObjCClass_New(cls);
            if (PyObjC_NSCFTypeClass == NULL) {
                return -1;
            }
        }
#ifndef PyObjC_ENABLE_CFTYPE_CATEGORY
        break;
#endif
    }

    if (PyObjC_NSCFTypeClass == NULL) {
        PyErr_SetString(PyExc_RuntimeError,
            "Cannot locate NSCFType");
        return -1;
    }

    return 0;
}

/*
 * Create proxy object for a special value of a CFType, that
 * is a value that just a magic cookie and not a valid
 * object. Such objects are sometimes used in CoreFoundation
 * (sadly enough).
 */
PyObject*
PyObjCCF_NewSpecial(char* typestr, void* datum)
{
    PyObject* rval = NULL;
#if PY_MAJOR_VERSION == 3
    PyObject* v = PyDict_GetItemStringWithError(PyObjC_TypeStr2CFTypeID, typestr);

#else
    PyObject* v = PyDict_GetItemString(PyObjC_TypeStr2CFTypeID, typestr);
#endif

    CFTypeID typeid;

    if (v == NULL) {
        if (PyErr_Occurred()) {
            return NULL;
        }
        PyErr_Format(PyExc_ValueError, "Don't know CF type for typestr '%s', cannot create special wrapper", typestr);
        return NULL;
    }

    if (depythonify_c_value(@encode(CFTypeID), v, &typeid) < 0) {
        return NULL;
    }

    if (gTypeid2class != NULL) {
        PyObject* cfid;
        PyTypeObject* tp;

        cfid = PyInt_FromLong(typeid);
#if PY_MAJOR_VERSION == 3
        tp = (PyTypeObject*)PyDict_GetItemWithError(gTypeid2class, cfid);
        Py_DECREF(cfid);

        if (tp == NULL && PyErr_Occurred()) {
            return NULL;
        }
#else
        tp = (PyTypeObject*)PyDict_GetItem(gTypeid2class, cfid);
        Py_DECREF(cfid);
#endif

        if (tp != NULL) {
            rval = tp->tp_alloc(tp, 0);
            if (rval == NULL) {
                return NULL;
            }

            ((PyObjCObject*)rval)->objc_object = (id)datum;
            ((PyObjCObject*)rval)->flags = PyObjCObject_kDEFAULT|PyObjCObject_kSHOULD_NOT_RELEASE|PyObjCObject_kMAGIC_COOKIE;
        }

    } else {
        rval = NULL;
        PyErr_Format(PyExc_ValueError,
            "Sorry, cannot wrap special value of typeid %d\n",
            (int)typeid);
    }

    return rval;
}

/*
 * Create proxy object for a special value of a CFType, that
 * is a value that just a magic cookie and not a valid
 * object. Such objects are sometimes used in CoreFoundation
 * (sadly enough).
 */
PyObject*
PyObjCCF_NewSpecial2(CFTypeID typeid, void* datum)
{
    PyObject *rval = NULL;

    if (gTypeid2class != NULL) {
        PyObject* cfid;
        PyTypeObject* tp;

        cfid = PyInt_FromLong(typeid);
#if PY_MAJOR_VERSION == 3
        tp = (PyTypeObject*)PyDict_GetItemWithError(gTypeid2class, cfid);
        Py_DECREF(cfid);
        if (tp == NULL && PyErr_Occurred()) {
            return NULL;
        }
#else
        tp = (PyTypeObject*)PyDict_GetItem(gTypeid2class, cfid);
        Py_DECREF(cfid);
#endif

        if (tp != NULL) {
            rval = tp->tp_alloc(tp, 0);
            if (rval == NULL) {
                return NULL;
            }

            ((PyObjCObject*)rval)->objc_object = (id)datum;
            ((PyObjCObject*)rval)->flags = PyObjCObject_kDEFAULT|PyObjCObject_kSHOULD_NOT_RELEASE|PyObjCObject_kMAGIC_COOKIE;
        }

    } else {
        rval = NULL;
        PyErr_Format(PyExc_ValueError,
            "Sorry, cannot wrap special value of typeid %d\n",
            (int)typeid);
    }

    return rval;
}
