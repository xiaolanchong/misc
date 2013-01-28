# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import logging
import codecs
from mecab.utils import text_type, isPy2
from .textparser import TextParser
from .sentenceparser import SentenceParser
# no sqlite at GAE
#from .sqlitedict import SqliteDictionary
from .glossary import Glossary
from .dartsdict import DartsDictionary
from .jdictprocessor import JDictProcessor

class Settings:
    def __init__(self):
        self.ignoreSymbols = True
        self.readingForKanjiOnly = True
        self.sentenceOnlyForFirst = False

    @classmethod
    def Minimal(cls):
        s = Settings()
        return s

    @classmethod
    def All(cls):
        s = Settings()
        s.ignoreSymbols = False
        s.readingForKanjiOnly = False
        s.sentenceOnlyForFirst = False
        return s

class TextProcessor:
    def __init__(self, dbFileName, parentDir=None):
      self.dictionary = DartsDictionary(dbFileName)
      self.parser = SentenceParser(parentDir)
      #self.dbFileName = dbFileName
     # self.parentDir = parentDir
    @classmethod
    def hasKanji(cls, word):
        m = re.search("[\u4E00-\u9FFF]", word, re.S|re.UNICODE)
        return m is not None

    def parseSentence(self, text):
        def isWordInDictionary(word):
            return self.dictionary.getReadingAndDefinition(word)[0] is not None
        allWords = self.parser.splitIntoWords(text, isWordInDictionary)
        return allWords

    def getContext(self, text, wordInfo):
        contextStart = max(0, wordInfo.startPos - 10)
        contextEnd = min(wordInfo.startPos + len(wordInfo.word) + 10, len(text))
        textToLog = text[contextStart:contextEnd]
        return textToLog


    def parseSentenceWithBestChoice(self, text, settings):
        allWordInfo = self.parser.tokenize2(text)
        jdictProcessor = JDictProcessor()
        allWords = []
        for wordInfo in allWordInfo:
            if settings.ignoreSymbols and wordInfo.isNotWord():
                logging.info("'%s' is an unknown token. Text: '%s'",
                            wordInfo.word, self.getContext(text, wordInfo))
                continue
            if len(wordInfo.dictionaryForm):
                alternatives = self.dictionary.getAllReadingAndDefinition(wordInfo.dictionaryForm)
                reading, definition = jdictProcessor.getBestAlternative(alternatives, wordInfo.partOfSpeech)
                if settings.readingForKanjiOnly and not TextProcessor.hasKanji(wordInfo.dictionaryForm):
                    reading = ''
                allWords.append((wordInfo.dictionaryForm, reading, definition))
            else:
                allWords.append((wordInfo.word, '', ''))
                logging.error("'%s' not found in dictionary. Text: '%s'",
                                wordInfo.word, self.getContext(text, wordInfo))
        return allWords

    def addToGlossary(self, glossary, allWords, sentence):
        for word in allWords:
            reading, definition = self.dictionary.getReadingAndDefinition(word)
            glossary.add(word, reading, definition, sentence)

    def do(self, text, settings = Settings.All()):
        p = TextParser(text)
        glossary = Glossary()
        for sentence in p.getSentences():
            #allWords = self.parseSentence(sentence)
            allWords = self.parseSentenceWithBestChoice(sentence, settings)
            for word, reading, definition in allWords:
                yield word, reading, definition, sentence
       #     self.addToGlossary(glossary, allWords, sentence)
       # for word, reading, definition, sentence in glossary.getFoundWords():
       #     yield word, reading, definition, sentence