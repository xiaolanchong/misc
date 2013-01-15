# -*- coding: utf-8 -*-

import sqlite3
import os.path

class Dictionary:

    def __init__(self):
        thisDir = os.path.dirname(__file__)
        self.__conn = sqlite3.connect(os.path.join(thisDir, '..', 'data', 'dict.sqlite'))

    def getReadingAndDefinition(self, word):
        c = self.__conn.cursor()
        c.execute("select kana, entry from dict where kanji=:what order by kanji", {"what": word})
        result = c.fetchone()
        if result:
            return result[0], result[1]
        else:
            return None, None
