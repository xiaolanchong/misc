# -*- coding: utf-8 -*-
from struct import unpack
import utils

class CharInfo:
    def __init__(self, type, defaultType, length, group, invoke):
        self.type = type
        self.defaultType = defaultType
        self.length = length
        self.group = group
        self.invoke= invoke

    def isKindOf(self, charInfo):
        return type & charInfo.type

    def isInCategory(self, categoryId):
        return self.type & (1 << categoryId)

    def __repr__(self):
        return 'type:{0}, defaultType:{1}, length:{2}, group:{3}, invoke:{4}'.format(
                 self.type, self.defaultType, self.length,
                 self.group, self.invoke)

class CharProperty:
    def __init__(self, file, encoding='euc-jp'):
        self.__map = []
        self.__categories = []
        self.loadFromBinary(file, encoding)

    def loadFromBinary(self, fileName, encoding):
        with open(fileName, 'rb') as inFile:
            uintSize = 4
            categoryBuffer = 32
            categoryNum, = unpack('<I', inFile.read(uintSize))
            calcFileSize = uintSize + categoryBuffer * categoryNum + uintSize * 0xffff
            for i in range(categoryNum):
                categoryStr, = unpack(str(categoryBuffer) + 's', inFile.read(categoryBuffer))
                self.__categories.append( utils.extractString(categoryStr, encoding))
            for i in range(0xffff):
                packedCharInfo, = unpack('<I', inFile.read(uintSize))
                charInfo = CharInfo( (packedCharInfo      ) & 0x3FFFF,
                                     (packedCharInfo >> 18) & 0xFF,
                                     (packedCharInfo >> 26) & 0xF,
                                     (packedCharInfo >> 30) & 0x1,
                                     (packedCharInfo >> 31) & 0x1)
                self.__map.append(charInfo)

    def getCategories(self):
        return self.__categories


    def getCharInfo(self, char):
        return self. __map[ord(char)]

    def getCharCaterogies(self, char):
        char = self.getCharInfo(char)
        categoryNames = []
        for i in range(len(self.__categories)):
            if char.isInCategory(i):
                categoryNames.append(self.__categories[i])
        return categoryNames;

