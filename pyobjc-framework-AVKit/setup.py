'''
Wrappers for the "AVKit" framework on macOS introduced in macOS 10.9.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
'''

from pyobjc_setup import setup, Extension
import os

VERSION="5.3"

setup(
    name='pyobjc-framework-AVKit',
    description = "Wrappers for the framework AVKit on macOS",
    min_os_level="10.9",
    packages = [ "AVKit" ],
    ext_modules = [
        Extension("AVKit._AVKit",
            [ "Modules/_AVKit.m" ],
            extra_link_args=["-framework", "AVKit"],
            depends=[
                os.path.join('Modules', fn)
                    for fn in os.listdir('Modules')
                    if fn.startswith('_AVKit')
            ]
        ),
    ],
    version=VERSION,
    install_requires = [
        'pyobjc-core>='+VERSION,
        'pyobjc-framework-Cocoa>='+VERSION,
        'pyobjc-framework-Quartz>='+VERSION,
    ],
    long_description=__doc__,
)
