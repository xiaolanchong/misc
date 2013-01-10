# -*- coding: utf-8 -*-

class Glossary:
    def __init__(self):
        self.words = set()
        self.orderedItems = []

    def add(self, word, definition, usageSample):
        if word not in self.words:
            self.words.add(word)
            self.orderedItems.append((word, definition, usageSample))

    def getItems(self):
        return self.orderedItems