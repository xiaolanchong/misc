# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
from .wordmapper import WordMapper
from mecab.writer import WordInfo
import mecab.partofspeech as PoS
from mecab.utils import isPy2
if isPy2():
    import textproc.jcconv_2x as jcconv
else:
    import textproc.jcconv_3x as jcconv

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

    def filterOnReading(self, readingsAndDefinitions, mecabReading):
        if len(readingsAndDefinitions) == 0:
            return [(None, None)]
        elif len(readingsAndDefinitions) == 1:
            return readingsAndDefinitions
        hiraganaReading = jcconv.kata2hira(mecabReading)
        filtered = []
        for reading, definition in readingsAndDefinitions:
            if hiraganaReading == reading:
                filtered.append(( reading, definition))
        return filtered if len(filtered) else readingsAndDefinitions

    def lookup(self, word):
        return self.dictionary.getFirstReadingAndDefinition(word)

    def mergeWord(self, a, b):
        rules = [ self.mergeNoun, self.mergeVerb ]
        for rule in rules:
            c = rule(a, b)
            if c:
                return c
        return None

    def mergeVerb(self, a, b):
        if a.partOfSpeech == PoS.VERB and PoS.isAfterVerb(b.partOfSpeech):
            c = a.word + b.word
            reading, definition = self.lookup(c)
            if reading:
                return WordInfo(c, a.startPos, c, PoS.VERB, reading)
        return None

##    def mergeVerbDeconjugate(self, a, b, dictionary):
##        if a.partOfSpeech == PoS.VERB and PoS.isAfterVerb(b.partOfSpeech):
##            tokens = dictionary.exactMatch(b)
##            words = [for tokens in ]
##            reading, definition = self.lookup(c)
##            if reading:
##                return WordInfo(c, a.startPos, c, PoS.VERB, reading)
##        return None

##    def mergeVerbWithReading(self, a, b):
##        if a.partOfSpeech == PoS.VERB and PoS.isAfterVerb(b.partOfSpeech):
##            c = a.word + b.word
##            reading, definition = self.lookup(c)
##            if reading:
##                return WordInfo(c, a.startPos, c, PoS.NOUN, reading)
##        return None

    def mergeNoun(self, a, b):
        if PoS.isNoun(a.partOfSpeech) and PoS.isNoun(b.partOfSpeech):
            c = a.word + b.word
            reading, definition = self.lookup(c)
            if reading:
                return WordInfo(c, a.startPos, c, PoS.NOUN, reading)
        return None

    def mergeByRule(self, conditionA, conditionB, resultPoS, a, b):
        if conditionA(a.partOfSpeech) and conditionB(b.partOfSpeech):
            mergedWord = a.word + b.word
            reading, definition = self.lookup(a.word + b.word)
            if reading:
                return WordInfo(mergedWord, a.startPos, mergedWord, resultPoS, reading)
        return None
