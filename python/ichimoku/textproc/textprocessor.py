# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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

class TextProcessor:
    def __init__(self, dbFileName, parentDir=None):
      self.dictionary = DartsDictionary(dbFileName)
      self.parser = SentenceParser(parentDir)
      #self.dbFileName = dbFileName
     # self.parentDir = parentDir

    def parseSentence(self, text):
        def isWordInDictionary(word):
            return self.dictionary.getReadingAndDefinition(word)[0] is not None
        allWords = self.parser.splitIntoWords(text, isWordInDictionary)
        return allWords

    #@profile
    def parseSentenceWithBestChoice(self, text):
        #parser = SentenceParser(self.parentDir)
        allWordInfo = self.parser.tokenize2(text)
        #parser = None
        jdictProcessor = JDictProcessor()
        #dictionary = DartsDictionary(self.dbFileName)
        allWords = []
        for wordInfo in allWordInfo:
            if len(wordInfo.dictionaryForm):
                alternatives = self.dictionary.getAllReadingAndDefinition(wordInfo.dictionaryForm)
                reading, definition = jdictProcessor.getBestAlternative(alternatives, wordInfo.partOfSpeech)
                allWords.append((wordInfo.dictionaryForm, reading, definition))
            else:
                #raise RuntimeError(text_type(wordInfo) + ' in ' + text)
            #    if isPy2():
            #        word = codecs.encode(wordInfo.word, 'utf-8')
            #        text = codecs.encode(wordInfo.word, 'utf-8')
            #    else:
            #        word = wordInfo.word
                contextStart = max(0, wordInfo.startPos - 10)
                contextEnd = wordInfo.startPos + len(wordInfo.word) + 10
                textToLog = text[contextStart:contextEnd]
                logging.error("'%s' not found in dictionary. Text: '%s'",
                                wordInfo.word,  textToLog)
        return allWords

    def addToGlossary(self, glossary, allWords, sentence):
        for word in allWords:
            reading, definition = self.dictionary.getReadingAndDefinition(word)
            glossary.add(word, reading, definition, sentence)

    def do(self, text):
        p = TextParser(text)
        glossary = Glossary()
        for sentence in p.getSentences():
            #allWords = self.parseSentence(sentence)
            allWords = self.parseSentenceWithBestChoice(sentence)
            for word, reading, definition in allWords:
                yield word, reading, definition, sentence
       #     self.addToGlossary(glossary, allWords, sentence)
       # for word, reading, definition, sentence in glossary.getFoundWords():
       #     yield word, reading, definition, sentence