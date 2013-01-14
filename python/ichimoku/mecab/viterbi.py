# -*- coding: utf-8 -*-

import sys
from tokenizer import Tokenizer
from connector import Connector
from node import Node

class Viterbi:
    def __init__(self):
        self.tokenizer = Tokenizer('test/sys.dic', 'test/unk.dic', 'test/char.bin')
        self.connector = Connector('test/matrix.bin')

    def getTokenizer(self):
        return self.tokenizer

    def getBestPath(self, text):
        endNodes = [[] for i in range(len(text) + 1)]
        bosNode = self.tokenizer.getBOSNode()
        endNodes[0] = [bosNode]
        for pos in range(len(text)):
            if len(endNodes[pos]) > 0:
                nodes = self.tokenizer.lookUp(text[pos:])
                for node in nodes:
                    self.connect(endNodes[pos], node)
                    endNodes[pos + len(node.token.text)].append(node)
        eosNode = self.tokenizer.getEOSNode()
        self.connect(endNodes[-1], eosNode)
        return Viterbi.createBackwardPath(eosNode)

    def connect(self, beginNodes, endNode):
        bestNode = None
        bestCost = sys.maxsize
        bestNodeConnection = 0
        for beginNode in beginNodes:
            if True: # beginNode.isKnown and endNode.isKnown:
                connectionCost = self.connector.getCost(beginNode.token.rightAttribute,
                                                    endNode.token.leftAttribute)
                totalCost = beginNode.totalCost + endNode.token.wordCost + connectionCost
            else:
                totalCost = beginNode.totalCost
            if totalCost < bestCost:
                bestCost = totalCost
                bestNode = beginNode
                bestNodeConnection = connectionCost
        if bestNode:
            Node.connect(bestNode, endNode, bestNodeConnection, bestCost)

    def createBackwardPath(endNode):
        beginNode = endNode
        path = []
        while(endNode):
            path.append(endNode)
            endNode = endNode.leftNode
        path.reverse()
        return path


