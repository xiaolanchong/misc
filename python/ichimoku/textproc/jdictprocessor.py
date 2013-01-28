# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
from .wordmapper import WordMapper
from mecab.writer import WordInfo
import mecab.partofspeech as PoS
from mecab.utils import isPy2
if isPy2:
    import jcconv_2x as jcconv
else:
    import jcconv_3x as jcconv

class JDictProcessor:
    def __init__(self, lookupDictionary):
        self.attrRegex = re.compile('^.*?\(\s*(.+?)\s*\)', re.S)
        self.dictionary = lookupDictionary

    def getWordAttributes(self, entry):
        posSet = set()
        m = self.attrRegex.match(entry)
        if len(entry) and m:
            posTags = m.groups()[0].split(',')
            for pos in posTags:
                posSet.add(pos)
        else:
            raise RuntimeError('Invalid format: ' + entry)
        return posSet

    def getBestAlternative(self, wordsAndDefinitions, pos):
        if len(wordsAndDefinitions) == 0:
            return (None, None)
        elif len(wordsAndDefinitions) == 1:
            return wordsAndDefinitions[0]
        allAttributes = [self.getWordAttributes(definition) for word, definition in wordsAndDefinitions]
        mapper = WordMapper()
        res = mapper.selectBestWord(allAttributes, pos)
        if res is not None:
            return wordsAndDefinitions[res]
        else:
            return None

    def getBestAlternativeOnReading(self, wordsAndDefinitions, mecabReading):
        if len(wordsAndDefinitions) == 0:
            return (None, None)
        elif len(wordsAndDefinitions) == 1:
            return wordsAndDefinitions[0]
        allAttributes = [self.getWordAttributes(definition) for word, definition in wordsAndDefinitions]
        mapper = WordMapper()
        res = mapper.selectBestWord(allAttributes, pos)
        if res is not None:
            return wordsAndDefinitions[res]
        else:
            return None

    def lookup(self, word):
        return self.dictionary.getFirstReadingAndDefinition(word)

    def mergeWord(self, a, b):
        if PoS.isNoun(a.partOfSpeech) and PoS.isNoun(b.partOfSpeech):
            mergedWord = a.word + b.word
            reading, definition = self.lookup(a.word + b.word)
            if reading:
                return WordInfo(mergedWord, a.startPos, mergedWord, PoS.NOUN, reading)
        return None