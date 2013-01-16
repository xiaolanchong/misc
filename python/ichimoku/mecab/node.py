# -*- coding: utf-8 -*-

from mecab.dicttoken import Token

class Node:
    def __init__(self, token):
        self.leftNode = None
        self.rightNode = None
        self.totalCost = 0
        self.token = token
        self.connectionCost = 0
        self.isKnown = True

    def createUnknownNode(text):
        t = Token(text, 0, 0, 0, 0, 0, 0)
        return Node(t)

    def connect(left, right, connectionCost, totalCost):
        assert(left)
        assert(right)
        left.rightNode = right
        right.leftNode = left
        right.totalCost = totalCost
        right.connectionCost = connectionCost

    def __repr__(self):
        return 'token: [{0}], totalCost: {1}'.format(self.token, self.totalCost)