#!/usr/bin/env python

import webapp2
import os.path
import logging

from google.appengine.api import urlfetch
from google.appengine.api.backends import get_url, InvalidBackendError
from django.utils import simplejson
from textproc.textprocessor import TextProcessor, Settings
from wwwapp.start import renderStartPage, renderDeckPage, renderAboutPage
from textproc.dataloader import getDataLoader
import models

class MainPage(webapp2.RequestHandler):
  def get(self):
    user = models.getDefaultUser()
    self.response.out.write(renderStartPage(user.name))

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
        logging.info('send %d bytes text to %s', len(data), url)
        result = urlfetch.fetch(url=url,
                        payload=data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'},
                        deadline=8)
        logging.info('received %d byte text from BE', len(result.content))
        logging.info('received text from BE: %s', result.content[1:100])
        self.response.out.write(result.content)
    except Exception as ex:
        logging.error(str(ex))
        self.response.status = 502
        self.response.status_message = 'Time elapsed while processing the request'

def getTags(tagsText):
    tagSet = set()
    uniqueTags = []
    for tag in tagsText.split(','):
        if tag not in tagSet:
            tagSet.add(tag)
            uniqueTags.append(tag)
    return uniqueTags

class AddCardPage(webapp2.RequestHandler):
  def post(self):
    logging.info('Received AddCard: %d', len(self.request.body))
    word = self.request.get('word')
    reading = self.request.get('reading')
    definition = self.request.get('definition')
    example = self.request.get('example')
    tags = self.request.get('tags')
    tags = getTags(tags)
    logging.info('Received : %s', self.request.body)
    logging.info('add card: %s, readinglen=%d, deflen=%d, examplelen=%d, tagsnum=%d',
                word, len(reading), len(definition), len(example), len(tags))
    models.addCard(word, reading, definition, example, tags)
    self.response.out.write('')

class DeleteCardPage(webapp2.RequestHandler):
  def post(self):
    logging.info('Received DeleteCard: %d', len(self.request.body))
    id = self.request.get('id')
    models.deleteCard(id)
    self.response.out.write('')

class DeckPage(webapp2.RequestHandler):
  def get(self):
    logging.info('Received DeckPage: %d', len(self.request.body))
    user = models.getDefaultUser()
    self.response.out.write(renderDeckPage(user.name, models.getCards()))

class AboutPage(webapp2.RequestHandler):
  def get(self):
    logging.info('Received AboutPage: %d', len(self.request.body))
    user = models.getDefaultUser()
    self.response.out.write(renderAboutPage(user.name))

class ExportDeckPage(webapp2.RequestHandler):
  def post(self):
    logging.info('Received Export: %d', len(self.request.body))
    data = self.request.get('exportdata')
    self.response.headers['Content-Type'] = 'application/force-download'
    self.response.headers['Content-disposition'] = 'attachment; filename=deck.csv'
    self.response.out.write(data)

class BackendPage(webapp2.RequestHandler):
  def get(self):
   self.response.status = 403
   self.response.status_message = "403 Forbidden. The server doesn't accept 'get' requests"

  def post(self):
    logging.info('[BE]Receive POST with %d bytes body', len(self.request.body))
    requestData = simplejson.loads(self.request.body)
    #logging.info(self.request.body)
    #logging.info(requestData)
    userText = requestData.get('text')
    #logging.info(userText)
    result = []
    contents = app.textProc.do(userText, Settings.NoExcessiveReading(), True)
    for word, startPos, reading, definition, sentence in contents:
        result.append((word, reading, definition, sentence))
    #contents = list(contents)
    logging.info("%d records sent", len(result))
    self.response.out.write(simplejson.dumps(result))

class MyApp(webapp2.WSGIApplication):
  def __init__(self):
    webapp2.WSGIApplication.__init__(self, [('/', MainPage),
                                            ('/mydeck', DeckPage),
                                            ('/about', AboutPage),
                                            ('/addcard', AddCardPage),
                                            ('/deletecard', DeleteCardPage),
                                            ('/export', ExportDeckPage),
                                            ('/backend', BackendPage)],
                                            debug=True)
    try:
        get_url()
        logging.info('Starting backend')
        self.textProc = TextProcessor(getDataLoader())
    except InvalidBackendError:
        logging.info('Starting frontend')

app = MyApp()