from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


profile = webdriver.FirefoxProfile()
profile.set_preference('general.useragent.override', "Apple iPhone 6s")

browser = webdriver.Firefox(profile)

browser.get("https://www.bing.com")

signIn = (By.CSS_SELECTOR, "#HBSignIn > a:nth-child(1)")

WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.ID, "mHamburger"))).click()
WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "#HBSignIn > a:nth-child(1)"))).click()


# points = int(WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable((By.ID, "id_rc"))).text)
#     while(points < points+150):
#         time.sleep(0.5)
#         points = int(WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable((By.ID, "id_rc"))).text)
#         while(True):
#             temp = find_term(browser)
#             if (temp != term):
#                 term = temp
#                 break
#         time.sleep(1)
#         search(browser, term)