# -*- coding: utf-8 -*-
# part of speech mapper

import re
import sys
import os.path

sys.path.append(os.path.abspath('..'))
from mecab.dictionary import Dictionary

allPartsOfSpeech = \
"""
abbr, abbr, adj-f, adj-i, adj-ku, adj-na, adj-nari, adj-no,
adj-pn, adj-shiku, adj-t, adv, adv-to, aux, aux-adj, aux-v,
conj, ctr, int, n, n-adv, n-pref, n-suf, n-t, num, on-mim,
pn, pref, prt, suf, v1, v2a-s, v2h-s, v2r-s, v2y-s, v4b, v4h,
v4k, v4r, v5aru, v5b, v5g, v5k, v5k-s, v5m, v5n, v5r, v5r-i,
v5s, v5t, v5u, v5u-s, vi, vk, vn, vr, vs, vs-c, vs-i, vs-s, vt, vz
"""
allPartsOfSpeech = set([ a.strip() for a in allPartsOfSpeech.split(',')])

def getEntryAttributes(entry, r):
    posSet = set()
    m = r.match(entry)
    if len(entry) and m:
        posTags = m.groups()[0].split(',')
        for pos in posTags:
            posSet.add(pos)
    else:
        raise RuntimeError('Invalid format: ' + entry)
    return posSet

def isPartOfSpeech(dictionary, word, posId):
    try:
        res = dictionary.exactMatchSearch(word)
    except UnicodeEncodeError as e:
        print(word, e)
    if len(res) == 0:
        return None
    for token in res:
        if token.partOfSpeechId == posId:
            return True
    return False

def getPartOfSpeech(dictionary, word):
    try:
        res = dictionary.exactMatchSearch(word)
    except UnicodeEncodeError as e:
        #print(word, e)
        return set([])
    if res is None:
        return set([])
    else:
        return set([token.partOfSpeechId for token in res])

def getRecords():
    dictionary = Dictionary(os.path.join(os.path.abspath('..'), 'data', 'sys.zip'))
    with open('../data/dict.txt', 'r', encoding='utf-8') as f:
     #   posSet = set()
        r = re.compile('^.*?\(\s*(.+?)\s*\)', re.S)
        overallDict = {}
        prevLine = ''
        for line in f.readlines():
            if prevLine == line.strip():
                continue
            line = line.strip()
            prev = line
            tokens = line.split('|||')
            entry = tokens[2]
            if len(tokens[0]):
                #overallDict[tokens[0]] = 1 + overallDict.get(tokens[0], 0)
                zzz = overallDict.get(tokens[0], [])
                zzz.append(line)
                overallDict[tokens[0]] = zzz
            elif len(tokens[1]):
                #overallDict[tokens[1]] = 1 + overallDict.get(tokens[1], 0)
                zzz = overallDict.get(tokens[1], [])
                zzz.append(line)
                overallDict[tokens[1]] = zzz
        wordNumber = {}
        with open('dict_dump.txt', 'w', encoding='utf-8') as of:
            for k, v in overallDict.items():
                if len(v) == 2:
                    for line in v:
                        of.write(line + '\n')
      #      wordNumber[v] = 1 + wordNumber.get(v, 0)
      #  print(wordNumber)


def main():
    getRecords()

def ok():
    dictionary = Dictionary(os.path.join(os.path.abspath('..'), 'data', 'sys.zip'))
    with open('../data/dict.txt', 'r', encoding='utf-8') as f:
     #   posSet = set()
        r = re.compile('^.*?\(\s*(.+?)\s*\)', re.S)
        posId = 31
        overallDict = {}
        totalWord = 0
        singlePosWord = 0
        for line in f.readlines():
            tokens = line.split('|||')
            entry = tokens[2]
           # posSet = getEntryAttributes(entry, r)
            posSet = []
           # tokens[0] = '明白'
            if len(tokens[0]):
                #for attribute in posSet:
                #    overallDict[attribute] = 1 + overallDict.get(attribute, 0)
                posSet = getPartOfSpeech(dictionary, tokens[0])
            elif len(posSet) == 0 and len(tokens[1]): # and isPartOfSpeech(dictionary, tokens[1], posId):
                #for attribute in posSet:
                #    overallDict[attribute] = 1 + overallDict.get(attribute, 0)
                posSet = getPartOfSpeech(dictionary, tokens[1])
            if len(posSet) == 0:
                m = re.match('(.+?)\s*/\(.+', tokens[2], re.S)
                if m:
                    posSet = [1] #getPartOfSpeech(dictionary, m.groups()[0])

            totalWord += 1
            overallDict[len(posSet)] = 1 + overallDict.get(len(posSet), 0)
            if len(posSet) > 1:
               # pass
                print(line, posSet)
                #break
        #print(singlePosWord / totalWord)
        for key in overallDict:
            print(key, overallDict[key] / totalWord)
        #    if key in allPartsOfSpeech:
        #        print(key, '\t', overallDict[key])
main()

