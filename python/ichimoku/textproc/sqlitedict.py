# -*- coding: utf-8 -*-

import sqlite3
#from .mecab import compress

class SqliteDictionary:

    def __init__(self, fileName):
        #thisDir = os.path.dirname(__file__)
        self.__conn = sqlite3.connect(fileName)

    def getReadingAndDefinition(self, word):
        c = self.__conn.cursor()
        c.execute("select kana, entry from dict where kanji=:what order by kanji", {"what": word})
        result = c.fetchone()
        if result:
            return result[0], result[1]
        else:
            return None, None
