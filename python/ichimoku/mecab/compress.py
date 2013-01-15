# -*- coding: utf-8 -*-

from zipfile import ZipFile

def load(fileName):
    """
        Loads the first file from the zip compressed file
    """
    with ZipFile(fileName, 'r') as zipFile:
        fileList =  zipFile.namelist()
        if len(fileList) == 0:
            raise IOError('No files in ' + fileName)
        return zipFile.open(fileList[0], 'r')