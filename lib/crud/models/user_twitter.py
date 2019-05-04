from google.appengine.ext import ndb
from tweet import Tweet

class User_twitter(ndb.Model):
    name = ndb.StringProperty()
    pseudo = ndb.StringProperty()
    description = ndb.StringProperty()
    numberOfTweet = ndb.IntegerProperty()

    followers = ndb.StringProperty(repeated = True)
    suscriptions = ndb.StringProperty(repeated = True)