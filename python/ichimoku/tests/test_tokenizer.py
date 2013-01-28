# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('..'))
from mecab.tokenizer import Tokenizer
import mecab.partofspeech as PoS

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        sys = os.path.join('..', 'data', 'sys.zip')
        unk = os.path.join('..', 'data', 'unk.zip')
        chz = os.path.join('..', 'data', 'char.bin')
        mtx = os.path.join('..', 'data', 'matrix.bin')
        self.tokenizer = Tokenizer(sys, unk, chz)

    def testSkipingSpaces(self):
        nodes = self.tokenizer.lookUp(' ' * 3 + '少し', 4)
        self.assertEqual(5, len(nodes))
        self.assertEqual(4 + 3, nodes[0].startPos)
        self.assertEqual(4 + 3, nodes[1].startPos)

    def testNoTokenizeSymbols(self):
        nodes = self.tokenizer.lookUp('kana', 4)
        self.assertEqual(6, len(nodes))
        self.assertEqual(4 + 0, nodes[0].startPos)
        self.assertEqual('kana', nodes[0].token.text)

    def testGroupUnknown(self):
        nodes = self.tokenizer.lookUp('マール・ブランデーの壜', 0)
        self.assertEqual(6, len(nodes))
        self.assertEqual('マール・ブランデー', nodes[0].token.text)

    def testComma(self):
        nodes = self.tokenizer.lookUp('、', 0)
        self.assertEqual(2, len(nodes))
        self.assertEqual(PoS.NOUN_NUMERIC, nodes[0].token.partOfSpeechId)
        self.assertEqual(PoS.COMMA, nodes[1].token.partOfSpeechId)

    def testUnknownKana(self):
        #nodes = self.tokenizer.lookUp('ジーン・モーラ', 0)
        expected = 'ジーン・モーラ'
        nodes = self.tokenizer.lookUp(expected, 0)
        self.assertEqual(6, len(nodes))
        self.assertEqual(expected, nodes[0].token.text)

    def testUnknownKanji(self):
        #nodes = self.tokenizer.lookUp('ジーン・モーラ', 0)
        nodes = self.tokenizer.lookUp('四時頃に', 0)
        self.assertEqual(1, len(nodes[0].token.text))
        nodes = self.tokenizer.lookUp('時頃に', 0)
        self.assertEqual(1, len(nodes[0].token.text))
        nodes = self.tokenizer.lookUp('頃に', 0)
        self.assertEqual(1, len(nodes[0].token.text))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TokenizerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)