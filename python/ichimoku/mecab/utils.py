# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys

if sys.version < '3':
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes

def extractString(buffer, encoding='ascii'):
        return text_type(buffer.rstrip(b'\0x00'), encoding)
