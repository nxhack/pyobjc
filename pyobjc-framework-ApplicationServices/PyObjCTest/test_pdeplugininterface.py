import PrintCore
import sys
from PyObjCTools.TestSupport import *

class TestPDEPluginInterfaceHelper (PrintCore.NSObject):
    def initWithBundle_(self, value): return 1
    def shouldHide(self): return 1
    def saveValuesAndReturnError_(self, value): return (1, None)
    def restoreValuesAndReturnError_(self, value): return (1, None)
    def shouldShowHelp(self): return 1
    def shouldPrint(self): return 1
    def printWindowWillClose_(self, value): pass
    def willChangePPDOptionKeyValue_ppdChoice_(self, a, b): return 1

class TestPDEPluginInterface (TestCase):
    def testMethods(self):
        self.assertResultIsBOOL(TestPDEPluginInterfaceHelper.initWithBundle_)
        self.assertResultIsBOOL(TestPDEPluginInterfaceHelper.shouldHide)
        self.assertResultIsBOOL(TestPDEPluginInterfaceHelper.saveValuesAndReturnError_)
        self.assertArgIsOut(TestPDEPluginInterfaceHelper.saveValuesAndReturnError_, 0)
        self.assertResultIsBOOL(TestPDEPluginInterfaceHelper.restoreValuesAndReturnError_)
        self.assertArgIsOut(TestPDEPluginInterfaceHelper.restoreValuesAndReturnError_, 0)
        self.assertResultIsBOOL(TestPDEPluginInterfaceHelper.shouldShowHelp)
        self.assertResultIsBOOL(TestPDEPluginInterfaceHelper.shouldPrint)
        self.assertArgIsBOOL(TestPDEPluginInterfaceHelper.printWindowWillClose_, 0)
        self.assertResultIsBOOL(TestPDEPluginInterfaceHelper.willChangePPDOptionKeyValue_ppdChoice_)


if __name__ == "__main__":
    main()
