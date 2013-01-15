# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
import dictionary

class DictionaryTest(unittest.TestCase):
    def testSingleWord(self):
        path = os.path.join('..', 'data', 'dict.sqlite')
        dict = dictionary.Dictionary(path)
        reading, definition = dict.getReadingAndDefinition("大好き")
        self.assertEqual(reading, "だいすき")
        self.assertEqual(definition, "(adj-na) loveable/very likeable/like very much/(P)")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DictionaryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)