# -*- coding: utf-8 -*-

from textproc.textparser import TextParser
from textproc.sentenceparser import SentenceParser
# no sqlite at GAE
#from .sqlitedict import SqliteDictionary
from textproc.glossary import Glossary
from textproc.dartsdict import DartsDictionary
from textproc.jdictprocessor import JDictProcessor

class TextProcessor:
    def __init__(self, dbFileName, parentDir=None):
        self.dictionary = DartsDictionary(dbFileName)
        self.sentenceParser = SentenceParser(parentDir)

    def parseSentence(self, parser, text):
        def isWordInDictionary(word):
            return self.dictionary.getReadingAndDefinition(word)[0] is not None
        allWords = parser.splitIntoWords(text, isWordInDictionary)
        return allWords

    def parseSentenceWithBestChoice(self, parser, text):
        allWordInfo = parser.tokenize2(text)
        jdictProcessor = JDictProcessor()
        allWords = []
        for wordInfo in allWordInfo:
            if len(wordInfo.dictionaryForm):
                alternatives = self.dictionary.getAllReadingAndDefinition(wordInfo.dictionaryForm)
                reading, definition = jdictProcessor.getBestAlternative(alternatives, wordInfo.partOfSpeech)
                allWords.append((wordInfo.dictionaryForm, reading, definition))
            else:
                RuntimeError(str(wordInfo) + ' in ' + text)
        return allWords

    def addToGlossary(self, glossary, allWords, sentence):
        for word in allWords:
            reading, definition = self.dictionary.getReadingAndDefinition(word)
            glossary.add(word, reading, definition, sentence)

    def do(self, text):
        p = TextParser(text)
        glossary = Glossary()
        for sentence in p.getSentences():
            #allWords = self.parseSentence(self.sentenceParser, sentence)
            allWords = self.parseSentenceWithBestChoice(self.sentenceParser, sentence)
            for word, reading, definition in allWords:
                yield word, reading, definition, sentence
       #     self.addToGlossary(glossary, allWords, sentence)
       # for word, reading, definition, sentence in glossary.getFoundWords():
       #     yield word, reading, definition, sentence