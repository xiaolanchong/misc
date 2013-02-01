# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class IntermediateWordInfo:
    def __init__(self, word, startPos, partOfSpeech, reading, definition, isSymbol = False, isKnownWord = True):
        self.word = word
        self.startPos = startPos
        self.partOfSpeech = partOfSpeech
        self.reading = reading
        self.definition = definition
        self.isSymbol = isSymbol
        self.isKnownWord = isKnownWord

    def __repr__(self):
        return '({0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(self.word, self.startPos, self.partOfSpeech,
                                             self.reading, self.definition, self.isSymbol,
                                              self.isKnownWord)
											  

    @classmethod
    def createUnknownWord(cls, word, startPos, partOfSpeech):
        return IntermediateWordInfo(word, startPos, partOfSpeech, '', '', False, False)

    @classmethod
    def createNonWord(cls, word, startPos, partOfSpeech):
        return IntermediateWordInfo(word, startPos, partOfSpeech, '', '', True, False)											  