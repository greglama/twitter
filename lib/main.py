import webapp2
import logging
from login import Login
from firstLogin import FirstLogin
from profile import Profile
from editProfile import EditProfile
from postTweet import PostTweet
from searchEngine import SearchEngine
from otherProfile import OtherProfile
from timeLine import TimeLine
from editTweet import EditTweet

TEMPLATE_FOLDER = "/template/"

FirstLogin.set_template_to_render(TEMPLATE_FOLDER + 'login.html')
Profile.set_template_to_render(TEMPLATE_FOLDER + 'userProfile.html')
EditProfile.set_template_to_render(TEMPLATE_FOLDER + 'editProfile.html')
SearchEngine.set_template_to_render(TEMPLATE_FOLDER + 'searchResult.html')
OtherProfile.set_template_to_render(TEMPLATE_FOLDER + 'otherProfile.html')
TimeLine.set_template_to_render(TEMPLATE_FOLDER + 'timeLine.html')
EditTweet.set_template_to_render(TEMPLATE_FOLDER + 'editTweet.html')

app = webapp2.WSGIApplication([
    ('/', Login),
    ('/firstLogin',FirstLogin),
    ('/profile', Profile),
    ('/editProfile', EditProfile),
    ('/postTweet', PostTweet),
    ('/searchEngine', SearchEngine),
    ('/otherProfile', OtherProfile),
    ('/timeLine', TimeLine),
    ('/editTweet', EditTweet)
], debug=True)