# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
from google.appengine.ext import db

class User(db.Model):
    """
        A logged user.
    """
    name = db.StringProperty(required=True, indexed=True)
    password = db.StringProperty(required=True)

class Deck(db.Model):
    """
        An arbitrary list of words (cards).
    """
    name = db.StringProperty(required=True)
    user = db.ReferenceProperty(User)

class Card(db.Model):
    """
        A word in a deck.
    """
    word = db.StringProperty(required=True)
    reading = db.StringProperty()
    definition = db.StringProperty(multiline=True)
    example = db.StringProperty(multiline=True)
    tag = db.StringProperty()
    deck = db.ReferenceProperty(Deck)
    added = db.DateTimeProperty(auto_now_add=True)

class Tag(db.Model):
    """
        A label attached to a card
    """
    name = db.StringProperty(required=True)
    user = db.ReferenceProperty(User, required=True)

class TaggedCard(db.Model):
    card = db.ReferenceProperty(Card, required=True)
    tag = db.ReferenceProperty(Tag, required=True)


defaultUser = u"llk"
defaultDeck = u"MyDeck"

def getDefaultUser():
    q = User.all().filter("name =", defaultUser)
    user = q.fetch(1)
    if user:
        return user[0]
    user = User(name=defaultUser, password=u"glitteringprizes")
    user.put()
    return user

def getDefaultDeck():
    defautlUser = getDefaultUser()
    q = Deck.all().filter("name =", defaultDeck)
    deck = q.fetch(1)
    if deck:
        return deck[0]
    deck = Deck(name=defaultDeck, user=defautlUser)
    deck.put()
    return deck

def addCard(word, reading, definition, example):
    defDeck = getDefaultDeck()
    card = Card(word=word, reading=reading,
                definition=definition, example=example, deck=defDeck)
    card.put()

def deleteCard(id):
    Card.delete(Card.get(id))

def getCards():
    deck = getDefaultDeck()
    q = Card.all()
    return q.fetch(None)