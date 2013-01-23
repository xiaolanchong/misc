#!/usr/bin/env python

import webapp2
import os.path
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
    self.textProc = TextProcessor(os.path.join('data', 'jdict.zip'), '.')

  def getMecabOutput(self, text):
    nodes = self.textProc.do(text)
    return nodes

app = MyApp()
