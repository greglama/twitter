import webapp2
import logging

from lib.login import Login
from lib.firstLogin import FirstLogin
from lib.profile import Profile
from lib.editProfile import EditProfile
from lib.postTweet import PostTweet
from lib.searchEngine import SearchEngine
from lib.otherProfile import OtherProfile
from lib.timeLine import TimeLine
from lib.editTweet import EditTweet

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