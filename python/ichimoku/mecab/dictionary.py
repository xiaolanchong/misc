# -*- coding: utf-8 -*-

import io
from struct import unpack, calcsize
from doublearray import DoubleArray
from dicttoken import Token

class Dictionary:
    def __init__(self, fileName):
        self.__charset = ''
        self.__tokens = []
        self.__featureBlob = None
        self.__dictionary = None
        self.loadFromBinary(fileName)

    def getFeatures(self):
        return self.__features

    def getTokens(self):
        return self.__tokens

    def loadFeatures(self, data):
        idx = 0
        while(idx <= len(data)):
            strEnd = data.find(b'\x00')
            if strEnd >= 0:
                feature = str(data[idx:strEnd], 'euc-jp')
                self.__features.append(feature)
                idx = strEnd + 1
            else:
                return

    def loadFromBinary(self, fileName):
        with open(fileName, 'rb') as dictFile:
            fmt = '<IIIIIIIIII'
            header = dictFile.read(calcsize(fmt))
            magic, version, dictType, lexSize, \
            leftSize, rightSize, dataSize, \
            tokenPartSize, featurePartSize, dummy = \
                unpack(fmt, header)
            if version != 102:
                raise RuntimeError('Incompatible dictionary version: {0}'.format(version))
            charSetBuffer, = unpack('32s', dictFile.read(32))
            self.__charset = str(charSetBuffer).rstrip('\x00')
            self.__dictionary = DoubleArray(dictFile.read(dataSize))
            #dictFile.seek(tokenPartSize, io.SEEK_CUR)
            self.loadTokens(dictFile, tokenPartSize)
            #self.loadFeatures(dictFile.read(featurePartSize))
            self.__featureBlob = dictFile.read(featurePartSize)


    def loadTokens(self, dictFile, tokenPartSize):
        fmt = 'HHHhII'
        tokenSize = calcsize(fmt)
        for i in range(tokenPartSize//tokenSize):
            data = dictFile.read(tokenSize)
            fields = unpack(fmt, data)
            self.__tokens.append(Token(*fields))

    def internalCommonPrefixSearch(self, text):
        encodedText = bytes(text, 'euc-jp')
        return self.__dictionary.commonPrefixSearch(encodedText)

    def commonPrefixSearch(self, text):
        encodedText = bytes(text, 'euc-jp')
        tokenStartIds = self.__dictionary.commonPrefixSearch(encodedText)
        tokens = []
        for tokenHanlder, tokenLength in tokenStartIds:
            tokenNum = tokenHanlder & 0xff
            tokenStartId = tokenHanlder >> 8
            for i in range(tokenNum):
                tokens.append(self.__tokens[tokenStartId + i])
        return tokens

    def getFeature(self, featureId):
        strEnd = self.__featureBlob.find(b'\x00', featureId)
        if strEnd >= 0:
            feature = str(self.__featureBlob[featureId:strEnd], 'euc-jp')
            return feature
        else:
            return None
