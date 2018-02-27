from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import random
from userAccounts import DataLink


class BingBot:
    def __init__(self, id):
        self._url = "http://bing.com"
        self._id = id
        self.data = DataLink()

    def _signed_in(self, browser):
        if(browser.find_element_by_id("id_s").is_displayed()):
            return True
        else:
            return False

    def log_in(self, browser, mobile = False):

        login = self.data.getLogin(self._id)
        email = (By.ID, "i0116")
        password = (By.ID, "i0118")
        button = (By.ID, "idSIButton9")

        if mobile:
            WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.ID, "mHamburger"))).click()
            WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "#HBSignIn > a:nth-child(1)"))).click()
        else:
            WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.ID, "id_l"))).click()

        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(email)).send_keys(login[0])
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(button)).click()

        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(password)).send_keys(login[1])
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(button)).click()

    def find_term(self, browser):
        try:
            links = browser.find_elements_by_xpath("//ol[@id='b_results']//li[@class='b_algo']//h2//a//strong")
            link_text = []
            for l in links:
                link_text.append(l.text)
            return random.choice(link_text)
        except Exception:
            terms = ["Portland", "c# vs java", "Microsoft", "c reference", "matplotlib docs", "gitkraken not working", "vscode c# formatting", "coach", "legacy", "tyrant", "Trump", "how to make a bot that writes"]
            return random.choice(terms)

    def search(self, browser, term):
        search_box = (By.ID, "sb_form_q")
        WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(search_box)).send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
        WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(search_box)).send_keys(term, Keys.ENTER)

    def desktop(self):
        options = Options()
        options.add_argument('-headless')
        browser = webdriver.Firefox()
        while(True):
            try:
                browser.get(self._url)
                if (not self._signed_in(browser)):
                        self.log_in(browser)
                        break
            except Exception:
                browser.quit()
                browser = webdriver.Firefox()
                continue
        term = ""
        i = 0
        while(i < 40):
            time.sleep(0.5)
            while(True):
                temp = self.find_term(browser)
                if (temp != term):
                    term = temp
                    break
            time.sleep(1)
            self.search(browser, term)
            i += 1
        browser.quit()
        print('success')

    def mobile(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', "Apple iPhone 6s")
        options = Options()
        options.add_argument('-headless')
        browser = webdriver.Firefox(profile, firefox_options=options)
        while(True):
            try:
                browser.get(self._url)
                self.log_in(browser, mobile=True)
                break
            except Exception:
                browser.quit()
                browser = webdriver.Firefox(profile, firefox_options=options)
                continue
        term = ""
        i = 0
        while(i < 30):
            try:
                time.sleep(1)
                while(True):
                    temp = self.find_term(browser)
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