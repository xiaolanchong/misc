#!/usr/bin/env python

import webapp2
import os.path
import logging
from google.appengine.api import urlfetch
from google.appengine.api.backends import get_url, InvalidBackendError
from django.utils import simplejson
from textproc.textprocessor import TextProcessor
from wwwapp.start import renderStartPage

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(renderStartPage(None))

  def post(self):
    logging.info('Received POST: %s', len(self.request.body))
    #data = simplejson.loads(self.request.body)
    userText = self.request.get('text')
    try:
        headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                    'Content-Type' : 'application/json' }
        values = {'text' : userText,
                  'word' : 1,
                  'definition' : 1,
                  'sentence' : 1 }
        logging.info('Received user text %d bytes', len(userText))
        #logging.debug('Received user text: %s', userText)
        data = simplejson.dumps(values)
        url = get_url(backend='sugoi-ideas') + '/backend'
        logging.info('send %d bytes text', len(data))
        result = urlfetch.fetch(url=url,
                        payload=data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'},
                        deadline=8)
        logging.info('received %d byte text', len(result.content))
        self.response.out.write(result.content)
    except Exception as ex:
        logging.error(str(ex))
        self.response.status = 502
        self.response.status_message = 'Time elapsed while processing the request'

class BackendPage(webapp2.RequestHandler):
  def get(self):
   self.response.status = 403
   self.response.status_message = "403 Forbidden. The server doesn't accept 'get' requests"

  def post(self):
    logging.info('Receive POST with %d bytes body', len(self.request.body))
    requestData = simplejson.loads(self.request.body)
    #logging.info(self.request.body)
    #logging.info(requestData)
    userText = requestData.get('text')
    #logging.info(userText)
    contents = app.textProc.do(userText)
    contents = list(contents)
    self.response.out.write(simplejson.dumps(contents))

class MyApp(webapp2.WSGIApplication):
  def __init__(self):
    webapp2.WSGIApplication.__init__(self, [('/', MainPage),
                                            ('/backend', BackendPage)],
                                            debug=True)
    try:
        get_url()
        logging.info('Starting backend')
        self.textProc = TextProcessor(os.path.join('data', 'jdict.zip'), '.')
    except InvalidBackendError:
        logging.info('Starting frontend')

app = MyApp()