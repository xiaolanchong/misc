# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import logging
import codecs
from mecab.utils import text_type, isPy2
from .textparser import TextParser
from .sentenceparser import SentenceParser
from .glossary import Glossary
from .dartsdict import DartsDictionary
from .jdictprocessor import JDictProcessor

class Settings:
    """
    Output settings of the processor
    """
    def __init__(self):
        self.ignoreSymbols = True # do not output 、 ？ etc.
        self.readingForKanjiOnly = True # do not provide reading if the word has no kanji
        self.sentenceOnlyForFirst = False # give the sentence only for the 1st word in it

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
    def __init__(self, dataLoader):
      self.dictionary = DartsDictionary(dataLoader.load('jdict'))
      self.parser = SentenceParser(dataLoader)

    @classmethod
    def hasKanji(cls, word):
        m = re.search("[\u4E00-\u9FFF]", word, re.S|re.UNICODE)
        return m is not None

    def parseSentence(self, text):
        """
        Parses and looks up the 1st entry in JDIC
        """
        def isWordInDictionary(word):
            return self.dictionary.getReadingAndDefinition(word)[0] is not None
        allWords = self.parser.splitIntoWords(text, isWordInDictionary)
        return allWords

    def getContext(self, text, wordInfo):
        """
        Gets 10 symbol before and after the given one
        text: text to the substring extract from
        wordInfo: the mean of the range
        """
        contextStart = max(0, wordInfo.startPos - 10)
        contextEnd = min(wordInfo.startPos + len(wordInfo.word) + 10, len(text))
        textToLog = text[contextStart:contextEnd]
        return textToLog

    def parseSentenceWithBestChoice(self, text, settings):
        """
        Parses and selects the best match to JDICT dictionary
        text: string to parse
        settings: Settings object to set the parsing up
        """
        allWordInfo = self.parser.tokenize2(text)
        jdictProcessor = JDictProcessor(self.dictionary)
        allWords = []
        for wordInfo in allWordInfo:
            if settings.ignoreSymbols and wordInfo.isNotWord():
                logging.info("'%s' is an unknown token. Text: '%s'",
                            wordInfo.word, self.getContext(text, wordInfo))
                continue
            if len(wordInfo.dictionaryForm):
                alternatives = self.dictionary.getAllReadingAndDefinition(wordInfo.dictionaryForm)
                alternatives = jdictProcessor.filterOnReading(alternatives, wordInfo.kanaReading)
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
            allWords = self.parseSentenceWithBestChoice(sentence, settings)
            for word, reading, definition in allWords:
                yield word, reading, definition, sentence