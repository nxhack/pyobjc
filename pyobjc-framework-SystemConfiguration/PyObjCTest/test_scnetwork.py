from PyObjCTools.TestSupport import *

from SystemConfiguration import *
import socket, sys
def resolver_available():
    try:
        socket.gethostbyname('www.python.org')
        return True
    except socket.error:
        return False

class TestSCNetwork (TestCase):
    def testConstants(self):
        self.assertEqual(kSCNetworkFlagsTransientConnection, 1 << 0)
        self.assertEqual(kSCNetworkFlagsReachable, 1<<1)
        self.assertEqual(kSCNetworkFlagsConnectionRequired, 1<<2)
        self.assertEqual(kSCNetworkFlagsConnectionAutomatic, 1<<3)
        self.assertEqual(kSCNetworkFlagsInterventionRequired, 1<<4)
        self.assertEqual(kSCNetworkFlagsIsLocalAddress, 1<<16)
        self.assertEqual(kSCNetworkFlagsIsDirect, 1<<17)

    def testHardFunctionsNoHost(self):
        self.assertRaises(socket.gaierror, SCNetworkCheckReachabilityByAddress,
            ('no-such-host.objective-python.org', 80), objc._size_sockaddr_ip4, None)

    @onlyIf(resolver_available(), "No DNS resolver available")
    def testHardFunctions(self):
        b, flags = SCNetworkCheckReachabilityByAddress(
                ('www.python.org', 80), objc._size_sockaddr_ip4, None)
        self.assertIsInstance(b, bool)
        self.assertIsInstance(flags, (int, long))
        self.assertEqual(b, True)
        self.assertEqual(flags, kSCNetworkFlagsReachable)


    @onlyIf(resolver_available(), "No DNS resolver available")
    def testFunctions(self):
        r, flags = SCNetworkCheckReachabilityByName(b"www.python.org", None)
        self.assertTrue(r is True or r is False)
        self.assertTrue(isinstance(flags, (int, long)))

        r = SCNetworkInterfaceRefreshConfiguration("en0")
        self.assertTrue(r is True or r is False)


if __name__ == "__main__":
    main()
