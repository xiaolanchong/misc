# -*- coding: utf-8 -*-

import sqlite3

class Dictionary:

    def __init__(self):
        self.__conn = sqlite3.connect('dict.sqlite')

    def getReadingAndDefinition(self, word):
        c = self.__conn.cursor()
        c.execute("select kana, entry from dict where kanji=:what order by kanji", {"what": word})
        result = c.fetchone()
        if result:
            return result[0], result[1]
        else:
            return None, None
