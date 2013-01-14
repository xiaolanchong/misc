# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import utils

class UtilsTest(unittest.TestCase):
    def testExtractString(self):
        res = utils.extractString(b'sample\x00\x00\x00')
        self.assertEqual('sample', res)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UtilsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)