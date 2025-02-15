"""
Generic setup.py file for PyObjC framework wrappers.

This file should only be changed in pyobjc-core and then copied
to all framework wrappers.
"""

__all__ = ('setup', 'Extension', 'Command')

import sys
from pkg_resources import Distribution

try:
    import setuptools

except ImportError:
    print("This package requires setuptools to build")
    sys.exit(1)

from setuptools.command import test
from setuptools.command import egg_info
from setuptools.command import build_py
from distutils.sysconfig import get_config_var, get_config_vars

from distutils import log
import shlex

class oc_build_py (build_py.build_py):
    def build_packages(self):
        log.info("overriding build_packages to copy PyObjCTest")
        p = self.packages
        self.packages = list(self.packages) + ['PyObjCTest']
        try:
            build_py.build_py.build_packages(self)
        finally:
            self.packages = p


from pkg_resources import working_set, normalize_path, add_activation_listener, require
from distutils.errors import DistutilsPlatformError, DistutilsError

REPO_NAME='pyobjc'

class oc_egg_info (egg_info.egg_info):
    def run(self):
        egg_info.egg_info.run(self)

        path = os.path.join(self.egg_info, 'PKG-INFO')
        with open(path, 'a+') as fp:
            fp.write('Project-URL: Documentation, https://%s.readthedocs.io/en/latest/\n' % (REPO_NAME,))
            fp.write('Project-URL: Issue tracker, https://bitbucket.org/ronaldoussoren/%s/issues?status=new&status=open\n' % (REPO_NAME,))

class oc_test (test.test):
    description = "run test suite"
    user_options = [
        ('verbosity=', None, "print what tests are run"),
    ]

    def initialize_options(self):
        test.test.initialize_options(self)
        self.verbosity='1'

    def finalize_options(self):
        test.test.finalize_options(self)
        if isinstance(self.verbosity, str):
            self.verbosity = int(self.verbosity)


    def cleanup_environment(self):
        from pkg_resources import add_activation_listener
        add_activation_listener(lambda dist: dist.activate())

        ei_cmd = self.get_finalized_command('egg_info')
        egg_name = ei_cmd.egg_name.replace('-', '_')

        to_remove =  []
        for dirname in sys.path:
            bn = os.path.basename(dirname)
            if bn.startswith(egg_name + "-"):
                to_remove.append(dirname)

        for dirname in to_remove:
            log.info("removing installed %r from sys.path before testing"%(
                dirname,))
            sys.path.remove(dirname)

        working_set.__init__()

    def add_project_to_sys_path(self):
        from pkg_resources import normalize_path, add_activation_listener
        from pkg_resources import working_set, require

        self.reinitialize_command('egg_info')
        self.run_command('egg_info')
        self.reinitialize_command('build_ext', inplace=1)
        self.run_command('build_ext')

        self.__old_path = sys.path[:]
        self.__old_modules = sys.modules.copy()

        if 'PyObjCTools' in sys.modules:
            del sys.modules['PyObjCTools']


        ei_cmd = self.get_finalized_command('egg_info')
        sys.path.insert(0, normalize_path(ei_cmd.egg_base))
        sys.path.insert(1, os.path.dirname(__file__))

        add_activation_listener(lambda dist: dist.activate())
        working_set.__init__()
        require('%s==%s'%(ei_cmd.egg_name, ei_cmd.egg_version))

    def remove_from_sys_path(self):
        from pkg_resources import working_set
        sys.path[:] = self.__old_path
        sys.modules.clear()
        sys.modules.update(self.__old_modules)
        working_set.__init__()


    def run(self):
        import unittest
        import time

        # Ensure that build directory is on sys.path (py3k)
        import sys

        self.cleanup_environment()
        self.add_project_to_sys_path()

        import PyObjCTools.TestSupport as modo

        from pkg_resources import EntryPoint
        loader_ep = EntryPoint.parse("x="+self.test_loader)
        loader_class = loader_ep.resolve()

        import warnings
        warnings.simplefilter("error")

        try:
            meta = self.distribution.metadata
            name = meta.get_name()
            test_pkg = name + "_tests"

            time_before = time.time()
            suite = loader_class().loadTestsFromName(self.distribution.test_suite)

            runner = unittest.TextTestRunner(verbosity=self.verbosity)
            result = runner.run(suite)

            time_after = time.time()

            # Print out summary. This is a structured format that
            # should make it easy to use this information in scripts.
            summary = dict(
                count=result.testsRun,
                fails=len(result.failures),
                errors=len(result.errors),
                xfails=len(getattr(result, 'expectedFailures', [])),
                xpass=len(getattr(result, 'unexpectedSuccesses', [])),
                skip=len(getattr(result, 'skipped', [])),
                testSeconds=(time_after - time_before),
            )
            print("SUMMARY: %s"%(summary,))
            if not result.wasSuccessful():
                raise DistutilsError("some tests failed")

        finally:
            self.remove_from_sys_path()


from setuptools import setup as _setup, Extension as _Extension, Command
from distutils.command import build, install
from setuptools.command import develop, test, build_ext, install_lib
import pkg_resources
import shutil
import os
import plistlib
import sys

CLASSIFIERS = list(filter(None,
"""
Development Status :: 5 - Production/Stable
Environment :: Console
Environment :: MacOS X :: Cocoa
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Natural Language :: English
Operating System :: MacOS :: MacOS X
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Objective C
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: User Interfaces
""".splitlines()))


def get_os_level():
    pl = plistlib.readPlist('/System/Library/CoreServices/SystemVersion.plist')
    v = pl['ProductVersion']
    return '.'.join(v.split('.')[:2])

def get_sdk_level():
    cflags = get_config_var('CFLAGS')
    cflags = shlex.split(cflags)
    for i, val in enumerate(cflags):
        if val == '-isysroot':
            sdk = cflags[i+1]
            break
    else:
        return None

    if sdk == '/':
        return get_os_level()

    sdk = os.path.basename(sdk)
    assert sdk.startswith('MacOSX')
    assert sdk.endswith('.sdk')
    return sdk[6:-4]

class pyobjc_install_lib (install_lib.install_lib):
    def get_exclusions(self):
        result = install_lib.install_lib.get_exclusions(self)
        if hasattr(install_lib, '_install_lib'):
            outputs = install_lib._install_lib.get_outputs(self)
        else:
            outputs = install_lib.orig.install_lib.get_outputs(self)

        exclusions = {}
        for fn in outputs:
            if 'PyObjCTest' in fn:
                exclusions[fn] = 1

        exclusions['PyObjCTest'] = 1
        exclusions[os.path.join(self.install_dir, 'PyObjCTest')] = 1
        for fn in os.listdir('PyObjCTest'):
            exclusions[os.path.join('PyObjCTest', fn)] = 1
            exclusions[os.path.join(self.install_dir, 'PyObjCTest', fn)] = 1
        result.update(exclusions)

        return result

def _find_executable(executable):
    if os.path.isfile(executable):
        return executable

    else:
        for p in os.environ['PATH'].split(os.pathsep):
            f = os.path.join(p, executable)
            if os.path.isfile(f):
                return executable
    return None

def _working_compiler(executable):
    import tempfile, subprocess
    with tempfile.NamedTemporaryFile(mode='w', suffix='.c') as fp:
        fp.write('#include <stdarg.h>\nint main(void) { return 0; }\n')
        fp.flush()

        cflags = get_config_var('CFLAGS')
        cflags = shlex.split(cflags)

        p = subprocess.Popen([
            executable, '-c', fp.name] + cflags,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit = p.wait()
        p.stdout.close()
        p.stderr.close()
        if exit != 0:
            return False

        binfile = fp.name[:-1] + 'o'
        if os.path.exists(binfile):
            os.unlink(binfile)


        binfile = os.path.basename(binfile)
        if os.path.exists(binfile):
            os.unlink(binfile)

    return True

def _fixup_compiler():
    if 'CC' in os.environ:
        # CC is in the environment, always use explicit
        # overrides.
        return

    try:
        import _osx_support
        _osx_support.customize_compiler(get_config_vars())
    except (ImportError, NameError):
        pass




    cc = oldcc = get_config_var('CC').split()[0]
    cc = _find_executable(cc)
    if cc is not None and os.path.basename(cc).startswith('gcc'):
        # Check if compiler is LLVM-GCC, that's known to
        # generate bad code.
        data = os.popen("'%s' --version 2>/dev/null"%(
            cc.replace("'", "'\"'\"'"),)).read()
        if 'llvm-gcc' in data:
            cc = None

    if cc is not None and not _working_compiler(cc):
        cc = None

    if cc is None:
        # Default compiler is not useable, try finding 'clang'
        cc = _find_executable('clang')
        if cc is None:
            cc = os.popen("/usr/bin/xcrun -find clang").read()

    if not cc:
        raise SystemExit("Cannot locate compiler candidate")

    if not _working_compiler(cc):
        raise SystemExit("Cannot locate a working compiler")

    if cc != oldcc:
        print("Use '%s' instead of '%s' as the compiler"%(
            cc, oldcc))

        vars = get_config_vars()
        for env in ('BLDSHARED', 'LDSHARED', 'CC', 'CXX'):
            if env in vars and env not in os.environ:
                split = vars[env].split()
                split[0] = cc if env != 'CXX' else cc + '++'
                vars[env] = ' '.join(split)

class pyobjc_build_ext (build_ext.build_ext):
    def run(self):
        _fixup_compiler()

        # Ensure that the PyObjC header files are available
        # in 2.3 and later the headers are in the egg,
        # before that we ship a copy.
        if not os.path.isfile('Modules/pyobjc-api.h'):
            dist, = pkg_resources.require('pyobjc-core')

            include_root = os.path.join(self.build_temp, 'pyobjc-include')
            if os.path.exists(include_root):
                shutil.rmtree(include_root)

            os.makedirs(include_root)
            if dist.has_metadata('include'):
                for fn in dist.metadata_listdir('include'):
                    data = dist.get_metadata('include/%s'%(fn,))
                    fp = open(os.path.join(include_root, fn), 'w')
                    try:
                        fp.write(data)
                    finally:
                        fp.close()

            else:
                raise SystemExit("pyobjc-core egg-info does not include header files")

            for e in self.extensions:
                if include_root not in e.include_dirs:
                    e.include_dirs.append(include_root)

        # Run the actual build
        build_ext.build_ext.run(self)

        # Then tweak the copy_extensions bit to ensure PyObjCTest gets
        # copied to the right place.
        extensions = self.extensions
        self.extensions = [
            e for e in extensions if e.name.startswith('PyObjCTest') ]
        self.copy_extensions_to_source()
        self.extensions = extensions



def Extension(*args, **kwds):
    """
    Simple wrapper about distutils.core.Extension that adds additional PyObjC
    specific flags.
    """
    os_level = get_sdk_level()
    if os_level is None:
        os_level = get_os_level()

    cflags =  []
    ldflags = []
    if 'clang' in get_config_var('CC'):
        cflags.append('-Wno-deprecated-declarations')

    CFLAGS = get_config_var('CFLAGS')
    if '-isysroot' not in CFLAGS: # and os.path.exists('/usr/include/stdio.h'):
        # We're likely on a system with de Xcode Command Line Tools.
        # Explicitly use the most recent problems to avoid compile problems.
        data = os.popen('/usr/bin/xcrun -sdk macosx --show-sdk-path').read()
        data = data.strip()
        if data:
            cflags.append('-isysroot')
            cflags.append(data)
            cflags.append("-DPyObjC_BUILD_RELEASE=%02d%02d"%(tuple(map(int, os.path.basename(data)[6:-4].split('.')))))

    else:
            cflags.append("-DPyObjC_BUILD_RELEASE=%02d%02d"%(tuple(map(int, os_level.split('.')))))


    if os_level == '10.4':
        cflags.append('-DNO_OBJC2_RUNTIME')

    if 'extra_compile_args' in kwds:
        kwds['extra_compile_args'] = kwds['extra_compile_args'] + cflags
    else:
        kwds['extra_compile_args'] = cflags

    if 'extra_link_args' in kwds:
        kwds['extra_link_args'] = kwds['extra_link_args'] + ldflags
    else:
        kwds['extra_link_args'] = ldflags

    return _Extension(*args, **kwds)

def _sort_key(version):
   return tuple(int(x) for x in version.split('.'))

def setup(
        min_os_level=None,
        max_os_level=None,
        cmdclass=None,
        **kwds):


    k = kwds.copy()

    os_level = get_sdk_level()
    if os_level is None:
        os_level = get_os_level()
    os_compatible = True
    if sys.platform != 'darwin':
        os_compatible = False

    else:
        if min_os_level is not None:
            if _sort_key(os_level) < _sort_key(min_os_level):
                os_compatible = False
        if max_os_level is not None:
            if _sort_key(os_level) > _sort_key(max_os_level):
                os_compatible = False

    if cmdclass is None:
        cmdclass = {}
    else:
        cmdclass = cmdclass.copy()

    if os_compatible or ('bdist_wheel' in sys.argv and 'ext_modules' not in k):
        cmdclass['build_ext'] = pyobjc_build_ext
        cmdclass['egg_info'] = oc_egg_info
        cmdclass['install_lib'] = pyobjc_install_lib
        cmdclass['test'] = oc_test
        cmdclass['build_py'] = oc_build_py

    else:
        if min_os_level != None:
            if max_os_level != None:
                msg = "This distribution is only supported on MacOSX versions %s upto and including %s"%(
                        min_os_level, max_os_level)
            else:
                msg = "This distribution is only supported on MacOSX >= %s"%(min_os_level,)
        elif max_os_level != None:
            msg = "This distribution is only supported on MacOSX <= %s"%(max_os_level,)
        else:
            msg = "This distribution is only supported on MacOSX"

        def create_command_subclass(base_class):

            class subcommand (base_class):
                def run(self, msg=msg):
                    raise DistutilsPlatformError(msg)

            return subcommand

        class no_test (oc_test):
            def run(self, msg=msg):
                print("WARNING: %s\n"%(msg,))
                print("SUMMARY: {'testSeconds': 0.0, 'count': 0, 'fails': 0, 'errors': 0, 'xfails': 0, 'skip': 65, 'xpass': 0, 'message': %r }"%(msg,))

        cmdclass['build'] = create_command_subclass(build.build)
        cmdclass['test'] = no_test
        cmdclass['install'] = create_command_subclass(install.install)
        cmdclass['install_lib'] = create_command_subclass(pyobjc_install_lib)
        cmdclass['develop'] = create_command_subclass(develop.develop)
        cmdclass['build_py'] = create_command_subclass(oc_build_py)

    if 'ext_modules' not in k:
        # No extension modules, can build universal wheel
        k['options'] = {
            'bdist_wheel': {
                'universal': 1,
            }
        }

    plat_name = "MacOS X"
    plat_versions = []
    if min_os_level is not None and min_os_level == max_os_level:
        plat_versions.append("==%s"%(min_os_level,))
    else:
        if min_os_level is not None:
            plat_versions.append(">=%s"%(min_os_level,))
        if max_os_level is not None:
            plat_versions.append("<=%s"%(max_os_level,))
    if plat_versions:
        plat_name += " (%s)"%(", ".join(plat_versions),)

    if os.path.isfile('Modules/pyobjc-api.h') or 'ext_modules' not in k:
        if 'setup_requires' in k:
            if len(k['setup_requires']) == 1 and k['setup_requires'][0].startswith('pyobjc-core'):
                del k['setup_requires']

    if 'long_description' in k:
        k['long_description'] += "\n\nProject links\n"
        k['long_description'] += "-------------\n"
        k['long_description'] += "\n"
        k['long_description'] += "* `Documentation <https://%s.readthedocs.io/en/latest/>`_\n\n" % (REPO_NAME,)
        k['long_description'] += "* `Issue Tracker <https://bitbucket.org/ronaldoussoren/%s/issues?status=new&status=open>`_\n\n" % (REPO_NAME,)
        k['long_description'] += "* `Repository <https://bitbucket.org/ronaldoussoren/%s/>`_\n\n" % (REPO_NAME,)
        k['long_description_content_type'] = 'text/x-rst; charset=UTF-8'

    _setup(
        cmdclass=cmdclass,
        author='Ronald Oussoren',
        author_email='pyobjc-dev@lists.sourceforge.net',
        url='https://bitbucket.org/ronaldoussoren/pyobjc',
        platforms = [ plat_name ],
        package_dir = { '': 'Lib', 'PyObjCTest': 'PyObjCTest' },
        dependency_links = [],
        package_data = { '': ['*.bridgesupport'] },
        test_suite='PyObjCTest',
        zip_safe = False,
        license = 'MIT License',
        classifiers = CLASSIFIERS,
        keywords = ["PyObjC"] + [ p for p in k['packages'] if p not in ('PyObjCTools',)],
        **k
    )
