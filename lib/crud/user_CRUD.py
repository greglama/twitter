from google.appengine.ext import ndb

from models.user_twitter import User_twitter
from models.tweet import Tweet

import logging

#------------ Creation, Get, Update, Exist, Search -----------------
def createUser(userId, name, pseudo, description):
    """create a new user and return it"""
    if not existsUser(userId):
        user = User_twitter(id = userId)
        user.name = name.lower()
        user.pseudo = pseudo.lower()
        user.numberOfTweet = 0
        user.tweets = []
        user.description = description
        user.suscriptions = [userId] # so the user's tweets end up inside his timeline

        user.put()
 
        return user

def getUser(userId):
    """return a user with a given id"""
    key_user = ndb.Key("User_twitter", userId)
    user_twitter = key_user.get()
    return user_twitter

def updateUser(userId, name, description):
    """update a user's name and description"""

    user = getUser(userId)
    user.name = name
    user.description = description
    user.put()

def existsUser(userId):
    """return True if there is a user with this id"""
    key_user = ndb.Key("User_twitter", userId)
    user = key_user.get()

    if user != None:
        return True
    else:
        return False

def searchUserByString(string):
    """query all user whom pseudo or name match the string"""
    return User_twitter.query(ndb.OR(User_twitter.name == string.lower(),
                                User_twitter.pseudo == string.lower())
                            ).fetch()

#------------ Follow, Unfollow -----------------

def userStartFollowing(userId, idToFollow):
    """The user with id userId starts following the user with id idToFollow"""
    user = getUser(userId)
    userToFollow = getUser(idToFollow)

    user.suscriptions.append(idToFollow)
    userToFollow.followers.append(userId)
    user.put()
    userToFollow.put()

def userStopToFollow(userId, idToUnfollow):
    """The user with id userId stops following the user with id idToUnfollow"""
    user = getUser(userId)
    userToUnfollow = getUser(idToUnfollow)

    user.suscriptions.remove(idToUnfollow)
    userToUnfollow.followers.remove(userId)
    user.put()
    userToUnfollow.put()

def doesUserFollow(userId, followedId):
    """return True if the user with id userId follows the user with id followedId"""
    user = getUser(userId)
    return (followedId in user.suscriptions)

def isUserFollowed(userId, followerId):
    """return True if the user with id userId is followed by the user with id followerId"""
    user = getUser(userId)
    return (followerId in user.followers)