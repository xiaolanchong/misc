
# -*- coding: utf-8 -*-

class Token:
    def __init__(self, leftAttribute, rightAttribute,
                        partOfSpeechId, wordCost,
                        featureId, compound):
        self.leftAttribute = leftAttribute
        self.rightAttribute = rightAttribute
        self.partOfSpeechId = partOfSpeechId
        self.wordCost = wordCost
        self.featureId = featureId
        self.compound = compound

    def __eq__(self, other):
        return  self.leftAttribute == other.leftAttribute and \
                self.rightAttribute == other.rightAttribute and  \
                self.partOfSpeechId == other.partOfSpeechId and  \
                self.wordCost == other.wordCost and \
                self.featureId == other.featureId and \
                self.compound == other.compound

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'la:{0}, ra:{1}, pos:{2}, cost:{3}, feature:{4}, compound:{5}'.format(
                    self.leftAttribute, self.rightAttribute, self.partOfSpeechId,
                    self.wordCost, self.featureId, self.compound)