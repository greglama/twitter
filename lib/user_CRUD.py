import logging
from google.appengine.ext import ndb
from user_twitter import User_twitter
from tweet import Tweet

class User_CRUD:
    def __init__(self):
        pass

    def existsUser(self, userId):
        """return True if there is a user with this id"""
        key_user = ndb.Key("User_twitter", userId)
        user = key_user.get()

        if user != None:
            return True
        else:
            return False

    def getUser(self, userId):
        """return a user with a given id"""
        key_user = ndb.Key("User_twitter", userId)
        user_twitter = key_user.get()
        return user_twitter

    def getAllTweetsOfUser(self, userId):
        """return all the tweets of a user"""
        user = self.getUser(userId)
        tweets = Tweet.query(Tweet.authorId == userId).order(-Tweet.dateTime).fetch()
        return tweets
    
    def get50lastTweetsOfUserIn(self, listId):
        """return the last 50 tweets of a list of users"""

        # tweets that have an authorId in the given list of id order by date 
        tweets = Tweet.query(Tweet.authorId.IN(listId)).order(-Tweet.dateTime).fetch()

        if len(tweets) > 50:
            tweets = tweets[:50]

        return tweets
    
    def createUser(self, userId, name, pseudo):
        """create a new user and return it"""
        if not self.existsUser(userId):
            user = User_twitter(id = userId)
            user.name = name.lower()
            user.pseudo = pseudo.lower()
            user.numberOfTweet = 0
            user.tweets = []

            user.put()

            return user
    
    def searchUserByString(self, string):
        """query all user whom pseudo or name match the string"""
        return User_twitter.query(ndb.OR(User_twitter.name == string.lower(),
                                    User_twitter.pseudo == string.lower())
                                ).fetch()

    def formatTextForSearch(self, text):
        """sets to lower case removes punctuation, new lines, splits on spaces and removes empty strings"""
        return filter(lambda s: s != "" ,
                                    text.lower()
                                    .replace(".","")
                                    .replace(",","")
                                    .replace("!", "")
                                    .replace("?", "")
                                    .replace("'", "")
                                    .replace("\t", " ")
                                    .replace("\n", " ")
                                    .replace("\r", " ")
                                    .split(" "))

    def postTweet(self, userId, text):
        """create a tweet for a given user"""
        user = self.getUser(userId)

        if user != None:
            user.numberOfTweet += 1
            user.put()

            id_tweet = userId + "_" + str(user.numberOfTweet)
            tweet = Tweet(id = id_tweet)
            tweet.author = user.pseudo
            tweet.authorId = userId
            tweet.text = text
            tweet.wordSearch = self.formatTextForSearch(text)
            tweet.put()

    def userStartFollowing(self, userId, idToFollow):
        """The user with id userId starts following the user with id idToFollow"""
        user = self.getUser(userId)
        userToFollow = self.getUser(idToFollow)

        user.suscriptions.append(idToFollow)
        userToFollow.followers.append(userId)
        user.put()
        userToFollow.put()
    
    def userStopToFollow(self, userId, idToUnfollow):
        """The user with id userId stops following the user with id idToUnfollow"""
        user = self.getUser(userId)
        userToUnfollow = self.getUser(idToUnfollow)

        user.suscriptions.remove(idToUnfollow)
        userToUnfollow.followers.remove(userId)
        user.put()
        userToUnfollow.put()

    def doesUserFollow(self, userId, followedId):
        """return True if the user with id userId follows the user with id followedId"""
        user = self.getUser(userId)
        return (followedId in user.suscriptions)

    def isUserFollowed(self, userId, followerId):
        """return True if the user with id userId is followed by the user with id followerId"""
        user = self.getUser(userId)
        return (followerId in user.followers)
    
    def getTimeLineForUser(self, userId):
        user = self.getUser(userId)

        result = []

        suscriptions_ids = list(user.suscriptions)

        #run the query only if the user follow at least one person
        if len(suscriptions_ids) > 0:
            result = self.get50lastTweetsOfUserIn(suscriptions_ids)

        return result
        


