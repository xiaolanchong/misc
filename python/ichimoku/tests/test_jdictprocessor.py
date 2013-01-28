# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('..'))
from textproc.jdictprocessor import JDictProcessor
import mecab.partofspeech as PoS

class JDictProcessorTest(unittest.TestCase):
    def setUp(self):
        self.processor = JDictProcessor()

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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(JDictProcessorTest)
    unittest.TextTestRunner(verbosity=2).run(suite)