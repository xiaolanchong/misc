# -*- coding: utf-8 -*-

import io
from struct import unpack, calcsize
from doublearray import DoubleArray
from dicttoken import Token
import utils

class Dictionary:
    def __init__(self, fileName):
        self.__charset = ''
        self.tokenBlob = []
        self.featureBlob = None
        self.doubleArray = None
        self.loadFromBinary(fileName)

    def getToken(self, tokenId):
        fmt = 'HHHhII'
        tokenSize = calcsize(fmt)
        #NOTE: dictionary tokens don't store their texts,
        #      which are available either looking up the token features
        #      or during the parsing
        fields = unpack(fmt, self.tokenBlob[tokenId * tokenSize : (tokenId + 1) * tokenSize])
        return Token('', fields[0], fields[1], fields[2],
                         fields[3], fields[4], fields[5] )

##    def loadFeatures(self, data):
##        idx = 0
##        while(idx <= len(data)):
##            strEnd = data.find(b'\x00')
##            if strEnd >= 0:
##                feature = str(data[idx:strEnd], self.getCharSet())
##                self.__features.append(feature)
##                idx = strEnd + 1
##            else:
##                return

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
            self.__charset = utils.extractString(charSetBuffer).lower()
            self.doubleArray = DoubleArray(dictFile.read(dataSize))
            #dictFile.seek(tokenPartSize, io.SEEK_CUR)
            self.tokenBlob = dictFile.read(tokenPartSize)
            #self.loadFeatures(dictFile.read(featurePartSize))
            self.featureBlob = dictFile.read(featurePartSize)


    def loadTokens(self, dictFile, tokenPartSize):
        fmt = 'HHHhII'
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
        encodedText = bytes(text, self.getCharSet())
        return self.doubleArray.commonPrefixSearch(encodedText)

    def commonPrefixSearch(self, text):
       # encodedText = bytes(text, self.getCharSet())
       # tokenStartIds = self.doubleArray.commonPrefixSearch(encodedText)
        tokenStartIds = self.internalCommonPrefixSearch(text)
        tokens = []
        for tokenHandler, tokenLength in tokenStartIds:
            #TODO: this a hack euc-jp (2 byte) -> unicode (1 char)
            assert(tokenLength % 2 == 0)
            tokenLength //= 2
            tokenNum = tokenHandler & 0xff
            tokenStartId = tokenHandler >> 8
            for i in range(tokenNum):
                d = self.getToken(tokenStartId + i)
                t = Token(text[:tokenLength], d.leftAttribute,
                          d.rightAttribute, d.partOfSpeechId,
                          d.wordCost, d.featureId, d.compound)
                tokens.append(t)
        return tokens

    def getCharSet(self):
        return self.__charset

    def getFeature(self, featureId):
        strEnd = self.featureBlob.find(b'\x00', featureId)
        if strEnd >= 0:
            feature = str(self.featureBlob[featureId:strEnd], self.getCharSet())
            return feature
        else:
            return None
