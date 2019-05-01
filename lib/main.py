import webapp2

from login import Login
from firstLogin import FirstLogin
from profile import Profile
from editProfile import EditProfile
from postTweet import PostTweet
from searchEngine import SearchEngine
from otherProfile import OtherProfile
from timeLine import TimeLine

app = webapp2.WSGIApplication([
    ('/', Login),
    ('/firstLogin',FirstLogin),
    ('/profile', Profile),
    ('/editProfile', EditProfile),
    ('/postTweet', PostTweet),
    ('/searchEngine', SearchEngine),
    ('/otherProfile', OtherProfile),
    ('/timeLine', TimeLine)
], debug=True)