from google.appengine.ext import ndb
from tweet import Tweet

class User_twitter(ndb.Model):
    name = ndb.StringProperty()
    pseudo = ndb.StringProperty()
    numberOfTweet = ndb.IntegerProperty()