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
BASE_URL = r'http://animeheaven.eu/'

"""
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
"""

# step 1 _ anime search: complete


def anime_search(query: str):
    if query is None:
        raise ValueError
    else:
        search_query = query.replace(" ", "+")
        search_url = SEARCH_URL+search_query

        search_page = requests.get(search_url)
        search_soup = BeautifulSoup(search_page.text, "lxml")

        list_of_animes = []

        for anime_link in search_soup.find_all(class_ = "cona"):
            if not anime_link in list_of_animes:
                list_of_animes.append(anime_link)
        print("The search results are :")
        for anime_link,num in zip(list_of_animes, range(0, len(list_of_animes))):
            print("[{0}] {1}".format(num+1, anime_link.text))

        choice = int(input("Enter your preferred anime\n"))

        # TODO : Check boundary condition for choice variable

        return list_of_animes[choice-1].text, list_of_animes[choice-1]['href']


# Step 2 _ get all the episode number and there links (hopefully)


def episodes_available(anime_link: str):

    anime_page = requests.get(anime_link)
    anime_soup = BeautifulSoup(anime_page.text, "lxml")

    total_ep = len(anime_soup.find_all(class_= "centerv"))//3

    print("Total available episodes : ", total_ep)
    return total_ep


print("Welcome to ALPHA phase of anime downloader")
print("Please make sure to report any problems faced\n\n")

anime_query: str = input("Enter the name of the anime you want search\n")
pref_anime, pref_anime_link = anime_search(anime_query)
pref_anime_link = BASE_URL + pref_anime_link

print("Anime Name : {0}".format(pref_anime))

pref_total_anime_ep = episodes_available(pref_anime_link)