# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
from textproc.textprocessor import TextProcessor

class TextProcessorTest(unittest.TestCase):
    def setUp(self):
        zzz = os.path.dirname(__file__)
        zzz = os.path.dirname(zzz)
        self.textProc = TextProcessor(os.path.join('..\\data', 'jdict.zip'), zzz)

    def testRecord(self):
        res = self.textProc.do('船が検疫所に着いたのは')
        for sentence in res:
            for token in sentence:
                print(token[0], token[1], token[2])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TextProcessorTest)
    unittest.TextTestRunner(verbosity=2).run(suite)