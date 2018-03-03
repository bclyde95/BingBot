import tweepy
from dataLink import DataLink
import re

class TweetTerms:
    """Generates fairly useful search terms from tweets to feed to the bot when it when the majority of search results are similar"""
    def __init__(self):
        """Gets auth info from db and initializes the API"""
        data = DataLink()
        login = data.getTwitterLogin()
        auth = tweepy.OAuthHandler(login["consumer_key"], login["consumer_secret"])
        auth.set_access_token(login["access_token"], login["access_secret"])
        self.api = tweepy.API(auth)

    def getHomeTweets(self):
        """Gets 10 tweets from users homepage, removes all special characters, splits every two words, and returns a jagged list of two-word terms"""
        terms = []
        for t in tweepy.Cursor(self.api.home_timeline).items(10):
            shortened = re.sub(r"[^\s\w]",'',t.text[0:t.text.find("http")])
            searchTerms = re.findall(r"[^\s]+\s[^\s]+", shortened)
            terms.append(searchTerms)
        return terms
