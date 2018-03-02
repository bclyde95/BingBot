"""Provides functionality to automate bing searches and login"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import random
import re
from dataLink import DataLink
from twitterTerms import TweetTerms



class BingBot:
    """A class to automate interactions with Bing. Includes login, semi-autonomous search (terms need to be input), and fully autonomous desktop and mobile search for rewards points"""

    def __init__(self, id):
        """Constructor for BingBot. Initializes the url, id, Datalink and TweetTerms classes, and generates the twitter search terms"""

        self._url = "http://bing.com"
        self._id = id
        self.data = DataLink()
        self.twitter = TweetTerms()
        self.terms = self.twitter.getHomeTweets()

    def _signed_in(self, browser):
        """Checks if signed in by checking if the 'sign in' text is displayed."""

        if(browser.find_element_by_id("id_s").is_displayed()):
            return False
        else:
            return True

    def _log_in(self, browser, mobile = False):
        """The functionality of the public log_in() function"""

        # Store the login data and the webpage elements
        login = self.data.getLogin(self._id)
        desktop_signin = (By.ID, "id_l")
        mobile_menu = (By.ID, "mHamburger")
        mobile_signin = (By.CSS_SELECTOR, "#HBSignIn > a:nth-child(1)")
        email = (By.ID, "i0116")
        password = (By.ID, "i0118")
        button = (By.ID, "idSIButton9")

        if mobile:
            # Expand mobile menu and click the sign in button
            WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(mobile_menu)).click()
            WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(mobile_signin)).click()
        else:
            # Click the sign in button
            WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(desktop_signin)).click()

        # Fill email field and click the submit button
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(email)).send_keys(login["email"])
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(button)).click()

        # Fill the password field and click the submit button
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(password)).send_keys(login["password"])
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(button)).click()

    def log_in(self, mobile = False, headless=False):
        """Automates the sign in click and login screens. 'mobile' mode when mobile=False"""

        options = Options()
        options.add_argument('-headless')
        if (mobile):
            profile = webdriver.FirefoxProfile()
            profile.set_preference('general.useragent.override', "Apple iPhone 6s")
            if (headless):
                browser = webdriver.Firefox(profile, options=options)
            else:
                browser = webdriver.Firefox(profile)
        else:
            if (headless):
                browser = webdriver.Firefox(options=options)
            else:
                browser = webdriver.Firefox()
        if (mobile):
            while(True):
                try:
                    browser.get(self._url)
                    self._log_in(browser, mobile=True)
                    break
                except Exception:
                    browser.quit()
                    if (headless):
                        browser = webdriver.Firefox(profile, options=options)
                    else:
                        browser = webdriver.Firefox(profile)
                    continue
        else:
            while(True):
                try:
                    browser.get(self._url)
                    if (self._signed_in(browser)):
                        self._log_in(browser)
                        break
                except Exception:
                    browser.quit()
                    if (headless):
                        browser = webdriver.Firefox(options=options)
                    else:
                        browser = webdriver.Firefox()
                    continue
        return browser

    def _find_term(self, browser):
        """Selects search terms from the links in the search results, pulling from a list if the terms to start and to avoid an endless loop"""

        try:
            time.sleep(0.5)
            links = browser.find_elements_by_xpath("//ol[@id='b_results']//li[@class='b_algo']//h2//a")
            link_text = []
            for l in links:
                shortened = re.sub(r"[^\s\w]",'',l.text)
                searchTerms = re.findall(r"[^\s]+\s[^\s]+", shortened)
                link_text.append(searchTerms)
            return random.choice(link_text[random.randint(0,len(link_text))])
        except Exception:
            return random.choice(self.terms[random.randint(0,9)])

    def search(self, browser, term):
        """Automates the search functionality, clearing the text box before each new search"""

        search_box = (By.ID, "sb_form_q")
        WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(search_box)).send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
        WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(search_box)).send_keys(term, Keys.ENTER)

    def desktop(self):
        # *** NEED TO TEST ***
        """The automation function for maxing out desktop points"""

        browser = self.log_in(headless=True)
        term = ""
        points = int(WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable((By.ID, "id_rc"))).text)
        pointGoal = points + 150
        while(points <= pointGoal):
            time.sleep(0.5)
            points = int(WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable((By.ID, "id_rc"))).text)
            while(True):
                temp = self._find_term(browser)
                if (temp != term):
                    term = temp
                    break
            time.sleep(1)
            self.search(browser, term)
            time.sleep(0.5)
        self.data.setPoints(id, points)
        browser.quit()
        print(self.data.getLogin(id)[0],'Desktop :', self.data.getPoints(id))

    def mobile(self):
        # *** IN PROGRESS ***
        """The automation function for maxing out mobile points"""
        
        browser = self.log_in(mobile=True, headless=True)
        term = ""
        i = 0
        while(i < 30):
            try:
                time.sleep(1)
                while(True):
                    temp = self._find_term(browser)
                    if (temp != term):
                        term = temp
                        break
                time.sleep(1)
                self.search(browser, term)
                i += 1
            except Exception:
                alert = browser.switch_to_alert()
                alert.accept()
                continue
        browser.quit()
        print('success')
