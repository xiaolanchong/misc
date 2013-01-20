# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys, os, platform, re, subprocess
import mecab.utils
import mecab.runmecab as runmecab
from mecab.viterbi import Viterbi
from mecab.writer import Writer
#from textproc.wordclass import PartOfSpeech, SubType

class SentenceParser(object):

    def __init__(self, rootDir=None):
        if rootDir is None:
            self.mecab = runmecab.MecabRunner(
             '%m,%f[6],%f[0],%f[1],%f[2],%f[3],%f[4],%f[5] ', '\n', '[%m] ')
        else:
            self.mecab = None
            sys = os.path.join(rootDir, 'data', 'sys.zip')
            unk = os.path.join(rootDir, 'data', 'unk.zip')
            chz = os.path.join(rootDir, 'data', 'char.bin')
            mtx = os.path.join(rootDir, 'data', 'matrix.bin')
            self.viterbi = Viterbi(sys, unk, chz, mtx)
            self.writer = Writer()

    def tokenize(self, expr, dumpNodes=False):
        if self.mecab:
            return self.tokenizeNative(expr, dumpNodes)
        else:
            return self.tokenizePyPort(expr, dumpNodes)

    def tokenizePyPort(self, expr, dumpNodes):
        path = self.viterbi.getBestPath(expr)
        res = self.writer.getMorphAndFeature(self.viterbi.getTokenizer(), path)
        out = []
        for tokenData in res:
            # [(tokenData[7], tokenData[0], tokenData[1], tokenData[2]) for tokenData in res]
            (originWord, dictionaryForm, symbolicPartOfSpeech, subType) =\
                tokenData[7], tokenData[0], tokenData[1], tokenData[2]
            isSuffix, skipIfNoOccurrence = self.getSuffixInfo(symbolicPartOfSpeech, subType)
            if dumpNodes:
                print(node)
            out.append((originWord, dictionaryForm, isSuffix, skipIfNoOccurrence))
        return out

    def tokenize2(self, expr):
        path = self.viterbi.getBestPath(expr)
        return self.writer.getWordInfo(self.viterbi.getTokenizer(), path)

    def tokenizeNative(self, expr, dumpNodes):
        exprFromMecab = self.mecab.run(expr)
        out = []
        for line in exprFromMecab:
            for node in line.split(" "):
                if not node:
                  break
                m =  re.match("(.+),(.+),(.+),(.*),(?:.*),(?:.*),(?:.*),(?:.*)", node);
                if m is None:
                    m = re.match("\[(.+)\]", node)
                    if m:
                    #raise RuntimeError('unknown node: ' + node)
                        word = m.groups(0)[0]
                        out.append((word, word, False, False))
                    else:
                        raise RuntimeError(node)
                else:
                    (originWord, dictionaryForm, symbolicPartOfSpeech, subType) = m.groups()
                    isSuffix, skipIfNoOccurrence = self.getSuffixInfo(symbolicPartOfSpeech, subType)
                    if dumpNodes:
                       print(node)
                    out.append((originWord, dictionaryForm, isSuffix, skipIfNoOccurrence))

        return out

    def splitIntoWords(self, expr, dictionary, dumpNodes=False):
        tokens = self.tokenize(expr, dumpNodes)
        allWords = []
        lastToken =None
        for originWord, dictionaryForm, isSuffix, skipIfNoOccurrence in tokens:
            if not isSuffix:
                if lastToken:
                    allWords.append(lastToken[1])
                lastToken = (originWord, dictionaryForm)
            else:
                if not lastToken:
                    lastToken = (originWord, dictionaryForm)
                else:
                    wordInDictionary = dictionary(lastToken[0] + originWord)
                    if wordInDictionary:
                        lastToken = (lastToken[0] + originWord, lastToken[1] + dictionaryForm)
                    else:
                        allWords.append(lastToken[1])
                        if skipIfNoOccurrence:
                            lastToken = None
                        else:
                            lastToken = (originWord, dictionaryForm)
        if lastToken:
            allWords.append(lastToken[1])
        return allWords

    def getSuffixInfo(self, partOfSpeech, subType):
        result = { '名詞' : (subType == '接尾', False) ,
##                   'å‹•è©ž' : (PartOfSpeech.VERB, False),
##                   'å½¢å®¹è©ž' : (PartOfSpeech.ADJECTIVE, False),
##                   'å‰¯è©ž' : (PartOfSpeech.ADVERB, False),
##                   'åŠ©è©ž' : (PartOfSpeech.PARTICLE, False),
##                   'æ„Ÿå‹•è©ž' : (PartOfSpeech.INTERJECTION, False),
##                   'è¨˜å·' : (PartOfSpeech.SYMBOL, False),
                   '助動詞' : (True, True),
                   '助詞' : (subType == '接続助詞', subType == '接続助詞')
##                   '' : (PartOfSpeech.CONJUNCTION, False)
                  }
        return result.get(partOfSpeech, (False, False))