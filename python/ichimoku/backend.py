#!/usr/bin/env python

import os.path
import webapp2
import logging
from django.utils import simplejson
from textproc.textprocessor import TextProcessor

class BackendPage(webapp2.RequestHandler):
  def get(self):
   # self.response.status = 403
   # self.response.status_message = "403 Forbidden. The server doesn't accept 'get' requests"
   pass

  def post(self):
    logging.info('################# get POST')
    requestData = simplejson(self.request.body)
    userText = requestData.get('text')
    contents = app.getMecabOutput(userText)
    self.response.out.write(simplejson(contents))

class MyApp(webapp2.WSGIApplication):
  def __init__(self):
    webapp2.WSGIApplication.__init__(self, [('/', BackendPage)], debug=True)
    logging.info('start ---------<')
    self.textProc = TextProcessor(os.path.join('data', 'jdict.zip'), '.')

  def getMecabOutput(self, text):
    nodes = self.textProc.do(text)
    return nodes

app = MyApp()