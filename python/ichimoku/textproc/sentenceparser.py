# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys, os, platform, re, subprocess
import mecab.utils as utils
#from textproc.wordclass import PartOfSpeech, SubType

isWin = True
mecabArgs = ['--node-format=%m,%f[6],%f[0],%f[1],%f[2],%f[3],%f[4],%f[5] ',
             '--eos-format=\n',
             '--unk-format=[%m] ']

if sys.platform == "win32":
    si = subprocess.STARTUPINFO()
    try:
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    except:
        si.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
else:
    si = None

# Mecab
##########################################################################

def mungeForPlatform(popen):
    if isWin:
        popen = [os.path.normpath(x) for x in popen]
        popen[0] += ".exe"
    elif not isMac:
        popen[0] += ".lin"
    return popen

class SentenceParser(object):

    def __init__(self):
        self.mecab = None

    def setup(self):
        base = '..\\support\\'
        self.mecabCmd = mungeForPlatform(
            [base + "mecab"] + mecabArgs + [
                '-d', base, '-r', base + "mecabrc"])
        os.environ['DYLD_LIBRARY_PATH'] = base
        os.environ['LD_LIBRARY_PATH'] = base
        if not isWin:
            os.chmod(self.mecabCmd[0], 0o755)

    def ensureOpen(self):
        if not self.mecab:
            self.setup()
            try:
                self.mecab = subprocess.Popen(
                    self.mecabCmd, bufsize=-1, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    startupinfo=si)
            except OSError:
                raise Exception("Please install mecab")

    def tokenize(self, expr, dumpNodes=False):
        self.ensureOpen()
        expr += '\n'
        self.mecab.stdin.write(expr.encode("euc-jp", "ignore"))
        self.mecab.stdin.flush()
        exprFromMecab = utils.text_type(self.mecab.stdout.readline(), "euc-jp")
        exprFromMecab = exprFromMecab.rstrip('\r\n')
        out = []
        for node in exprFromMecab.split(" "):
            if not node:
                break
            m =  re.match("(.+),(.+),(.+),(.*),(?:.*),(?:.*),(?:.*),(?:.*)", node);
            if m is None:
                m = re.match("\[(.+)\]", node)
                if m:
                    #raise RuntimeError('unknown node: ' + node)
                    word = m.groups(0)[0]
                    out.append((word, word, False, False))

                else:
                    raise RuntimeError(node)
            else:
                (originWord, dictionaryForm, symbolicPartOfSpeech, subType) = m.groups()
                isSuffix, skipIfNoOccurrence = self.getSuffixInfo(symbolicPartOfSpeech, subType)
                if dumpNodes:
                    print(node)
                out.append((originWord, dictionaryForm, isSuffix, skipIfNoOccurrence))

        return out

    def splitIntoWords(self, expr, dictionary, dumpNodes=False):
        tokens = self.tokenize(expr, dumpNodes)
        allWords = []
        lastToken =None
        for originWord, dictionaryForm, isSuffix, skipIfNoOccurrence in tokens:
            if not isSuffix:
                if lastToken:
                    allWords.append(lastToken[1])
                lastToken = (originWord, dictionaryForm)
            else:
                if not lastToken:
                    lastToken = (originWord, dictionaryForm)
                else:
                    wordInDictionary = dictionary(lastToken[0] + originWord)
                    if wordInDictionary:
                        lastToken = (lastToken[0] + originWord, lastToken[1] + dictionaryForm)
                    else:
                        allWords.append(lastToken[1])
                        if skipIfNoOccurrence:
                            lastToken = None
                        else:
                            lastToken = (originWord, dictionaryForm)
        if lastToken:
            allWords.append(lastToken[1])
        return allWords

    def getSuffixInfo(self, partOfSpeech, subType):
        result = { '名詞' : (subType == '接尾', False) ,
##                   'å‹•è©ž' : (PartOfSpeech.VERB, False),
##                   'å½¢å®¹è©ž' : (PartOfSpeech.ADJECTIVE, False),
##                   'å‰¯è©ž' : (PartOfSpeech.ADVERB, False),
##                   'åŠ©è©ž' : (PartOfSpeech.PARTICLE, False),
##                   'æ„Ÿå‹•è©ž' : (PartOfSpeech.INTERJECTION, False),
##                   'è¨˜å·' : (PartOfSpeech.SYMBOL, False),
                   '助動詞' : (True, True),
                   '助詞' : (subType == '接続助詞', subType == '接続助詞')
##                   '' : (PartOfSpeech.CONJUNCTION, False)
                  }
        return result.get(partOfSpeech, (False, False))