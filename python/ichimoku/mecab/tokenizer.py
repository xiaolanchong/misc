# -*- coding: utf-8 -*-

from mecab.dictionary import Dictionary
from mecab.charproperty import CharProperty
from mecab.dicttoken import Token
from mecab.node import Node

class Tokenizer:
    def __init__(self, sysDictFileName, unkDictFileName, charPropFileName):
        self.BOS_FEATURE = -1
        self.EOS_FEATURE = -2
        self.sysDictionary = Dictionary(sysDictFileName)
        self.unkDictionary = Dictionary(unkDictFileName)
        if self.sysDictionary.getCharSet() != 'euc-jp':
            raise RuntimeError('Unknown dictionary encoding: ' + self.sysDictionary.getCharSet())
        self.charProperties = CharProperty(charPropFileName, self.sysDictionary.getCharSet())

    def getFeature(self, featureId, isKnown):
        if isKnown:
            return self.sysDictionary.getFeature(featureId)
        else:
            return '' #return self.unkDictionary.getFeature(featureId)

    def lookUp(self, text):
        #TODO: skip spaces (CharInof(' '))
        tokens = self.sysDictionary.commonPrefixSearch(text)
        if tokens and len(tokens):
            return [Node(token) for token in tokens]
        else:
            #unknown token
            #TODO: join the same class chars in the single token
            charInfo = self.charProperties.getCharInfo(text[0])
            ch = charInfo.defaultType
            cat = self.charProperties.getCategories()[ch]
            tokens = self.unkDictionary.commonPrefixSearch(cat)
            nodes = [Node(token) for token in tokens]
            for node in nodes:
                node.token.text = text[0]
                node.isKnown = False
            return nodes

            #return [Node.createUnknownNode(text[0])]


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