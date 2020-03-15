import re

import CoreFoundation
from PyObjCTools.TestSupport import TestCase


class TestCFUUIDAPI(TestCase):
    def testTypes(self):
        self.assertIsCFType(CoreFoundation.CFUUIDRef)

    def testTypeID(self):
        v = CoreFoundation.CFUUIDGetTypeID()
        self.assertIsInstance(v, int)

    def testCreate(self):
        self.assertResultIsCFRetained(CoreFoundation.CFUUIDCreate)
        uuid = CoreFoundation.CFUUIDCreate(None)
        self.assertIsNot(uuid, None)
        self.assertIsInstance(uuid, CoreFoundation.CFUUIDRef)
        text = CoreFoundation.CFUUIDCreateString(None, uuid)
        self.assertIsInstance(text, str)
        m = re.match("^[0-9A-Z]{8}(-[0-9A-Z]{4}){3}-[0-9A-Z]{12}$", text)
        self.assertIsNot(m, None)

    def testCreateWithBytes(self):
        self.assertResultIsCFRetained(CoreFoundation.CFUUIDCreateWithBytes)
        uuid = CoreFoundation.CFUUIDCreateWithBytes(
            None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
        )
        self.assertIsNot(uuid, None)
        self.assertIsInstance(uuid, CoreFoundation.CFUUIDRef)
        self.assertResultIsCFRetained(CoreFoundation.CFUUIDCreateString)
        text = CoreFoundation.CFUUIDCreateString(None, uuid)
        self.assertEqual(text, b"01020304-0506-0708-090A-0B0C0D0E0F10".decode("ascii"))
        self.assertRaises(
            ValueError,
            CoreFoundation.CFUUIDCreateWithBytes,
            None,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            300,
        )
        self.assertRaises(
            ValueError,
            CoreFoundation.CFUUIDCreateWithBytes,
            None,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            300,
            16,
        )

    def testCreateFromString(self):
        self.assertResultIsCFRetained(CoreFoundation.CFUUIDCreateFromString)
        uuid1 = CoreFoundation.CFUUIDCreateFromString(
            None, b"01020304-0506-0708-090A-0B0C0D0E0F10".decode("ascii")
        )
        self.assertIsNot(uuid1, None)
        self.assertIsInstance(uuid1, CoreFoundation.CFUUIDRef)
        text = CoreFoundation.CFUUIDCreateString(None, uuid1)
        self.assertEqual(text, b"01020304-0506-0708-090A-0B0C0D0E0F10".decode("ascii"))
        uuid2 = CoreFoundation.CFUUIDCreateFromString(
            None, b"01020304-0506-0708-090A-0B0C0D0E0F10".decode("ascii")
        )
        text = CoreFoundation.CFUUIDCreateString(None, uuid2)
        self.assertEqual(text, b"01020304-0506-0708-090A-0B0C0D0E0F10".decode("ascii"))
        # CoreFoundation.CFUUID interns values
        self.assertIs(uuid1, uuid2)

    def testGetBytes(self):
        uuid = CoreFoundation.CFUUIDCreateWithBytes(
            None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
        )
        self.assertIsNot(uuid, None)
        self.assertIsInstance(uuid, CoreFoundation.CFUUIDRef)
        bytes = CoreFoundation.CFUUIDGetUUIDBytes(uuid)
        self.assertIsInstance(bytes, CoreFoundation.CFUUIDBytes)
        self.assertEqual(bytes.byte0, 1)
        self.assertEqual(bytes.byte1, 2)
        self.assertEqual(bytes.byte2, 3)
        self.assertEqual(bytes.byte3, 4)
        self.assertEqual(bytes.byte4, 5)
        self.assertEqual(bytes.byte5, 6)
        self.assertEqual(bytes.byte6, 7)
        self.assertEqual(bytes.byte7, 8)
        self.assertEqual(bytes.byte8, 9)
        self.assertEqual(bytes.byte9, 10)
        self.assertEqual(bytes.byte10, 11)
        self.assertEqual(bytes.byte11, 12)
        self.assertEqual(bytes.byte12, 13)
        self.assertEqual(bytes.byte13, 14)
        self.assertEqual(bytes.byte14, 15)
        self.assertEqual(bytes.byte15, 16)

    def testConstant(self):
        # This is an interesting one, the result of
        # CoreFoundation.CFUUIDGetConstantUUIDWithBytes should not be released.

        uuid = CoreFoundation.CFUUIDGetConstantUUIDWithBytes(None, *range(16))
        CoreFoundation.CFRetain(
            CoreFoundation.CFUUIDGetConstantUUIDWithBytes
        )  # Ensure the value won't be released.
        self.assertIsNot(uuid, None)
        self.assertIsInstance(uuid, CoreFoundation.CFUUIDRef)
        s = CoreFoundation.CFUUIDCreateString(None, uuid)

        uuid = None
        del uuid

        uuid = CoreFoundation.CFUUIDGetConstantUUIDWithBytes(None, *range(16))
        self.assertIsNot(uuid, None)
        self.assertIsInstance(uuid, CoreFoundation.CFUUIDRef)
        t = CoreFoundation.CFUUIDCreateString(None, uuid)

        self.assertEqual(s, t)

    def testCreateFromUUIDBytes(self):
        bytes = CoreFoundation.CFUUIDBytes(*range(16, 32))
        uuid = CoreFoundation.CFUUIDCreateFromUUIDBytes(None, bytes)

        self.assertIsNot(uuid, None)
        self.assertIsInstance(uuid, CoreFoundation.CFUUIDRef)
        text = CoreFoundation.CFUUIDCreateString(None, uuid)
        self.assertEqual(text, b"10111213-1415-1617-1819-1A1B1C1D1E1F".decode("ascii"))

    def testStructs(self):
        o = CoreFoundation.CFUUIDBytes()
        self.assertHasAttr(o, "byte0")
        self.assertHasAttr(o, "byte1")
        self.assertHasAttr(o, "byte2")
        self.assertHasAttr(o, "byte3")
        self.assertHasAttr(o, "byte4")
        self.assertHasAttr(o, "byte5")
        self.assertHasAttr(o, "byte6")
        self.assertHasAttr(o, "byte7")
        self.assertHasAttr(o, "byte8")
        self.assertHasAttr(o, "byte9")
        self.assertHasAttr(o, "byte10")
        self.assertHasAttr(o, "byte11")
        self.assertHasAttr(o, "byte12")
        self.assertHasAttr(o, "byte13")
        self.assertHasAttr(o, "byte14")
        self.assertHasAttr(o, "byte15")
