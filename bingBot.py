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
            return True
        else:
            return False

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
        """Automates the sign in click and login screens. 'mobile' mode when mobile=True"""

        # Add headless option
        options = Options()
        options.add_argument('-headless')

        if (mobile):
            # create Firefox profile with an Iphone 6 as the user agent
            profile = webdriver.FirefoxProfile()
            profile.set_preference('general.useragent.override', "Apple iPhone 6s")

            if (headless):
                # if headless, create webdriver with the data for headless and mobile
                browser = webdriver.Firefox(profile, options=options, executable_path="./geckodriver")
            else:
                # if not, create webdriver with only the data for mobile
                browser = webdriver.Firefox(profile, executable_path="./geckodriver")
        else:
            if (headless):
                # if headless, create webdriver with data for headless
                browser = webdriver.Firefox(options=options, executable_path="./geckodriver")
            else:
                # if not, create webdriver normally
                browser = webdriver.Firefox(executable_path="./geckodriver")
        if (mobile):
            while(True):
                try:
                    # load the webpage and login. if successful, break the loop
                    browser.get(self._url)
                    self._log_in(browser, mobile=True)
                    break
                except Exception:
                    # if login fails, quit the current browser instance and open the correct new one
                    browser.quit()
                    if (headless):
                        browser = webdriver.Firefox(profile, options=options, executable_path="./geckodriver")
                    else:
                        browser = webdriver.Firefox(profile, executable_path="./geckodriver")
                    continue
        else:
            while(True):
                try:
                    # load the webpage, check if signed in. if not, login. if successful break the loop
                    browser.get(self._url)
                    if (not self._signed_in(browser)):
                        self._log_in(browser)
                        break
                except Exception:
                    # if login fails, quit the current browser instance and open the correct new one
                    browser.quit()
                    if (headless):
                        browser = webdriver.Firefox(options=options, executable_path="./geckodriver")
                    else:
                        browser = webdriver.Firefox(executable_path="./geckodriver")
                    continue
        return browser

    def _find_term(self, browser):
        """Selects search terms from the links in the search results, pulling from a list if the terms to start and to avoid an endless loop"""

        try:
            time.sleep(0.5)
            # get all of the search result links on the page
            links = browser.find_elements_by_xpath("//ol[@id='b_results']//li[@class='b_algo']//h2//a")
            link_text = []
            for l in links:
                # remove anything that is not a space or a word from the string
                shortened = re.sub(r"[^\s\w]",'',l.text)
                # make terms from two words separated by a space
                searchTerms = re.findall(r"[^\s]+\s[^\s]+", shortened)
                # add search terms to the link_text list
                link_text.append(searchTerms)
            # pick a random search term and return it
            return random.choice(link_text[random.randint(0,len(link_text))])
        except Exception:
            # if picking from the webpage fails, randomly pick from terms generated from twitter data
            term = ""
            while True:
                try:
                    term = random.choice(self.terms[random.randint(0,14)])
                    break
                except IndexError:
                    continue
            return term

    def search(self, browser, term):
        """Automates the search functionality, clearing the text box before each new search"""

        # select search box
        search_box = (By.ID, "sb_form_q")
        # select all pre-existing text and delete it
        WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(search_box)).send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
        # input term into search box and hit enter
        WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(search_box)).send_keys(term, Keys.ENTER)

    def desktop(self):
        """The automation function for maxing out desktop points"""

        # start headless browser and login
        while True:
            try:
                browser = self.log_in(headless=True)
                break
            except Exception:
                continue
        

        term = ""
        i = 0

        # 5 points are earned per search with a max of 150 on desktop. it iterates 35 times to account for possible repeats
        while(i < 35):
            time.sleep(0.5)

            while(True):
                # finds term from page or twitter
                temp = self._find_term(browser)
                # if current term does not equal previous term, store temp in term and exit loop.
                # if not, generate another term
                if (temp != term):
                    term = temp
                    break
            time.sleep(1)
            # search using the generated term
            self.search(browser, term)
            time.sleep(0.5)

            # iterate counter
            i += 1

        # if points are lower than previously stored, the user must have redeemed some.
        # if true, increment timesRedeemed in database by 1
        points = int(WebDriverWait(browser,10).until(expected_conditions.visibility_of_element_located((By.ID, "id_rc"))).text)
        if (int(points) < self.data.getPoints(self._id)):
            self.data.setTimes(self._id, self.data.getTimes(self._id) + 1)

        # set points in database to current points
        self.data.setPoints(self._id, points)

        # quit browser and output account and current points to console
        browser.quit()
        print(self.data.getLogin(self._id)["email"],'Total Points :', self.data.getPoints(self._id))

    def mobile(self):
        """The automation function for maxing out mobile points"""
        # start headless, mobile browser and login
        while True:
            try:
                browser = self.log_in(mobile=True, headless=True)
                break
            except Exception:
                continue
        
        
        term = ""
        i = 0

        # 5 points are earned per search with a max of 100 on mobile. it iterates 25 times to account for possible repeats
        while(i < 25):
            try:
                time.sleep(1)
                while(True):
                    # if current term does not equal previous term, store temp in term and exit loop.
                    # if not, generate another term
                    temp = self._find_term(browser)
                    if (temp != term):
                        term = temp
                        break
                time.sleep(1)
                # search using the generated term
                self.search(browser, term)

                # iterate counter
                i += 1
            except Exception:
                # if a popup asking for location occurs, switch to the alert and accept it
                try:
                    alert = browser.switch_to_alert()
                    alert.accept()
                    continue
                except Exception:
                    continue

        # reload the page, open mobile menu and get points value
        browser.get(self._url)
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.ID, "mHamburger"))).click()
        points = WebDriverWait(browser, 10).until(expected_conditions.visibility_of_element_located((By.ID, "fly_id_rc"))).text

        # if points are lower than previously stored, the user must have redeemed some.
        # if true, increment timesRedeemed in database by 1
        if (int(points) < self.data.getPoints(self._id)):
            self.data.setTimes(self._id, self.data.getTimes(self._id) + 1)

        # set points in database to current points
        self.data.setPoints(self._id, int(points))

        # quit browser and output account and current points to console
        browser.quit()
        print(self.data.getLogin(self._id)["email"], 'Total Points :', self.data.getPoints(self._id))
