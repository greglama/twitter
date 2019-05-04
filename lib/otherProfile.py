import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from twitterBaseHandler import TwitterBaseHandler

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
        profile = self.userCrud.getUser(profileId)

        # get the profile and its tweets
        tweets = self.userCrud.getAllTweetsOfUser(profileId) #tweets of the profile to see

        follow_unfollow = self.FOLLOW

        # if the profile is already followed
        if self.userCrud.isUserFollowed(profileId, user_twitter_id):
            follow_unfollow = self.UNFOLLOW

        
        template_values = {
            "userName": profile.name,
            "userPseudo": profile.pseudo,
            "profileId" : profileId,
            "logout_url": logout_url,
            "list_tweet" : tweets,
            "follow_unfollow": follow_unfollow
        }

        self.sendHTMLresponse(template_values, '/template/otherProfile.html')
    
    def post(self):

        # TODO refactor here

        # get the user (redirect if None)        
        user_twitter = self.getCurrentTwitterUser()

        #get IDs of both parties 
        user_twitter_id = user_twitter.key.id()
        profileId = self.request.get('profileId')

        #if he is following then we want to unfollow
        if self.request.get('followUnfollow') == self.FOLLOW:
            self.userCrud.userStartFollowing(user_twitter_id, profileId)

        # and vice-versa
        if self.request.get('followUnfollow') == self.UNFOLLOW:
            self.userCrud.userStopToFollow(user_twitter_id, profileId)
        
        self.redirect("/otherProfile?profileId=" + profileId)