# -*- coding: utf-8 -*-

import re
import unicodedata

class TextParser:
    def __init__(self, text):
        self.__sentences = self.__markSentences(text)

    def __markSentences(self, text):
        inDirectSpeach = False
        sentences = []
        for group in re.findall("\s*(「|≪)|(?:(\S+?)(?:。|？|……|！|」|≫))|(」|≫)",
                                text, re.MULTILINE):
            if group[0]:
                inDirectSpeach = True
            elif group[2]:
                inDirectSpeach = False
            else:
                sentences.append(group[1].strip())
        return sentences

    def getSentences(self):
        return self.__sentences