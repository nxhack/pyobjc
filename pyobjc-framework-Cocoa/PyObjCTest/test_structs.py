#
# Tests for the struct-wrappers for NSPoint, NSSize, NSRange and NSRect.
#
from Foundation import *
from PyObjCTools.TestSupport import *
import operator

def do_set_slice(op, start, stop, value):
    op[start:stop] = value

def do_del_slice(op, start, stop):
    del op[start:stop]

class TestNSPoint (TestCase):
    def testConstructor(self):
        p = NSPoint()
        self.assertIsInstance(p, NSPoint)
        self.assertEqual(p.x, 0)
        self.assertEqual(p.y, 0)

        p = NSPoint(1,2)
        self.assertIsInstance(p, NSPoint)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p[0], 1)
        self.assertEqual(p[1], 2)

        p = NSPoint(y=1,x=2)
        self.assertIsInstance(p, NSPoint)
        self.assertEqual(p.x, 2)
        self.assertEqual(p.y, 1)
        self.assertEqual(p[1], 1)
        self.assertEqual(p[0], 2)

        self.assertRaises(TypeError, NSPoint, 1, 2, 3)
        self.assertRaises(TypeError, NSPoint, 1, 2, y=3)
        self.assertRaises(TypeError, NSPoint, 1, x=3)
        self.assertRaises(TypeError, NSPoint, x=3, z=4)

    def testMakePoint(self):
        p = NSMakePoint(1, 2)
        self.assertIsInstance(p, NSPoint)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)

    def testHash(self):
        p = NSMakePoint(1, 2)
        self.assertRaises(TypeError, hash, p)

    def testCompare(self):
        p = NSMakePoint(1, 2)
        q = NSMakePoint(2, 3)
        P = (1, 2)
        Q = (2, 3)

        self.assertTrue(not (p < p))
        self.assertTrue(not (p < P))
        self.assertTrue(p < q)
        self.assertTrue(p < Q)

        self.assertTrue(p <= p)
        self.assertTrue(p <= P)
        self.assertTrue(p <= q)
        self.assertTrue(p <= Q)

        self.assertTrue(p == p)
        self.assertTrue(p == P)
        self.assertTrue(not (p == q))
        self.assertTrue(not (p == Q))

        self.assertTrue(p != q)
        self.assertTrue(p != Q)
        self.assertTrue(not(p != p))
        self.assertTrue(not(p != P))

        self.assertTrue(q >= p)
        self.assertTrue(q >= P)
        self.assertTrue(q >= q)
        self.assertTrue(q >= Q)

        self.assertTrue(not (q > q))
        self.assertTrue(not (q > Q))
        self.assertTrue(q > p)
        self.assertTrue(q > P)

    def testRepr(self):
        p = NSPoint()
        self.assertEqual(repr(p), "<NSPoint x=0.0 y=0.0>")

        p = NSPoint(42, 98)
        self.assertEqual(repr(p), "<NSPoint x=42 y=98>")

        p.x = p
        self.assertEqual(repr(p), "<NSPoint x=<NSPoint ...> y=98>")

    def testStr(self):
        p = NSPoint()
        self.assertEqual(str(p), "<NSPoint x=0.0 y=0.0>")

        p = NSPoint(42, 98)
        self.assertEqual(str(p), "<NSPoint x=42 y=98>")

        p.x = p
        self.assertEqual(repr(p), "<NSPoint x=<NSPoint ...> y=98>")

    def testSlice(self):
        p = NSPoint(1,2)
        q = p[:]

        self.assertIsInstance(q, tuple)
        self.assertEqual(q, (1.0,2.0))

    def testDeleteAttr(self):
        p = NSPoint(1,2)
        self.assertRaises(TypeError, delattr, p, 'x')

    def testDeleteSlice(self):
        p = NSPoint(1,2)
        self.assertRaises(TypeError, operator.delitem, p, 0)

    def testAssignSlice(self):
        p = NSPoint(1,2)
        p[:] = (4,5)

        self.assertIsInstance(p, NSPoint)
        self.assertEqual(p.x, 4)
        self.assertEqual(p.y, 5)

        p[:] = p
        self.assertIsInstance(p, NSPoint)
        self.assertEqual(p.x, 4)
        self.assertEqual(p.y, 5)

        self.assertRaises(TypeError, do_set_slice, p, 0, 2, [1,2,3])
        self.assertRaises(TypeError, do_set_slice, p, 0, 2, [3])
        self.assertRaises(TypeError, do_set_slice, p, 0, 3, [1,2,3])

        self.assertRaises(TypeError, do_del_slice, p, 0, 0)
        self.assertRaises(TypeError, do_del_slice, p, 0, 1)
        self.assertRaises(TypeError, do_del_slice, p, 0, 2)

class TestNSSize (TestCase):
    def testConstructor(self):
        p = NSSize()
        self.assertIsInstance(p, NSSize)
        self.assertEqual(p.width, 0)
        self.assertEqual(p.height, 0)

        p = NSSize(1,2)
        self.assertIsInstance(p, NSSize)
        self.assertEqual(p.width, 1)
        self.assertEqual(p.height, 2)
        self.assertEqual(p[0], 1)
        self.assertEqual(p[1], 2)

        p = NSSize(height=1,width=2)
        self.assertIsInstance(p, NSSize)
        self.assertEqual(p.width, 2)
        self.assertEqual(p.height, 1)
        self.assertEqual(p[1], 1)
        self.assertEqual(p[0], 2)

        self.assertRaises(TypeError, NSSize, 1, 2, 3)
        self.assertRaises(TypeError, NSSize, 1, 2, height=3)
        self.assertRaises(TypeError, NSSize, 1, width=3)
        self.assertRaises(TypeError, NSSize, width=3, z=4)

    def testMakeSize(self):
        p = NSMakeSize(1, 2)
        self.assertIsInstance(p, NSSize)
        self.assertEqual(p.width, 1)
        self.assertEqual(p.height, 2)

class TestNSRange (TestCase):
    def testConstructor(self):
        p = NSRange()
        self.assertIsInstance(p, NSRange)
        self.assertEqual(p.location, 0)
        self.assertEqual(p.length, 0)

        p = NSRange(1,2)
        self.assertIsInstance(p, NSRange)
        self.assertEqual(p.location, 1)
        self.assertEqual(p.length, 2)
        self.assertEqual(p[0], 1)
        self.assertEqual(p[1], 2)

        p = NSRange(length=1,location=2)
        self.assertIsInstance(p, NSRange)
        self.assertEqual(p.location, 2)
        self.assertEqual(p.length, 1)
        self.assertEqual(p[1], 1)
        self.assertEqual(p[0], 2)

        self.assertRaises(TypeError, NSRange, 1, 2, 3)
        self.assertRaises(TypeError, NSRange, 1, 2, length=3)
        self.assertRaises(TypeError, NSRange, 1, location=3)
        self.assertRaises(TypeError, NSRange, location=3, z=4)

    def testMakeSize(self):
        p = NSMakeSize(1, 2)
        self.assertIsInstance(p, NSSize)
        self.assertEqual(p.width, 1)
        self.assertEqual(p.height, 2)

class TestNSRect (TestCase):
    def testConstructor(self):
        p = NSRect()
        self.assertIsInstance(p, NSRect)
        self.assertIsNot(p.origin, None)
        self.assertIsNot(p.size, None)
        self.assertEqual(p.origin, NSPoint(0, 0))
        self.assertEqual(p.size, NSSize(0, 0))

        p = NSRect(1,2)
        self.assertIsInstance(p, NSRect)
        self.assertEqual(p.origin, 1)
        self.assertEqual(p.size, 2)
        self.assertEqual(p[0], 1)
        self.assertEqual(p[1], 2)

        p = NSRect(size=1,origin=2)
        self.assertIsInstance(p, NSRect)
        self.assertEqual(p.origin, 2)
        self.assertEqual(p.size, 1)
        self.assertEqual(p[1], 1)
        self.assertEqual(p[0], 2)

        self.assertRaises(TypeError, NSRect, 1, 2, 3)
        self.assertRaises(TypeError, NSRect, 1, 2, origin=3)
        self.assertRaises(TypeError, NSRect, 1, origin=3)
        self.assertRaises(TypeError, NSRect, origin=3, z=4)

    def testMakeRect(self):
        p = NSMakeRect(1, 2, 3, 4)
        self.assertIsInstance(p, NSRect)
        self.assertEqual(p.origin, (1, 2))
        self.assertEqual(p.size, (3,4))
        self.assertEqual(p.origin.x, 1)
        self.assertEqual(p.origin.y, 2)
        self.assertEqual(p.size.width, 3)
        self.assertEqual(p.size.height, 4)

    def testNSEdgeInserts(self):
        v = NSEdgeInsets()
        self.assertEqual(v.top, 0.0)
        self.assertEqual(v.left, 0.0)
        self.assertEqual(v.bottom, 0.0)
        self.assertEqual(v.right, 0.0)



if __name__ == "__main__":
    main()
