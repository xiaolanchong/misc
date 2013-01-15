# -*- coding: utf-8 -*-

import sys
import os.path
from textproc.textprocessor import TextProcessor

def main():
    if len(sys.argv) != 2:
        print(sys.argv[0], '<filename>')
        exit(0)

    with open(sys.argv[1], 'r', encoding="utf-8") as file:
        contents = file.read()
        textProc = TextProcessor(contents)
        with open(os.path.join('testdata', 'ichimoku_out.txt'), 'w', encoding='utf-8') as outFile:
            for word, reading, definition, sentence in textProc.do():
                outFile.write('{0:<10}  {1:<10}  {2:<10}  {3}\n'.format(word, reading, definition,sentence))


if __name__ == '__main__':
    main()
