from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import random

def signed_in(browser, mobile=False):
    if(browser.find_element_by_id("id_s").is_displayed()):
        return True
    else:
        return False

def log_in(browser, login, mobile = False):

    email = (By.ID, "i0116")
    password = (By.ID, "i0118")
    next = (By.ID, "idSIButton9")

    if mobile:
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.ID, "mHamburger"))).click()
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "#HBSignIn > a:nth-child(1)"))).click()
    else:
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.ID, "id_l"))).click()

    # wait for email field and enter email
    WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(email)).send_keys(login[0])

    # Click Next
    WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(next)).click()

    # wait for password field and enter password
    WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(password)).send_keys(login[1])

    # Click Login - same id?
    WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(next)).click()

def find_term(browser):
    try:
        links = browser.find_elements_by_xpath("//ol[@id='b_results']//li[@class='b_algo']//h2//a//strong")
        link_text = []
        for l in links:
            link_text.append(l.text)
        return random.choice(link_text)
    except Exception:
        terms = ["dragon", "apples", "water", "backpack", "egg", "gold", "strawberry", "couch"]
        return random.choice(terms)

def search(browser, term):
    search_box = (By.ID, "sb_form_q")
    WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(search_box)).send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
    WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(search_box)).send_keys(term, Keys.ENTER)

def desktop(url, login):
    options = Options()
    options.add_argument('-headless')
    browser = webdriver.Firefox()
    while(True):
        try:
            browser.get(url)
            if (not signed_in(browser)):
                    log_in(browser, login)
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
            temp = find_term(browser)
            if (temp != term):
                term = temp
                break
        time.sleep(1)
        search(browser, term)
        i += 1
    browser.quit()
    print('success')

def mobile(url, login):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('general.useragent.override', "Apple iPhone 6s")
    options = Options()
    options.add_argument('-headless')
    browser = webdriver.Firefox(profile, firefox_options=options)
    while(True):
        try:
            browser.get(url)
            log_in(browser, login, mobile=True)
            break
        except Exception:
            browser.quit()
            browser = webdriver.Firefox(profile, firefox_options=options)
            continue
    term = ""
    i = 0
    while(i < 30):
        time.sleep(1)
        while(True):
            temp = find_term(browser)
            if (temp != term):
                term = temp
                break
        time.sleep(1)
        search(browser, term)
        i += 1
    browser.quit()
    print('success')

def main():
    url = "http://www.bing.com"
    logins = [("bclyde9514@gmail.com", "November112015"),("cindycore27@yahoo.com", "2129Vineave"),("brandon.clyde@outlook.com", "November112015"),("cindycore27@outlook.com", "2129Vineave")]
    for l in logins:
        desktop(url,l)
        mobile(url, l)




if __name__ == "__main__":
    main()