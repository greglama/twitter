import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from firstLogin import FirstLogin
from profile import Profile
from editProfile import EditProfile
from postTweet import PostTweet
from searchEngine import SearchEngine

from user_CRUD import User_CRUD

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Main(webapp2.RequestHandler):
    userCrud = User_CRUD()
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        # if the user is connected
        if user != None:
            # if it is the first connexion
            if not self.userCrud.existsUser(user.user_id()):
                # if yes go to first connexion
                self.redirect("/firstLogin")

            # else go to user profile
            else:
                self.redirect("/profile")
        # else he isn't connected go to the login page
        else:
            self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
    ('/', Main),
    ('/firstLogin',FirstLogin),
    ('/profile', Profile),
    ('/editProfile', EditProfile),
    ('/postTweet', PostTweet),
    ('/searchEngine', SearchEngine)
], debug=True)