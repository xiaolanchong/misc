# -*- coding: utf-8 -*-

from dictionary import Dictionary
from charproperty import CharProperty
from dicttoken import Token
from node import Node

class Tokenizer:
    def __init__(self, dictFileName, charPropFileName):
        self.BOS_FEATURE = -1
        self.EOS_FEATURE = -2
        self.dictionary = Dictionary(dictFileName)
        if self.dictionary.getCharSet() != 'euc-jp':
            raise RuntimeError('Unknown dictionary encoding: ' + self.dictionary.getCharSet())
        self.charProperties = CharProperty(charPropFileName, self.dictionary.getCharSet())

    def getFeature(self, featureId):
        return self.dictionary.getFeature(featureId)

    def lookUp(self, text):
        #TODO: skip spaces (CharInof(' '))
        tokens = self.dictionary.commonPrefixSearch(text)
        return [Node(token) for token in tokens]

    def getBOSNode(self):
        t = Token('', 0, 0, 0, 0, self.BOS_FEATURE, 0)
        return Node(t)

    def getEOSNode(self):
        t = Token('', 0, 0, 0, 0, self.EOS_FEATURE, 0)
        return Node(t)

    def isEOSNode(self, node):
        return node.token.featureId == self.EOS_FEATURE
    def isBOSNode(self, node):
        return node.token.featureId == self.BOS_FEATURE