# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
from textproc.wordmapper import WordMapper

class JDictProcessor:
    def __init__(self):
        self.attrRegex = re.compile('^.*?\(\s*(.+?)\s*\)', re.S)


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