import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from twitterBaseHandler import TwitterBaseHandler

from crud.user_CRUD import getUser, isUserFollowed, userStartFollowing, userStopToFollow
from crud.tweets_CRUD import getAllTweetsOfUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class OtherProfile(TwitterBaseHandler):

    FOLLOW = "Follow"
    UNFOLLOW = "Unfollow"

    def get(self):
        self.redirectIfNotConnected()
        logout_url = self.getLogoutUrl()

        user_twitter = self.getCurrentTwitterUser()
        user_twitter_id = user_twitter.key.id() # id of current user

        profileId = self.request.get('profileId') # id of profile to see
        profile = getUser(profileId)

        # if the user is visiting its own profile through the search tool
        if profileId == user_twitter_id:
            self.redirect("/profile", True, True) #redirect him to his profile

        # get the profile and its tweets
        tweets = getAllTweetsOfUser(profileId) #tweets of the profile to see

        
        follow_unfollow = OtherProfile.FOLLOW

        # if the visited profile is already followed
        if isUserFollowed(profileId, user_twitter_id):
            follow_unfollow = OtherProfile.UNFOLLOW #sugest to unfollow

        template_values = {
            "userName": profile.name,
            "userPseudo": profile.pseudo,
            "description": profile.description,
            "profileId" : profileId,
            "logout_url": logout_url,
            "list_tweet" : tweets,
            "follow_unfollow": follow_unfollow
        }

        self.sendHTMLresponse(template_values, OtherProfile.TEMPLATE_TO_RENDER)
    
    def post(self):
        self.redirectIfNotConnected()

        user_twitter = self.getCurrentTwitterUser()

        #get IDs of both users 
        user_twitter_id = user_twitter.key.id()
        profileId = self.request.get('profileId')

        #follow or unfollow depending of the request
        if self.request.get('followUnfollow') == self.FOLLOW:
            userStartFollowing(user_twitter_id, profileId)

        if self.request.get('followUnfollow') == self.UNFOLLOW:
            userStopToFollow(user_twitter_id, profileId)
        
        self.redirect("/otherProfile?profileId=" + profileId)