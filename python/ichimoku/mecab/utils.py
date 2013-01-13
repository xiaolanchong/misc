# -*- coding: utf-8 -*-

def extractString(buffer, encoding='cp1252'):
        return str(buffer.rstrip(b'\0x00'), encoding)