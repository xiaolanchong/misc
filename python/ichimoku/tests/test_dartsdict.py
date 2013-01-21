# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
import sys
sys.path.append(os.path.abspath('..'))
from textproc import dartsdict

class DartsDictionaryTest(unittest.TestCase):
    def setUp(self):
        self.dictionary = dartsdict.DartsDictionary('../data/jdict.zip')

    def testRecord(self):
        reading, entry = self.dictionary.getFirstReadingAndDefinition('開扉')
        self.assertEqual('かいひ', reading)
        self.assertEqual('(n,vs) opening a door', entry)

    def testDuplicatedRecord(self):
        reading, entry = self.dictionary.getFirstReadingAndDefinition('々')
        self.assertEqual('くりかえし', reading)
        self.assertEqual('(n) repetition of kanji (sometimes voiced)', entry)

    def testNoSuchWord(self):
        reading, entry = self.dictionary.getFirstReadingAndDefinition('メグレ')
        self.assertIsNone(reading)
        self.assertIsNone(entry)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DartsDictionaryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)