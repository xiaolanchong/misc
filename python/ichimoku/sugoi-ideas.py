#!/usr/bin/env python

import cgi
import webapp2
import os.path
from mecab.viterbi import Viterbi
from mecab.writer import Writer

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    self.response.out.write("""
          <form action="/" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
        </body>
      </html>""")

  def post(self):
    self.response.out.write('<html><body>')
    reqContent = self.request.get('content')
    self.response.out.write("""
          <form action="/" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
		  <H1>""" +
		  self.getMecabOutput(reqContent) +
		  """</H1>
        </body>
      </html>""")

  def getMecabOutput(self, text):
    return app.getMecabOutput(text)

class MyApp(webapp2.WSGIApplication):
  def __init__(self):
    webapp2.WSGIApplication.__init__(self, [('/', MainPage)], debug=True)

    sys = os.path.join('data', 'sys.zip')
    unk = os.path.join('data', 'unk.zip')
    chz = os.path.join('data', 'char.bin')
    mtx = os.path.join('data', 'matrix.bin')
    self.viterbi = Viterbi(sys, unk, chz, mtx)
    self.writer = Writer()

  def getMecabOutput(self, text):
    nodes = self.viterbi.getBestPath(text)
    res = ', '.join(self.writer.getNodeText(self.viterbi.getTokenizer(), nodes))
    return res

app = MyApp()
