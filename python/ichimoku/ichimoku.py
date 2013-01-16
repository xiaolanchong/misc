# -*- coding: utf-8 -*-

import sys
import os.path
from textproc.textprocessor import TextProcessor
from mecab.utils import isPy2, text_type

def openInputFile(fileName):
    if isPy2():
        return open(fileName, 'r')
    else:
        return open(fileName, 'r', encoding='utf-8')

def openOutputFile(fileName):
    if isPy2():
        return open(fileName, 'w')
    else:
        #print('Py3333333')
        return open(fileName, 'w', encoding='utf-8')

def main():
    if len(sys.argv) != 2:
        print(sys.argv[0], '<filename>')
        exit(0)

    with openInputFile(sys.argv[1]) as file:
        contents = file.read()
        if isPy2():
            contents = unicode(contents, 'utf-8')
        parent = os.path.dirname(__file__)
        textProc = TextProcessor(os.path.join('data', 'dict.sqlite'), parent)
        with openOutputFile(os.path.join('testdata', 'ichimoku_zz_py.txt')) as outFile:
            for word, reading, definition, sentence in textProc.do(contents):
                line = text_type('{0:<10}  {1:<10}  {2:<10}  {3}\n').format(word, reading, definition,sentence)
                if isPy2():
                    outFile.write(line.encode('utf-8'))
                else:
                    outFile.write(line)


if __name__ == '__main__':
    main()
