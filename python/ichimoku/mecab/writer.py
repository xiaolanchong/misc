# -*- coding: utf-8 -*-

from node import Node
from dicttoken import Token

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
            featureStr = tokenizer.getFeature(node.token.featureId)
            featureStr = featureStr.split(',')
            nodeInfo.append(text)
            nodeInfo.append(featureStr[6])
            nodeInfo.append(str(node.token.partOfSpeechId))
            nodeInfo.append(str(node.token.wordCost))
            nodeInfo.append(str(node.connectionCost))
            nodeInfo.append(str(node.totalCost))
            nodeInfo.append(str(node.token.leftAttribute))
            nodeInfo.append(str(node.token.rightAttribute))
            res.append(nodeInfo)
            prevNodeCost = node.totalCost
        return res