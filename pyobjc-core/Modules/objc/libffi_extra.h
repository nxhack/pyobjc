/*
 * Some functions that make working with libffi APIs more convenient
 * when supporting various versions of macOS with the system  install
 * of libffi.
 */

/*
 * ffi_alloc_closure + ffi_prep_closure
 */
#include "ffi.h"
extern int  alloc_prepped_closure(ffi_closure** cl, ffi_cif* cif, void** codeloc,
                                  void* func, void* userdata);
