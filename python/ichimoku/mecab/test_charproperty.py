# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os.path
import unittest
import charproperty

class CharInfoTest(unittest.TestCase):
    def testCharCategories(self):
        prop = charproperty.CharProperty(os.path.join('..', 'data', 'char.bin'))
        self.assertEqual(['DEFAULT', 'SPACE', 'KANJI', 'SYMBOL',
                          'NUMERIC', 'ALPHA', 'HIRAGANA', 'KATAKANA',
                          'KANJINUMERIC', 'GREEK', 'CYRILLIC'], prop.getCategories())
        self.assertEqual(['SPACE'], prop.getCharCaterogies(' '))
        self.assertEqual(['NUMERIC'], prop.getCharCaterogies('1'))
        self.assertEqual(['ALPHA'], prop.getCharCaterogies('a'))
        self.assertEqual(['KANJI'], prop.getCharCaterogies('吗'))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CharInfoTest)
    unittest.TextTestRunner(verbosity=2).run(suite)