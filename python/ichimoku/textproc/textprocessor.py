
from .textparser import TextParser
from .sentenceparser import SentenceParser
from .dictionary import Dictionary
from .glossary import Glossary

class TextProcessor:
    def __init__(self, dbFileName):
        self.dictionary = Dictionary(dbFileName)

    def parseSentence(parser, text):
        def isWordInDictionary(word):
            return self.dictionary.getReadingAndDefinition(word)[0] is not None
        allWords = parser.splitIntoWords(text, isWordInDictionary)
        return allWords

    def addToGlossary(glossary, allWords, sentence):
        for word in allWords:
            reading, definition = self.dictionary.getReadingAndDefinition(word)
            glossary.add(word, reading, definition, sentence)

    def do(self, text):
        p = TextParser(text)
        sentenceParser = SentenceParser()
        glossary = Glossary()
        for sentence in p.getSentences():
            allWords = parseSentence(sentenceParser, sentence)
            addToGlossary(glossary, allWords, sentence)
        #with open('testdata/ichimoku_out.txt', 'w', encoding='utf-8') as outFile:
        #    for word, reading, definition, sentence in glossary.getFoundWords():
        #        outFile.write('{0:<10}  {1:<10}  {2:<10}  {3}\n'.format(word, reading, definition,sentence))
            for word, reading, definition, sentence in glossary.getFoundWords():
                yield word, reading, definition, sentence