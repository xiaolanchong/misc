# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from mecab.node import Node
from mecab.dicttoken import Token

class WordInfo:
    def __init__(self, word, dictionaryForm, partOfSpeech, kana):
        self.word = word
        self.dictionaryForm = dictionaryForm
        self.partOfSpeech = partOfSpeech
        self.kana = kana

    def __repr__(self):
        return '({0}, {1}, {2}, {3})'.format(self.word, self.dictionaryForm,
                                            self.partOfSpeech, self.kana)

    def __eq__(self, other):
        return  self.word == other.word and \
                self.dictionaryForm == other.dictionaryForm and \
                self.partOfSpeech == other.partOfSpeech and \
                self.kana == other.kana

    def __neq__(self, other):
        return not self.__eq__(other)

class Writer:
    def __init__(self):
        pass

    def getNodeText(self, tokenizer, path):
        nodeText = []
        for node in path:
            if tokenizer.isBOSNode(node):
                text = '<BOS>'
            elif tokenizer.isEOSNode(node):
                text = '<EOS>'
            else:
                text = node.token.text
            nodeText.append(text)
        return nodeText

    def getMecabOutput(self, tokenizer, path):
        res = []
        prevNodeCost = 0
        for node in path:
            nodeInfo = []
            if tokenizer.isBOSNode(node) or \
               tokenizer.isEOSNode(node):
                continue
            else:
                text = node.token.text
            featureStr = tokenizer.getFeature(node.token.featureId, node.isKnown)
            featureStr = featureStr.split(',')
            nodeInfo.append(text)
            nodeInfo.append(featureStr[6] if len(featureStr) >= 7 else '')
            nodeInfo.append(str(node.token.partOfSpeechId))
            nodeInfo.append(str(node.token.wordCost))
            nodeInfo.append(str(node.connectionCost))
            nodeInfo.append(str(node.totalCost))
            nodeInfo.append(str(node.token.leftAttribute))
            nodeInfo.append(str(node.token.rightAttribute))
            res.append(nodeInfo)
            prevNodeCost = node.totalCost
        return res

    def getMorphAndFeature(self, tokenizer, path):
        out =[]
        for node in path:
            if tokenizer.isBOSNode(node) or \
               tokenizer.isEOSNode(node):
                continue
            text = node.token.text
            featureStr = tokenizer.getFeature(node.token.featureId, node.isKnown)
            featureStr = featureStr.split(',')
            padding = ['' for i in range(0 if len(featureStr) >= 7 else 7 - len(featureStr))]
            out.append([text] + featureStr + padding)
        return out

    def getWordInfo(self, tokenizer, path):
        out =[]
        for node in path:
            if tokenizer.isBOSNode(node) or \
               tokenizer.isEOSNode(node):
                continue
            text = node.token.text
            featureStr = tokenizer.getFeature(node.token.featureId, node.isKnown)
            featureStr = featureStr.split(',')
           # print(featureStr[7], featureStr[8], featureStr[9] if len(featureStr) >= 10 else '')
            out.append(WordInfo(text, self.getItemOrEmptyStr(featureStr, 6),
                                node.token.partOfSpeechId, self.getItemOrEmptyStr(featureStr, 7)))
        return out

    def getItemOrEmptyStr(self, arr, index):
        return arr[index] if len(arr) > index else ''
