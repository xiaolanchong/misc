# -*- coding: utf-8 -*-

import unittest
from viterbi import Viterbi
from node import Node
from dicttoken import Token
from runmecab import MecabOutputGetter
from writer import Writer

class MockConnector:
    def getCost(self, leftAttribute, rightAttribute):
        return leftAttribute * rightAttribute

class ViterbiTest(unittest.TestCase):
    def setUp(self):
        self.defaultText = '船が検疫所に着いたのは、朝の四時頃にちがいない。'

    #@unittest.skip("temp skipping")
    def testConnectNodeMutualCost(self):
        v = Viterbi()
        v.connector = MockConnector()
        bestNode = Node(Token('b', 12, 10, 0, 0, 5, 0))
        beginNodes = [Node(Token('a', 10, 15, 0, 0, 5, 0)),
                      bestNode,
                      Node(Token('c', 11, 11, 0, 0, 5, 0))]
        endNode = Node(Token('7', 10, 10, 0, 0, 5, 0))
        v.connect(beginNodes, endNode)
        self.assertEquals(endNode.leftNode, bestNode)

    #@unittest.skip("temp skipping")
    def testAnalyze(self):
        v = Viterbi()
        nodes = v.getBestPath(self.defaultText)
        writer = Writer()
        res = writer.getNodeText(v.getTokenizer(), nodes)
        self.assertEqual(['<BOS>', '船', 'が', '検疫', '所', 'に',
                          '着い', 'た', 'の', 'は', '、', '朝', 'の',
                          '四', '時', '頃', 'に', 'ちがい',
                          'ない', '。', '<EOS>'], res)

    def testRunMecab(self):
       # runner = MecabRunner()
       # res = runner.run(self.defaultText)
       # print(res)
       pass

    def testCompareMecab(self):
        v = Viterbi()
        nodes = v.getBestPath(self.defaultText)
        writer = Writer()
        pyResult = writer.getMecabOutput(v.getTokenizer(), nodes)
        runner = MecabOutputGetter()
        mecabResult = runner.run(self.defaultText)
        self.assertEqual(len(mecabResult), len(pyResult))
        for i in range(len(mecabResult)):
            self.assertEqual(mecabResult[i], pyResult[i])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ViterbiTest)
    unittest.TextTestRunner(verbosity=2).run(suite)