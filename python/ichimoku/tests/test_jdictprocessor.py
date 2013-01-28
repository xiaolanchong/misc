# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('..'))
from textproc.jdictprocessor import JDictProcessor
from textproc.dartsdict import DartsDictionary
import mecab.partofspeech as PoS
from mecab.writer import WordInfo

class JDictProcessorTest(unittest.TestCase):
    def setUp(self):
        dictionary = DartsDictionary(os.path.join('..', 'data', 'jdict.zip'))
        self.processor = JDictProcessor(dictionary)

    def testDifferentReadingsSameWord(self):
        """
        新所帯|||あらじょたい|||(n) new household/new home
        新所帯|||しんじょたい|||(n) new household/new home
        新所帯|||しんしょたい|||(n) new household/new home
        """
        pass

    def testJoinReadings(self):
        """
        大君|||たいくん|||(n) liege lord/shogunate
        大君|||おおきみ|||(n) emperor/king/prince
        大君|||おおぎみ|||(n) emperor/king/prince
        """

    def testRemovePartitialDuplicates(self):
        """
        黒桧|||くろべ|||(n,uk) Japanese arborvitae (Thuja standishii)
        黒桧|||くろび|||(n,uk) Japanese arborvitae (Thuja standishii)
        黒桧|||くろべ|||黒桧 [クロベ] /(n,uk) Japanese arborvitae (Thuja standishii)/
        """

    def testBestChoice(self):
        definitions = \
        [( 'に', '(n) load/baggage/cargo/freight/goods/burden/responsibility/(P)'),
         ( 'に', '(suf) takes after (his mother)'),
         ( 'に', '(n) red earth (i.e. containing cinnabar or minium)/vermilion)'),
         ( 'に', '(num) two/(P)'),
         ( 'に', '(prt) indicates such things as location of person or thing, location of short-term action, etc./(P)')]
        res = self.processor.getBestAlternative(definitions, PoS.PRT_CASE)
        self.assertEqual(definitions[-1], res)

    def testEqualMatch(self):
        definitions = \
        [ ('着く', '(v5k) to arrive at/to reach/to sit on/to sit at (e.g. the table)/(P)'),
          ('着く', '(v5k,vt) to put on (or wear) lower-body clothing ')
        ]
        res = self.processor.getBestAlternative(definitions, PoS.VERB)
        self.assertEqual(definitions[0], res)

    def testMergeNoun(self):
        a = WordInfo( '検疫', 0, '検疫', PoS.NOUN_VSURU, 'xx')
        b = WordInfo( '所', 2, '所', PoS.NOUN_SUFFIX, 'xx')
        newWord = self.processor.mergeWord(a, b)
        expected = WordInfo('検疫所', 0, '検疫所' , PoS.NOUN, 'けんえきじょ')
        self.assertEqual(newWord, expected)

    def testMergeNoun3Kanji(self):
        a = WordInfo( '数', 0, '数', PoS.NOUN_VSURU, 'xx')
        b = WordInfo( '時間', 1, '時間', PoS.NOUN_SUFFIX, 'xx')
        newWord = self.processor.mergeWord(a, b)
        expected = WordInfo('数時間', 0, '数時間' , PoS.NOUN, 'すうじかん')
        self.assertEqual(newWord, expected)

    def testMergeNoun4Kanji(self):
        a = WordInfo( '予算', 0, '予算', PoS.NOUN, 'xx')
        b = WordInfo( '補正', 2, '補正', PoS.NOUN, 'xx')
        newWord = self.processor.mergeWord(a, b)
       # expected = WordInfo('補正予算', 0, '補正予算' , PoS.NOUN, 'すうじかん')
        self.assertIsNone(newWord)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(JDictProcessorTest)
    unittest.TextTestRunner(verbosity=2).run(suite)