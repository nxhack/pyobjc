'''
Wrappers for the "GameController" framework on macOS introduced in macOS 10.9.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
'''

from pyobjc_setup import setup, Extension
import os

VERSION="5.3"

setup(
    name='pyobjc-framework-GameController',
    description = "Wrappers for the framework GameController on macOS",
    packages = [ "GameController" ],
    version=VERSION,
    install_requires = [
        'pyobjc-core>='+VERSION,
        'pyobjc-framework-Cocoa>='+VERSION,
    ],
    long_description=__doc__,
)
