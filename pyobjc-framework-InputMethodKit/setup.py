'''
Wrappers for the "InputMethodKit" framework on macOS 10.5 or later. The
interfaces in this framework allow you to develop input methods.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
'''
from pyobjc_setup import setup, Extension
import os

VERSION="5.3"

setup(
    name='pyobjc-framework-InputMethodKit',
    description = "Wrappers for the framework InputMethodKit on macOS",
    min_os_level='10.5',
    packages = [ "InputMethodKit" ],
    ext_modules = [
        Extension("InputMethodKit._InputMethodKit",
            [ "Modules/_InputMethodKit.m" ],
            extra_link_args=["-framework", "InputMethodKit"],
            depends=[
                os.path.join('Modules', fn)
                    for fn in os.listdir('Modules')
                    if fn.startswith('_InputMethodKit')
            ]
       ),
    ],
    version=VERSION,
    install_requires = [
        'pyobjc-core>='+VERSION,
        'pyobjc-framework-Cocoa>='+VERSION,
    ],
    long_description=__doc__,
)
