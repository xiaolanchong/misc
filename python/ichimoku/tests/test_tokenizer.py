# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('..'))
from mecab.tokenizer import Tokenizer
import mecab.partofspeech as PoS
from textproc.dataloader import getDataLoader

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer(getDataLoader())

    def testSkipingSpaces(self):
        nodes = self.tokenizer.lookUp(' ' * 3 + '少し', 4)
        self.assertEqual(5, len(nodes))
        self.assertEqual('少', nodes[0].token.text)
        self.assertEqual(4 + 3, nodes[0].startPos)
        self.assertEqual(4 + 3, nodes[1].startPos)

    def testWhiteSpaces(self):
        nodes = self.tokenizer.lookUp('\n少し', 4)
        self.assertEqual(5, len(nodes))
        self.assertEqual('少', nodes[0].token.text)
        self.assertEqual(4 + 1, nodes[0].startPos)
        self.assertEqual(4 + 1, nodes[1].startPos)

    def testFindNonSpace(self):
        pos = self.tokenizer.findNonSpacePosition('少し')
        self.assertEqual(0, pos)
        pos = self.tokenizer.findNonSpacePosition('')
        self.assertEqual(0, pos)
        pos = self.tokenizer.findNonSpacePosition('  少し')
        self.assertEqual(2, pos)
        pos = self.tokenizer.findNonSpacePosition('\n  \t少し')
        self.assertEqual(4, pos)

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

    def testBracket(self):
        nodes = self.tokenizer.lookUp('」', 0)
        self.assertEqual(1, len(nodes))

    def testUnknownKana(self):
        #nodes = self.tokenizer.lookUp('ジーン・モーラ', 0)
        expected = 'ジーン・モーラ'
        nodes = self.tokenizer.lookUp(expected, 0)
        self.assertEqual(7, len(nodes))
        self.assertEqual('ジーン', nodes[0].token.text)
        self.assertEqual(expected, nodes[1].token.text)

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