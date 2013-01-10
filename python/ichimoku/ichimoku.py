# -*- coding: utf-8 -*-

import sys
import textparser
from sentenceparser import SentenceParser
from dictionary import Dictionary
from glossary import Glossary

def parseSentence(parser, dictionary, text):
    def isWordInDictionary(word):
        return dictionary.getReadingAndDefinition(word)[0] is not None
    allWords = parser.splitIntoWords(text, isWordInDictionary)
    return allWords

def addToGlossary(glossary, allWords, sentence, dictionary):
    for word in allWords:
        definition = dictionary.getReadingAndDefinition(word)[1]
        glossary.add(word, definition, sentence)

def main():
    if len(sys.argv) != 2:
        print(sys.argv[0], '<filename>')
        exit(0)
    with open(sys.argv[1], encoding="utf-8") as file:
        contents = file.read()
        p = textparser.TextParser(contents)
        sentenceParser = SentenceParser()
        glossary = Glossary()
        dictionary = Dictionary()
        for sentence in p.getSentences()[1:100]:
            allWords = parseSentence(sentenceParser, dictionary, sentence)
            addToGlossary(glossary, allWords, sentence, dictionary)
            #print(sentence, allWords)
        with open('out.txt', 'w', encoding='utf-8') as outFile:
            for word, definition, sentence in glossary.getItems():
                outFile.write('{0:<10}   {1}   {2}\n'.format(word, definition,sentence))


if __name__ == '__main__':
    main()
