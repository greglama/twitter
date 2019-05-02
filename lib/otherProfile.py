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
        self.response.headers['Content-Type'] = 'text/html'

        logout_url = self.getLogoutUrl()
        
        user_twitter = self.getCurrentUserOrRedirect()

        profileId = self.request.get('profileId') # id of profile to see
        user_twitter_id = user_twitter.key.id() # id of current user

        # get the profile and its tweets
        profile = self.userCrud.getUser(profileId)
        tweets = self.userCrud.getAllTweetsOfUser(profileId)

        follow_unfollow = self.FOLLOW

        # if the profile is already followed
        if self.userCrud.isUserFollowed(profileId, user_twitter_id):
            follow_unfollow = self.UNFOLLOW

        
        template_values = {
            "userName": profile.name,
            "userPseudo": profile.pseudo,
            "logout_url": logout_url,
            "list_tweet" : tweets,
            "profileId" : profileId,
            "follow_unfollow": follow_unfollow
        }

        template = JINJA_ENVIRONMENT.get_template('/template/otherProfile.html')
        self.response.write(template.render(template_values))
    
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # get the user (redirect if None)        
        user_twitter = self.getCurrentUserOrRedirect()

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