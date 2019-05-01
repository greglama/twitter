import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from user_CRUD import User_CRUD

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class OtherProfile(webapp2.RequestHandler):

    FOLLOW = "Follow"
    UNFOLLOW = "Unfollow"
    userCrud = User_CRUD()

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        logout_url = users.create_logout_url(self.request.uri)
        user_twitter = None

        if user != None:
            # get the user twitter
            user_twitter = self.userCrud.getUser(user.user_id())

        # redirect toward login if no user
        if user_twitter == None:
            self.redirect("/")

        # fulfill the template and display the html
        else:
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
        
        # TODO refactor this whole thing... inheritence --------------------
        user = users.get_current_user()
        logout_url = users.create_logout_url(self.request.uri)
        user_twitter = None

        if user != None:
            # get the user twitter
            user_twitter = self.userCrud.getUser(user.user_id())

        # redirect toward login if no user
        if user_twitter == None:
            self.redirect("/")

        #--------------------

        profileId = self.request.get('profileId')

        if self.request.get('followUnfollow') == self.FOLLOW:
            self.userCrud.userStartFollowing(user_twitter.key.id(), profileId)

        if self.request.get('followUnfollow') == self.UNFOLLOW:
            self.userCrud.userStopToFollow(user_twitter.key.id(), profileId)
        
        self.redirect("/otherProfile?profileId=" + profileId)