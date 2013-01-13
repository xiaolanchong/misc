# -*- coding: utf-8 -*-

import unittest
import dictionary

class DictionaryTest(unittest.TestCase):
    def testSingleWord(self):
        dict = dictionary.Dictionary()
        reading, definition = dict.getReadingAndDefinition("大好き")
        self.assertEqual(reading, "だいすき")
        self.assertEqual(definition, "(adj-na) loveable/very likeable/like very much/(P)")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DictionaryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)