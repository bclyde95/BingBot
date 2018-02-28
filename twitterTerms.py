import tweepy
from userAccounts import DataLink
import re

class TweetTerms:
    def __init__(self):
        """Gets auth info from db and initializes the API"""
        data = DataLink()
        login = data.getTwitterLogin()
        auth = tweepy.OAuthHandler(login[0], login[1])
        auth.set_access_token(login[2], login[3])
        self.api = tweepy.API(auth)

    def getHomeTweets(self):
        terms = []
        for t in tweepy.Cursor(self.api.home_timeline).items(10):
            shortened = re.sub(r"[^\s\w]",'',t.text[0:t.text.find("http")])
            searchTerms = re.findall("[^\s]+\s[^\s]+", shortened)
            terms.append(searchTerms)
        return terms
