# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
import sys
sys.path.append(os.path.abspath('..'))
from mecab.viterbi import Viterbi
from mecab.node import Node
from mecab.token import Token
from mecab.runmecab import MecabOutputGetter
from mecab.writer import Writer
from textproc.dataloader import getDataLoader

class MockConnector:
    def getCost(self, leftAttribute, rightAttribute):
        return leftAttribute * rightAttribute

class ViterbiTest(unittest.TestCase):
    def setUp(self):
        self.defaultText = '船が検疫所に着いたのは、朝の四時頃にちがいない。'
        self.viterbi = Viterbi(getDataLoader())

    #@unittest.skip("temp skipping")
    def testConnectNodeMutualCost(self):
        self.viterbi.connector = MockConnector()
        bestNode = Node(Token('b', 12, 10, 0, 0, 5, 0), 0)
        beginNodes = [Node(Token('a', 10, 15, 0, 0, 5, 0), 0),
                      bestNode,
                      Node(Token('c', 11, 11, 0, 0, 5, 0), 0)]
        endNode = Node(Token('7', 10, 10, 0, 0, 5, 0), 0)
        self.viterbi.connect(beginNodes, endNode)
        self.assertEquals(endNode.leftNode, bestNode)

    #@unittest.skip("temp skipping")
    def testAnalyze(self):
        nodes = self.viterbi.getBestPath(self.defaultText)
        writer = Writer()
        res = writer.getNodeText(self.viterbi.getTokenizer(), nodes)
        self.assertEqual(['<BOS>', '船', 'が', '検疫', '所', 'に',
                          '着い', 'た', 'の', 'は', '、', '朝', 'の',
                          '四', '時', '頃', 'に', 'ちがい',
                          'ない', '。', '<EOS>'], res)

    #@unittest.skip("temp skipping")
    def testCompareMecabWithOneSentence(self):
        self.compareOneSentence(self.defaultText)

    def testNoneToken(self):
        expr = '船客の大部分はまだ眠っていた。' # FAILS !!!
        self.compareOneSentence(expr)

    def testUnknownNode(self):
        expr = 'すべてに滲《し》み込み'
        self.compareOneSentence(expr)

    def compareOneSentence(self, expr):
        nodes = self.viterbi.getBestPath(expr)
        writer = Writer()
        pyResult = writer.getMecabOutput(self.viterbi.getTokenizer(), nodes)
        runner = MecabOutputGetter()
        mecabResult = runner.run(expr)
       # print(pyResult)
      #  print(mecabResult)
        self.assertEqual(len(mecabResult), len(pyResult))
        for i in range(len(mecabResult)):
            self.assertEqual(mecabResult[i], pyResult[i])


    def out(text, mecabOutput, pyOutput):
        z = text + ' | ' + str(pyResult) + str(mecabResult)

   # @unittest.skip("temp skipping")
    def testEntireFile(self):
        writer = Writer()
        runner = MecabOutputGetter()
        return
        with open(r'test/MaigraitInNewYork_ch1.txt', 'r', encoding='utf-8') as inFile:
            for line in inFile.readlines():
                text = line.strip()
                nodes = self.viterbi.getBestPath(text)
                pyResult = writer.getMecabOutput(self.viterbi.getTokenizer(), nodes)

                mecabResult = runner.run(text)
                self.assertEqual(len(mecabResult), len(pyResult),  text + ' | ' + str(pyResult) + str(mecabResult))  #text)
                for i in range(len(mecabResult)):
                    self.assertEqual(mecabResult[i], pyResult[i])



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ViterbiTest)
    unittest.TextTestRunner(verbosity=2).run(suite)