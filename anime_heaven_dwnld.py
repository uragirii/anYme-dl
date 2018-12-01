# This is the test file created for working on a different site than before.
# Gogo anime faces some problems and animeheaven doesnot. It but prevents from multiple downloading of data

import requests
import time
import os
from bs4 import BeautifulSoup
import zipfile
import sys
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys



USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'

SEARCH_URL = r'http://animeheaven.eu/search.php?q='
BASE_URL = r'http://animeheaven.eu/'

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


def print_anime_details(anime_link: str):

    anime_page = requests.get(anime_link)
    anime_soup = BeautifulSoup(anime_page.text, "lxml")

    print('\n', list(anime_soup.find_all(class_="infodes2"))[0].text, '\n')


def reporthook(blocknum, blocksize, totalsize):
    """
    function copied from https://stackoverflow.com/questions/13881092/download-progressbar-for-python-3
    """
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = '\rPercentage : %5.1f%% (%*d MB out of  %d MB)' % (
            percent, len(str(totalsize)), readsofar//1048576, totalsize//1048576)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))


def download_file(url,filename,folder):
    print("Downloading file : " , filename)
    urlretrieve(url, os.path.join(folder,filename), reporthook)
    print("Download Complete")

print("Welcome to ALPHA phase of anime downloader")
print("Please make sure to report any problems faced\n\n")

if not os.path.exists("Files"):         # Will store the program files in this folder
    os.mkdir("Files")

anime_query: str = input("Enter the name of the anime you want search\n")
pref_anime, pref_anime_link = anime_search(anime_query)
pref_anime_link = BASE_URL + pref_anime_link

print("Anime Name : {0}".format(pref_anime))

print_anime_details(pref_anime_link)

pref_total_anime_ep = episodes_available(pref_anime_link)

# I will only initialize chrome driver once and it will be used everywhere

options = Options()
options.add_argument('log-level=3')
options.headless = True
chrome_driver = r'./Files/chromedriver.exe'
if not os.path.exists(chrome_driver):
    print("Chrome driver does not exist. Downloading it and saving in {Files} folder")
    # TODO Downlaod chrome driver for platform specific
    download_file("https://chromedriver.storage.googleapis.com/2.44/chromedriver_win32.zip", "chromedriver.zip", "Files")
    print("Extracting components")
    with zipfile.ZipFile(os.path.join("Files","chromedriver.zip"), "r") as zip_ref:
        zip_ref.extractall("./Files")
    print("Complete.")


driver = webdriver.Chrome(chrome_driver, chrome_options=options)

print("Getting all the episodes links:")
driver.get(pref_anime_link)
time.sleep(3)
inner_html = driver.execute_script("return document.body.innerHTML")
anime_page_soup = BeautifulSoup(inner_html, 'lxml')
anime_ep_links = []
for link in anime_page_soup.find_all(class_="infovan"):
    anime_ep_links.append(BASE_URL+link['href'])

anime_ep_links = anime_ep_links[::-1]   # Episodes are displayed in reverse order

# Step 3 _Begin  downloading the anime episodes
# By default will save episodes in ./{anime-name}/
print("Saving the episodes in the directory ./{0}/".format(pref_anime))
if not os.path.exists(pref_anime):
     os.mkdir(pref_anime)

for epi in range(pref_total_anime_ep):
    print("Downloading episode num {0} from {1} :".format(epi+1, pref_total_anime_ep))
    driver.get(anime_ep_links[epi])
    time.sleep(3)
    inner_html = driver.execute_script("return document.body.innerHTML")
    epi_soup = BeautifulSoup(inner_html, 'lxml')
    # ERRC002 Abuse Protection

    for abuse in epi_soup.find_all(class_='now2'):
        if 'abuse protection' in abuse.text:
            print("Triggered Abuse Protection, waiting for 60 seconds")
            time.sleep(60)
            driver.get(anime_ep_links[epi])
            time.sleep(3)
            inner_html = driver.execute_script("return document.body.innerHTML")
            epi_soup = BeautifulSoup(inner_html, 'lxml')
            break

    dwnld_lnk = list(epi_soup.find_all(class_='an'))[0]['href']
    filename = pref_anime + " Ep " + str(epi+1) + ".mp4"
    download_file(dwnld_lnk,filename,pref_anime)
driver.close()