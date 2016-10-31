import unittest
import ConfigAccessor

class makePathTest(unittest.TestCase):
    def testNoParameters(self):
        self.assertEqual(ConfigAccessor._makePath(), "")

    def testOneParameter(self):
        self.assertEqual(ConfigAccessor._makePath("one"), "one")

    def testManyParameters(self):
        self.assertEqual(ConfigAccessor._makePath("one", "two", "three"), "one/two/three")

    def testParametersWithSlashes(self):
        self.assertEqual(ConfigAccessor._makePath("one/", "/two", "/three/"), "one/two/three")

    def testParametersWithBackslashes(self):
        self.assertEqual(ConfigAccessor._makePath("one\\", "\\two", "\\three\\"), "one/two/three")
