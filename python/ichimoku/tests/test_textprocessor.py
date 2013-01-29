# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
import sys
sys.path.append(os.path.abspath('..'))
from textproc.textprocessor import TextProcessor, Settings
from mecab.writer import WordInfo

class TextProcessorTest(unittest.TestCase):
    def setUp(self):
        zzz = os.path.dirname(__file__)
        zzz = os.path.dirname(zzz)
        self.textProc = TextProcessor(os.path.join('..', 'data', 'jdict.zip'), zzz)

    def testDumpAll(self):
        res = self.textProc.do('船が検疫所に着いたのは', Settings.All())
        res = list(res)
        expected = \
        [
        ('船', 'ふね', '(n,n-suf,ctr) ship/boat/watercraft/vessel/steamship/tank/tub/vat/trough/counter for boat-shaped containers (e.g. of sashimi)/(P)', '船が検疫所に着いたのは'),
        ('が', 'が', '(prt,conj) indicates sentence subject (occasionally object)/indicates possessive (esp. in literary expressions)/but/however/still/and/(P)', '船が検疫所に着いたのは'),
        ('検疫', 'けんえき', '(n,vs) quarantine/medical inspection', '船が検疫所に着いたのは'),
        ('所', 'しょ', "(suf,ctr) counter for places", '船が検疫所に着いたのは'),
        ('に', 'に', '(prt) indicates such things as location of person or thing, location of short-term action, etc./(P)', '船が検疫所に着いたのは'),
        ('着く', 'つく', '(v5k) to arrive at/to reach/to sit on/to sit at (e.g. the table)/(P)', '船が検疫所に着いたのは'),
        ('た', 'た', '(aux-v) indicate past completed or action/indicates light imperative', '船が検疫所に着いたのは'),
        ('の', 'の', '(prt,fem) indicates possessive/nominalizes verbs and adjectives/substitutes for "ga" in subordinate phrases/(at sentence-end, falling tone) indicates a confident conclusion/(P)', '船が検疫所に着いたのは'),
        ('は', 'は', '(prt) topic marker particle/indicates contrast with another option (stated or unstated)/adds emphasis/(P)', '船が検疫所に着いたのは')
        ]
        #        self.assertEqual(len(expected), len(res))
        self.assertEqual(expected, res)

    def testNoKanji(self):
        self.assertFalse(TextProcessor.hasKanji('が'))
        self.assertTrue(TextProcessor.hasKanji('所'))
        self.assertFalse(TextProcessor.hasKanji('。'))

    def testMinimalMode(self):
        res = self.textProc.do('船が、検疫所に着いたのは', Settings.Minimal())
        res = list(res)
        expected = \
        [
        ('船', 'ふね', '(n,n-suf,ctr) ship/boat/watercraft/vessel/steamship/tank/tub/vat/trough/counter for boat-shaped containers (e.g. of sashimi)/(P)', '船が、検疫所に着いたのは'),
        ('が', '', '(prt,conj) indicates sentence subject (occasionally object)/indicates possessive (esp. in literary expressions)/but/however/still/and/(P)', '船が、検疫所に着いたのは'),
        ('検疫', 'けんえき', '(n,vs) quarantine/medical inspection', '船が、検疫所に着いたのは'),
        ('所', 'しょ', "(suf,ctr) counter for places", '船が、検疫所に着いたのは'),
        ('に', '', '(prt) indicates such things as location of person or thing, location of short-term action, etc./(P)', '船が、検疫所に着いたのは'),
        ('着く', 'つく', '(v5k) to arrive at/to reach/to sit on/to sit at (e.g. the table)/(P)', '船が、検疫所に着いたのは'),
        ('た', '', '(aux-v) indicate past completed or action/indicates light imperative', '船が、検疫所に着いたのは'),
        ('の', '', '(prt,fem) indicates possessive/nominalizes verbs and adjectives/substitutes for "ga" in subordinate phrases/(at sentence-end, falling tone) indicates a confident conclusion/(P)', '船が、検疫所に着いたのは'),
        ('は', '', '(prt) topic marker particle/indicates contrast with another option (stated or unstated)/adds emphasis/(P)', '船が、検疫所に着いたのは')
        ]
        #        self.assertEqual(len(expected), len(res))
        self.assertEqual(expected, res)

    def testUnknownWord(self):
        res = self.textProc.do('デッキに昇って行った')
        res = list(res)
        self.assertEqual(6, len(res))
        self.assertEqual('デッキ', res[0][0])
      #  for word, reading, definition, sentence in res:
      #      print(word, reading ,definition)

    def testGetContext(self):
        snt = 'デッキに昇って行った'
        res = self.textProc.getContext(snt, WordInfo('デ', 0, '', 0, '') )
        self.assertEqual(snt, res)

    def testExtentionOfUnknownToken(self):
        res = self.textProc.do('ジーン・モーラの姿は見えなかった。')
        res = list(res)
        self.assertEqual(7, len(list(res)))
        self.assertEqual('ジーン・モーラ', res[0][0])

    def testONReading(self):
        res = self.textProc.do('数時間が')
        res = list(res)
        self.assertEqual(3, len(list(res)))
        self.assertEqual('すう', res[0][1])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TextProcessorTest)
    unittest.TextTestRunner(verbosity=2).run(suite)