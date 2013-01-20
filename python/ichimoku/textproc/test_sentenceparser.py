# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from mecab.writer import WordInfo
from sentenceparser import SentenceParser

class SentenceParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = SentenceParser()

    def testSimple(self):
        res = self.parser.splitIntoWords('ですからあの人', lambda x: False)
        self.assertEquals(['ですから', 'あの', '人'], res)

    def testNoNounSuffixJoin(self):
        res = self.parser.splitIntoWords('船が検疫所に', lambda x: False)
        self.assertEquals(['船', 'が', '検疫', '所', 'に'], res)

    def testNounSuffixJoin(self):
        res = self.parser.splitIntoWords('船が検疫所に', lambda x: True)
        self.assertEquals(['船', 'が', '検疫所', 'に'], res)

    def testUnknownToken(self):
        res = self.parser.splitIntoWords('メグレは機関の止った瞬間', lambda x: True)
        self.assertEquals(['メグレ', 'は', '機関', 'の', '止るた', '瞬間'], res)

    def testTwoNounSuffixJoin(self):
        res = self.parser.splitIntoWords('朝の四時頃に', lambda x: True)
        self.assertEquals(['朝', 'の', '四時頃', 'に'], res)

    def testNaiFormAsEntireExpression(self):
        res = self.parser.splitIntoWords('朝ちがいない', lambda x: True)
        self.assertEquals(['朝', 'ちがいない'], res)

    def testTaForm(self):
        #dictionary
        res = self.parser.splitIntoWords('所に着いたのは', lambda x: False)
        self.assertEquals(['所', 'に', '着く', 'の', 'は'], res)

    def testTeIruForm(self):
        #dictionary
        res = self.parser.splitIntoWords('雨が降っていた', lambda x: False, True)
        self.assertEquals(['雨', 'が', '降る', 'いる'], res)

    def testMecabFailure(self):
        res = self.parser.splitIntoWords('すべてに滲み込み', lambda x: False)
        self.assertEquals(['すべて', 'に', '滲みる', '込み'], res)

    def testPyPort(self):
        parser = SentenceParser('..')
        res = parser.splitIntoWords('所に着いたのは', lambda x: False)
        self.assertEquals(['所', 'に', '着い', 'の', 'は'], res)

    def testTokenize2(self):
        parser = SentenceParser('..')
        res = parser.tokenize2('所に着いたのは', lambda x: False)
        expected = [ WordInfo('所', '所', 38, 'トコロ'),
                     WordInfo('に', 'に', 13, 'ニ'),
                     WordInfo('着い', '着く', 31, 'ツイ'),
                     WordInfo('た', 'た', 25, 'タ'),
                     WordInfo('の', 'の', 63, 'ノ'),
                     WordInfo('は', 'は', 16, 'ハ')
                   ]
        self.assertEquals(expected, res)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SentenceParserTest)
    unittest.TextTestRunner(verbosity=2).run(suite)