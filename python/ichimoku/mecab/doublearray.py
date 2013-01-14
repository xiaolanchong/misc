# -*- coding: utf-8 -*-

from struct import unpack

class DoubleArray:
    def __init__(self, dataZ):
        assert(isinstance(dataZ, bytes))
        self.dataZ = dataZ

    def exactMatchSearch(self, sequence):
        pass

    def getItemZ(self, index):
        return unpack('<iI', self.dataZ[8*index : 8*index+8])

    def commonPrefixSearch(self, sequence):
        node_pos = 0
        base,dummy = self.getItemZ(node_pos)
        res = []
        idx = 0
        for item in sequence:
            bb, cc = self.getItemZ(base)
            if base == cc and bb < 0:
                res.append((-bb-1, idx))
            p = base + item + 1
            bz, cz = self.getItemZ(p)
            if base == cz:
                base = bz
            else:
                return res
            idx += 1
        bb, cc = self.getItemZ(base)
        if base == cc and bb < 0:
            res.append((-bb-1, idx))
        return res
