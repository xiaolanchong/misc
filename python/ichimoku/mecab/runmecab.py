# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys, os, platform, re, subprocess
import utils

isWin = True

if sys.platform == "win32":
    si = subprocess.STARTUPINFO()
    try:
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    except:
        si.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
else:
    si = None

def mungeForPlatform(popen):
    if isWin:
        popen = [os.path.normpath(x) for x in popen]
        popen[0] += ".exe"
    elif not isMac:
        popen[0] += ".lin"
    return popen

class MecabRunner(object):
    def __init__(self, nodeFormat='%m,%f[6]', eosNodeFormat='\n', unknownNodeFormat='[%m]'):
        self.mecab = None
        self.lineDelimiter = '|'
        self.mecabArgs = ['--node-format=' + nodeFormat + self.lineDelimiter,
                          '--eos-format=' + eosNodeFormat + self.lineDelimiter,
                          '--unk-format=' + unknownNodeFormat + self.lineDelimiter]

    def setup(self):
        base = '..\\support\\'
        self.mecabCmd = mungeForPlatform(
            [base + "mecab"] + self.mecabArgs + [
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

    def run(self, expr):
        self.ensureOpen()
        expr += '\n'
        self.mecab.stdin.write(expr.encode("euc-jp", "ignore"))
        self.mecab.stdin.flush()
        exprFromMecab = utils.text_type(self.mecab.stdout.readline(), "euc-jp")
        exprFromMecab = exprFromMecab.rstrip('\r\n')
        return exprFromMecab.split(self.lineDelimiter)[:-1]

class MecabOutputGetter(MecabRunner):
    def __init__(self):
        fmt = '%m,%f[6],[pos],%h,[cost],%pw,%pC,%pc,%phl,%phr,'\
              '[l2]%pb,%P,%pP,%pA,%pB'
        MecabRunner.__init__(self, fmt, '\n', '=' + fmt)

    def run(self, expr):
        lines = MecabRunner.run(self, expr)
        res = [self.getParam(line) for line in lines]
        return res


    def getParam(self, expr):
        if len(expr) == 0:
            return
      #  if re.match('\[(.+?)\]', expr, re.S):
      #      return
        m = re.match('\=?(.+?),(.*?),\[pos\],(\d+),\[cost\],(-?\d+),(-?\d+),(-?\d+),(-?\d+),(-?\d+),\[l2\].*', expr, re.S)
        if m:
            morphema, dictForm, pos, wordCost, linkCost, totalCost, leftAttr, rightAttr = m.groups()
            return [morphema, dictForm, pos, wordCost, linkCost, totalCost, leftAttr, rightAttr]
        else:
            raise RuntimeError('Incorrect mecab output: ' + expr)

if __name__ == '__main__':
    runner = MecabOutputGetter()
    #res = runner.run('船が検疫所に着いたのは、朝の四時頃にちがいない。')
    res = runner.run('すべてに滲《し》み込み')
    for line in res:
        print(' '.join(line))
