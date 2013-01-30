# -*- coding: utf-8 -*-

from mecab.dictionary import Dictionary
from mecab.charproperty import CharProperty
from mecab.token import Token
from mecab.node import Node

class Tokenizer:
    def __init__(self, loader):
        self.BOS_FEATURE = -1
        self.EOS_FEATURE = -2
        self.sysDictionary = Dictionary(loader, 'sys')
        self.unkDictionary = Dictionary(loader, 'unk')
        if self.sysDictionary.getCharSet() != 'euc-jp':
            raise RuntimeError('Unknown dictionary encoding: ' + self.sysDictionary.getCharSet())
        self.charProperties = CharProperty(loader, self.sysDictionary.getCharSet())
        self.spaceCharInfo = self.charProperties.getCharInfo(' ')

    def getFeature(self, featureId, isKnown):
        if isKnown:
            return self.sysDictionary.getFeature(featureId)
        else:
            return '' #return self.unkDictionary.getFeature(featureId)

    def seekToOtherCharType(self, text, charInfo):
        for i in range(len(text)):
            ch = self.charProperties.getCharInfo(text[i])
            if not charInfo.isKindOf(ch):
                return i, ch
        return len(text), charInfo

    def needSeizeMoreChars(self, text, startCharInfo):
        if startCharInfo.invoke:
            endToLookupPos, endToLookup = self.seekToOtherCharType(text, startCharInfo)
            return endToLookupPos != 0
        else:
            return False

    def lookUp(self, text, posInSentence):
        # skip leading spaces
        startToLookup, startCharInfo = self.seekToOtherCharType(text, self.spaceCharInfo)
        text = text[startToLookup:]
        posInSentence += startToLookup
        tokens = self.sysDictionary.commonPrefixSearch(text)
        if tokens and len(tokens):
            if not startCharInfo.canBeGrouped():
                return [Node(token, posInSentence) for token in tokens]
            else:
                wordFound = tokens[0].text
                endToLookupPos, endToLookup = self.seekToOtherCharType(text[len(wordFound):], startCharInfo)
                if endToLookupPos == 0:
                    # can't extend the tokens
                    return [Node(token, posInSentence) for token in tokens]
                else:
                    # extend the context and convert the found tokens to unknown ones
                    return self.getUnknownTokens(startCharInfo, text[0 : len(wordFound) + endToLookupPos], posInSentence)
        else:
            #unknown token
            endToLookupPos, endToLookup = self.seekToOtherCharType(text, startCharInfo)
            return self.getUnknownTokens(startCharInfo, text[0 : endToLookupPos], posInSentence)

    def getUnknownTokens(self, startCharInfo, tokenText, posInSentence):
        ch = startCharInfo.defaultType
        cat = self.charProperties.getCategories()[ch]
        tokens = self.unkDictionary.commonPrefixSearch(cat)
        nodes = [Node(token, posInSentence) for token in tokens]
        for node in nodes:
            node.token.text = tokenText
            node.isKnown = False
        return nodes

    def getBOSNode(self, bosPos):
        t = Token('', 0, 0, 0, 0, self.BOS_FEATURE, 0)
        return Node(t, bosPos)

    def getEOSNode(self, eosPos):
        t = Token('', 0, 0, 0, 0, self.EOS_FEATURE, 0)
        return Node(t, eosPos)

    def isEOSNode(self, node):
        return node.token.featureId == self.EOS_FEATURE

    def isBOSNode(self, node):
        return node.token.featureId == self.BOS_FEATURE