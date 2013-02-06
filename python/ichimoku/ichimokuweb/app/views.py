# Create your views here.

from django.views.generic import TemplateView, View
from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext, Template
import sys
import os
import logging
import models
sys.path.append(os.path.abspath('..'))
from textproc.textprocessor import TextProcessor, Settings
from textproc.dataloader import getDataLoader

logger = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = {'user':'llk'} # compute what you want to pass to the template
        return self.render_to_response(context)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logging.info('Get a message!')
        if request.method == 'POST':
            userText = request.POST['text']
            result = []
            textProc = TextProcessor(getDataLoader())
            contents = textProc.do(userText, Settings.NoExcessiveReading(), True)
            for word, startPos, reading, definition, sentence in contents:
                result.append((word, reading, definition, sentence, self.getWordStatus(word)))
            #contents = list(contents)
          #  logging.info("%d records sent", len(result))
            data = simplejson.dumps(result)
            h = HttpResponse(data, mimetype="application/json", status=200)
            return h

    def getWordStatus(self, word):
        q = models.Card.objects.filter(word=word,deck_id=1)
        return 1 if q.exists() else 0

class AddCardView(View):
    def getTags(self, tagsText):
        tagSet = set()
        uniqueTags = []
        for tag in tagsText.split(','):
            tag = tag.strip()
            if tag not in tagSet:
                tagSet.add(tag)
                uniqueTags.append(tag)
        return uniqueTags

    def post(self, request, *args, **kwargs):
        logging.info("'AddCard' message")
        word = request.POST['word']
        reading = request.POST['reading']
        definition = request.POST['definition']
        example = request.POST['example']
        tags = request.POST['tags']
        tags = self.getTags(tags)
        self.addCard(word, reading, definition, example, tags)
        h = HttpResponse('', mimetype="text/plain", status=200)
        return h

    def addCard(self, word, reading, definition, example, tags):
        card = models.Card.objects.filter(deck_id=1, word=word)
        if not card.exists():
            newCard = models.Card(deck_id=1, word=word, reading=reading,
                              definition =definition, example=example)
            newCard.save()
            card = newCard
        else:
            card = card[0]
        self.attachTags(1, card, tags)

    def addTag(self, userId, tagName):
        tag,created = models.Tag.objects.get_or_create(user_id=userId, name=tagName)
        return tag

    def attachTags(self, userId, card, tagList):
        for tagName in tagList:
            tag = self.addTag(userId, tagName)
            card.tag.add(tag.pk)
        card.save()


class DeckView(TemplateView):
    template_name = 'deck.html'
    context_object_name = "context"

    def get_context_data(self, **kwargs):
        context = super(DeckView, self).get_context_data(**kwargs)
        context['cards'] =  models.Card.objects.filter(deck_id=1).order_by('added')
        return context
