# This is the test file created for working on a different site than before.
# Gogo anime faces some problems and animeheaven doesnot. It but prevents from multiple downloading of data

import requests
import time
import os
from bs4 import BeautifulSoup
from requests import Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys



USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'

SEARCH_URL = r'http://animeheaven.eu/search.php?q='


def anime_search(query: str):
    if query is None:
        raise ValueError
    else:
        search_query = query.replace(" ", "+")
        search_url = SEARCH_URL+search_query

        search_page = requests.get(search_url)
        search_soup = BeautifulSoup(search_page.text, "lxml")
        for x in search_soup.find_all(class_="cona"):
            print(x.text)
            print(x['href'])


def is_downloadable(url:str):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

print(is_downloadable(r'http://s5vkxea.animeheaven.eu/720kl/msl/Re_ZERO_-Break_Time_from_Zero---1--1461571001__35d8e5.mp4?dd5d157'))
# anime_search("re zero")
# Testing if i need selenium for this or not.
anime_url = r'http://animeheaven.eu/watch.php?a=Re%20ZERO%20-Break%20Time%20from%20Zero-&e=1'
options = Options()
options.headless = True
chrome_driver = r'C:/Users/apoor/Drivers/chromedriver.exe'
driver = webdriver.Chrome(chrome_driver,chrome_options=options)
driver.get(anime_url)
print("Sleep")
time.sleep(3)
print("Sleep off")
inner_html = driver.execute_script("return document.body.innerHTML")
htmlElem = BeautifulSoup(inner_html,'lxml')
