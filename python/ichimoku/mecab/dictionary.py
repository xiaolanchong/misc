# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import io
import sys
import os.path
from struct import unpack, calcsize
from mecab.doublearray import DoubleArray
from mecab.token import Token
from mecab.utils import text_type, extractString, isPy2x6
import mecab.compress as compress

class Dictionary:
    def __init__(self, fileName):
        self.charset = None
        self.tokenBlob = []
        self.featureBlob = None
        self.doubleArray = None
        if isPy2x6():
            #dictFile = compress.load(fileName)
            dictFile = open(fileName, mode='rb')
            self.loadFromBinary(dictFile)
        else:
            with compress.load(fileName) as dictFile:
                self.loadFromBinary(dictFile)

    def getToken(self, tokenId):
        fmt = str('HHHhII')
        tokenSize = calcsize(fmt)
        #NOTE: dictionary tokens don't store their texts,
        #      which are available either looking up the token features
        #      or during the parsing
        fields = unpack(fmt, self.tokenBlob[tokenId * tokenSize : (tokenId + 1) * tokenSize])
        return Token('', fields[0], fields[1], fields[2],
                         fields[3], fields[4], fields[5] )

    def loadFeatures(self, data):
        """
            Loads all features from the dictionary.
            Note: it's a time consuming function, only for service purposes
        """
        idx = 0
        while(idx <= len(data)):
            strEnd = data.find(b'\x00')
            if strEnd >= 0:
                feature = str(data[idx:strEnd], self.getCharSet())
                self.__features.append(feature)
                idx = strEnd + 1
            else:
                return

    def loadFromBinary(self, dictFile):
        """
            Loads the dictionary from the blob
        """
        fmt = str('<IIIIIIIIII')
        header = dictFile.read(calcsize(fmt))
        magic, version, dictType, lexSize, \
        leftSize, rightSize, dataSize, \
        tokenPartSize, featurePartSize, dummy = \
            unpack(fmt, header)
        if version != 102:
            raise RuntimeError('Incompatible dictionary version: {0}'.format(version))
        charSetBuffer, = unpack(str('32s'), dictFile.read(32))
        self.charset = extractString(charSetBuffer).lower()
        self.doubleArray = DoubleArray(dictFile.read(dataSize))
        self.tokenBlob = dictFile.read(tokenPartSize)
        self.featureBlob = dictFile.read(featurePartSize)


    def loadTokens(self, dictFile, tokenPartSize):
        fmt = str('HHHhII')
        tokenSize = calcsize(fmt)
        for i in range(tokenPartSize//tokenSize):
            data = dictFile.read(tokenSize)
            #NOTE: dictionary tokens don't store their texts,
            #      which are available either looking up the token features
            #      or during the parsing
            fields = unpack(fmt, data)
            self.__tokens.append(Token('', fields[0], fields[1], fields[2],
                                           fields[3], fields[4], fields[5] ))

    def internalCommonPrefixSearch(self, text):
        encodedText = bytearray(text, self.getCharSet())
        return self.doubleArray.commonPrefixSearch(encodedText)

    def commonPrefixSearch(self, text):
        """
        Looks up all words matching a part of the text starting from
        the beginning.
        E.g. 'abcd' produces 'a', 'ab' 'abc' given the latters are
        actual words
        """
        return self.internalSearch(text, self.doubleArray.commonPrefixSearch)

    def internalSearch(self, text, functionToMatch):
        tokens = []
        encodedText = bytearray(text, self.getCharSet())
        tokenStartIds = functionToMatch(encodedText)
        for tokenHandler, tokenLength in tokenStartIds:
            tokenNum = tokenHandler & 0xff
            tokenStartId = tokenHandler >> 8
            for i in range(tokenNum):
                d = self.getToken(tokenStartId + i)
                tokenText = text_type(bytes(encodedText[:tokenLength]), self.getCharSet())
                t = Token(tokenText, d.leftAttribute,
                          d.rightAttribute, d.partOfSpeechId,
                          d.wordCost, d.featureId, d.compound)
                tokens.append(t)
        return tokens

    def exactMatchSearch(self, text):
        """
            Looks up all words matching the text starting from
            the beginning.
            E.g. 'abcd' produces 'abcd'  given the latter is an existing word.
        """
        return self.internalSearch(text, self.doubleArray.exactMatchSearch)

    def getCharSet(self):
        """
            Gets the dictionary charset: euc-jp, utf-8, etc.
        """
        return self.charset

    def getFeature(self, featureId):
        """
            Gets the dictionary entry for the word
        """
        strEnd = self.featureBlob.find(b'\x00', featureId)
        if strEnd >= 0:
            feature = text_type(self.featureBlob[featureId:strEnd], self.getCharSet())
            return feature
        else:
            return None
