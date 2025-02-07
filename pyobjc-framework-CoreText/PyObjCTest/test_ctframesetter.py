
from PyObjCTools.TestSupport import *
from CoreText import *

try:
    from Quartz import CGSize
except ImportError:
    CGSize = None, None


class TestCTFramesetter (TestCase):

    def testTypes(self):
        self.assertIsInstance(CTFramesetterRef, objc.objc_class)

    def testFunctions(self):
        v = CTFramesetterGetTypeID()
        self.assertIsInstance(v, (int, long))

        setter = CTFramesetterCreateWithAttributedString(
                    CFAttributedStringCreate(None, b"hello".decode('latin1'), None))
        self.assertIsInstance(setter, CTFramesetterRef)

        # CTFramesetterCreateFrame: tested in test_ctframe.py

        v = CTFramesetterGetTypesetter(setter)
        self.assertIsInstance(v, CTTypesetterRef)

    @min_os_level('10.5')
    @onlyIf(CGSize is not None, "CoreGraphics not available")
    def testMethods10_5(self):
        setter = CTFramesetterCreateWithAttributedString(
                    CFAttributedStringCreate(None, b"hello".decode('latin1'), None))
        self.assertIsInstance(setter, CTFramesetterRef)

        self.assertArgIsOut(CTFramesetterSuggestFrameSizeWithConstraints, 4)

        r = CTFramesetterSuggestFrameSizeWithConstraints(
                setter, CFRange(0, 2), None, CGSize(100, 500),
                None)
        self.assertIsInstance(r, tuple)
        self.assertEqual(len(r), 2)

        size, range = r

        self.assertIsInstance(size, CGSize)
        self.assertIsInstance(range, CFRange)

    @min_os_level('10.14')
    def testMethods10_14(self):
        self.assertResultIsCFRetained(CTFramesetterCreateWithTypesetter)


if __name__ == "__main__":
    main()
