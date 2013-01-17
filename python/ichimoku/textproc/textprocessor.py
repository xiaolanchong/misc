
from .textparser import TextParser
from .sentenceparser import SentenceParser
# no sqlite at GAE
#from .sqlitedict import SqliteDictionary
from .glossary import Glossary
from .dartsdict import DartsDictionary

class TextProcessor:
    def __init__(self, dbFileName, parentDir=None):
        self.dictionary = DartsDictionary(dbFileName)
        self.sentenceParser = SentenceParser(parentDir)

    def parseSentence(self, parser, text):
        def isWordInDictionary(word):
            return self.dictionary.getReadingAndDefinition(word)[0] is not None
        allWords = parser.splitIntoWords(text, isWordInDictionary)
        return allWords

    def addToGlossary(self, glossary, allWords, sentence):
        for word in allWords:
            reading, definition = self.dictionary.getReadingAndDefinition(word)
            glossary.add(word, reading, definition, sentence)

    def do(self, text):
        p = TextParser(text)
        glossary = Glossary()
        for sentence in p.getSentences():
            allWords = self.parseSentence(self.sentenceParser, sentence)
            self.addToGlossary(glossary, allWords, sentence)
        for word, reading, definition, sentence in glossary.getFoundWords():
            yield word, reading, definition, sentence