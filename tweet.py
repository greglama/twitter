from google.appengine.ext import ndb

class Tweet(ndb.Model):
    author = ndb.StringProperty(indexed = True) #pseudo
    authorId = ndb.StringProperty(indexed = True) #user ID
    text = ndb.StringProperty()
    wordSearch = ndb.StringProperty(repeated = True) # tokenise the text to make search easier
    dateTime = ndb.DateTimeProperty(auto_now_add = True)