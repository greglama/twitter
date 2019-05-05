import logging
from google.appengine.ext import ndb

from models.user_twitter import User_twitter
from models.tweet import Tweet

from user_CRUD import getUser

def formatTextForSearch(text):
    """sets to lower case removes punctuation and new lines, splits on spaces and removes empty strings"""
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

# ------------------- Create and get tweets ----------------------

def postTweet(userId, text):
    """create a tweet for a given user"""
    user = getUser(userId)

    if user != None:
        user.numberOfTweet += 1
        user.put()

        id_tweet = userId + "_" + str(user.numberOfTweet)
        tweet = Tweet(id = id_tweet)
        tweet.author = user.pseudo
        tweet.authorId = userId
        tweet.text = text
        tweet.wordSearch = formatTextForSearch(text)
        tweet.put()


def getAllTweetsOfUser(userId):
    """return all the tweets of a user"""
    user = getUser(userId)
    tweets = Tweet.query(Tweet.authorId == userId).order(-Tweet.dateTime).fetch()
    return tweets


def get50lastTweetsOfUserIn(listId):
    """return the last 50 tweets of a list of users"""

    # tweets that have an authorId in the given list of id order by date 
    tweets = Tweet.query(Tweet.authorId.IN(listId)).order(-Tweet.dateTime).fetch(50)

    return tweets


def getTimeLineForUser(userId):
    """return the tweets of a given user's timeline"""

    user = getUser(userId)
    result = []

    #list of user's id that the current user follow
    suscriptions_ids = list(user.suscriptions)

    #run the query only if the user follow at least one person
    if len(suscriptions_ids) > 0:
        result = get50lastTweetsOfUserIn(suscriptions_ids)

    return result

def plainTextSearch(text):
    """search tweets that could match with the given text"""

    tokenizedText = formatTextForSearch(text)

    resultTweets = Tweet.query(
        Tweet.wordSearch.IN(tokenizedText) # if some of the tweet's words are in the tokenized text
        ).order(-Tweet.dateTime).fetch() # fetch by date from more recent to oldest
    
    return resultTweets
