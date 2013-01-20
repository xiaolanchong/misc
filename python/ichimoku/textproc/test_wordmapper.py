# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
from wordmapper import WordMapper
from mecab import partofspeech as PoS

class WordMapperTest(unittest.TestCase):
    def setUp(self):
        self.mapper = WordMapper()

    def testMatchNoun(self):
        self.assertTrue(self.mapper.match(['n'], PoS.NOUN))
        self.assertFalse(self.mapper.match(['vi'], PoS.NOUN))
        self.assertFalse(self.mapper.match(['vi'], PoS.NOUN))
        self.assertFalse(self.mapper.match(['n'], PoS.NOUN_VSURU))
        self.assertTrue(self.mapper.match(['vs'], PoS.NOUN_VSURU))
        #self.assertTrue(self.)

    def testMatchVerb(self):
        self.assertTrue(self.mapper.match(['vi'], PoS.VERB))
        self.assertFalse(self.mapper.match(['vs'], PoS.VERB))
        #self.assertTrue()

    def testMatchAdjective(self):
        pass

    def testSuffix(self):
        self.assertFalse(self.mapper.match(['suf', 'uk', 'n'], PoS.NOUN_SUFFIX))
        self.assertFalse(self.mapper.match(['suf', 'ctr'], PoS.NOUN_SUFFIX))

    def testTaAuxillary(self):
        taWords = [{'pref', 'n'}, {'ok', 'adj-no', 'pn'}, {'n'},
                   {'adj-no', 'n-adv', 'n'}, {'arch', 'ctr', 'n-suf', 'n'},
                   {'aux-v'}]
        self.assertEqual(5, self.mapper.selectBestWord(taWords, PoS.VERB_AUX))

    def testParticle(self):
        self.assertEqual(1, self.mapper.selectBestWord([{'n'}, {'prt'}], PoS.PRT_CASE))
        self.assertEqual(1, self.mapper.selectBestWord([{'suf'}, {'conj', 'int'}], PoS.PRT_CASE))
        self.assertEqual(2, self.mapper.selectBestWord([['n'], {'suf', 'n'}, {'adv', 'prt'}], PoS.PRT_CASE))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(WordMapperTest)
    unittest.TextTestRunner(verbosity=2).run(suite)