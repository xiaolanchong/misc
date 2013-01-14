# -*- coding: utf-8 -*-

import unittest
import textparser

class ParserTest(unittest.TestCase):
    #@unittest.skip("demonstrating skipping")
    def testNarration(self):
        textToParse = \
        """
        ジーンの船室、だった。
        ノックをしたところでなんになる？
        　メグレは船室にもどった。
        それから酒を飲んだ……
        """
        p = textparser.TextParser(textToParse)
        result = [
            "ジーンの船室、だった",
            "ノックをしたところでなんになる",
            "メグレは船室にもどった",
            "それから酒を飲んだ"
            ]
        self.assertListEqual(result, list(p.getSentences()))

   # @unittest.skip("demonstrating skipping")
    def testDirectSpeach(self):
        textToParse = \
        "「怒るって何をだね？" \
        "よくご存じでしょう……" \
        "」"
        p = textparser.TextParser(textToParse)
        result = [
            "怒るって何をだね",
            "よくご存じでしょう"
            ]
        self.assertListEqual(result, list(p.getSentences()))

    def testSpacesBeforeSpeachMark(self):
       textToParse = \
       """　ジョン・モーラは背は普通以下の、小柄なそうだった。
             「私に何かご用ですか？
            」
       """
       p = textparser.TextParser(textToParse)
       result = [
            "ジョン・モーラは背は普通以下の、小柄なそうだった",
            "私に何かご用ですか"
            ]
       self.assertListEqual(result, list(p.getSentences()))

    def testRemoveFurigana(self):
        p = textparser.TextParser('錨《いかり》の騒々しい物音', True)
        self.assertListEqual(['錨の騒々しい物音'], p.getSentences())
        p = textparser.TextParser('錨の騒々《そうぞう》しい物音', True)
        self.assertListEqual(['錨の騒々しい物音'], p.getSentences())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ParserTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
