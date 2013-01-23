#!/usr/bin/env python

import webapp2
import os.path
#import urllib
#import urllib2
from google.appengine.api import urlfetch
import logging
from google.appengine.api.backends import get_url
from django.utils import simplejson
from textproc.textprocessor import TextProcessor
from wwwapp.start import renderStartPage

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(renderStartPage(None))

  def post(self):
    logging.info('Received user text: %s', self.request.body)
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
        logging.debug('Received user text: %s', userText)
        #data = urllib.urlencode(simplejson.dumps(values))
        data = simplejson.dumps(values)
        #req = urllib2.Request(get_url(backend='sugoi-ideas',instance=0), data, headers) #'http://localhost:9100'
        #response = urllib2.urlopen(req)
        #res = response.read()
        #taggedData = simplejson.loads(res)
        url = get_url(backend='sugoi-ideas',instance=0) + '/backend'
        logging.info('send %d byte text', len(data))
        result = urlfetch.fetch(url=url,
                        payload=data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
        logging.info('received %d byte text', len(result.content))
       # data = simplejson.loads(result.content)
        self.response.out.write(result.content)
        #self.response.out.write(renderStartPage(data))
    except Exception as ex:
        logging.error(str(ex))
        self.response.status = 502
        self.response.status_message = 'Bad Gateway'

class BackendPage(webapp2.RequestHandler):
  def get(self):
   # self.response.status = 403
   # self.response.status_message = "403 Forbidden. The server doesn't accept 'get' requests"
   pass

  def post(self):
    logging.info('################# get POST')
    requestData = simplejson.loads(self.request.body)
    logging.info(self.request.body)
    logging.info(requestData)
    userText = requestData.get('text')
    logging.info(userText)
    #contents = [['word01'],['definition01'] ]#app.getMecabOutput(userText)
    self.textProc = TextProcessor(os.path.join('data', 'jdict.zip'), '.')
    contents = self.textProc.do(userText)
    contents = list(contents)
   # contents = getMecabOutput(userText)
    self.response.out.write(simplejson.dumps(contents))

class MyApp(webapp2.WSGIApplication):
  def __init__(self):
    webapp2.WSGIApplication.__init__(self, [('/', MainPage), ('/backend', BackendPage)], debug=True)
    logging.info('started FrontEnd')

app = MyApp()