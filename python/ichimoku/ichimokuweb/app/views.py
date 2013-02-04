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

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return super(AjaxableResponseMixin, self).form_invalid(form)

    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'pk': form.instance.pk,
            }
            return self.render_to_json_response(data)
        else:
            return super(AjaxableResponseMixin, self).form_valid(form)

logger = logging.getLogger(__name__)

class IndexView(AjaxableResponseMixin, TemplateView):
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
                result.append((word, reading, definition, sentence))
            #contents = list(contents)
          #  logging.info("%d records sent", len(result))
            data = simplejson.dumps(result)
            h = HttpResponse(data, mimetype="application/json", status=200)
            return h

class AddCardView(View):
    def getTags(self, tagsText):
        tagSet = set()
        uniqueTags = []
        for tag in tagsText.split(','):
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
        newCard = models.Card(deck_id=1, word=word, reading=reading,
                                     example=example)
        newCard.save()

class DeckView(TemplateView):
    template_name = 'deck.html'
