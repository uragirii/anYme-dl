# This file is created for doenloading episodes from chia-anime.tv.
# Trying to fix ISSC001 - Animeheaven has a daily limit.

import requests
import time
import os
import zipfile
import sys
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import lxml

# In  this I'll start with class only,

# step1 - Search animes : complete

BASE_URL = r'http://ww2.chia-anime.tv/'
SEARCH_URL = BASE_URL + r'search/'

def anime_search(query: str):
    search_query = query.replace(" ", '%')
    search_url = SEARCH_URL + search_query

    search_page = requests.get(search_url)
    search_soup = BeautifulSoup(search_page.text, 'lxml')

    list_of_animes = []

    for anime_link in search_soup.find_all(class_="title"):
        if not anime_link.a in list_of_animes:
            list_of_animes.append(anime_link.a)

    print("The search results are:")
    for anime_link, num in zip(list_of_animes, range(len(list_of_animes))):
        print("[{}] {}".format(num+1, anime_link.text))

    while True:
        choice = int(input("Enter your preferred anime\n"))
        if not 0 < choice <= len(list_of_animes):
            print("Enter a valid choice between 1 and {}".format(len(list_of_animes)))
        else:
            break

    return list_of_animes[choice-1].text, list_of_animes[choice-1]['href']


# step 2  _ get all the details an d info about anime.




