#!/usr/bin/env python

import cgi
import webapp2
import os.path
#from mecab.viterbi import Viterbi
#from mecab.writer import Writer
from textproc.textprocessor import TextProcessor
from wwwapp.start import renderStartPage

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(renderStartPage(None))

  def post(self):
    userText = self.request.get('content')
    contents = app.getMecabOutput(userText)
    self.response.out.write(renderStartPage(contents))

class MyApp(webapp2.WSGIApplication):
  def __init__(self):
    webapp2.WSGIApplication.__init__(self, [('/', MainPage)], debug=True)
    #sys = os.path.join('data', 'sys.zip')
    #unk = os.path.join('data', 'unk.zip')
    #chz = os.path.join('data', 'char.bin')
    #mtx = os.path.join('data', 'matrix.bin')
    #self.viterbi = Viterbi(sys, unk, chz, mtx)
    #self.writer = Writer()
    self.textProc = TextProcessor(os.path.join('data', 'dict.sqlite'), 'data')

  def getMecabOutput(self, text):
    nodes = self.textProc.do(text)
    return self.writer.getNodeText(self.viterbi.getTokenizer(), nodes)

app = MyApp()
