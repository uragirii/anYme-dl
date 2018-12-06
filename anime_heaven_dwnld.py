# This is the test file created for working on a different site than before.
# Gogo anime faces some problems and animeheaven doesnot. It but prevents from multiple downloading of data

import requests
import time
import os
#import pickle
import zipfile
import sys
from urllib.request import urlretrieve
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup
    import lxml
except ImportError:
    import pip
    try:
        print("Installing Requirements for program.")
        pip.main(['install', 'selenium'])
        pip.main(['install', 'beautifulsoup4'])
        pip.main(['install', 'lxml'])
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.keys import Keys
        from bs4 import BeautifulSoup
    except SystemExit as e:
        print("Couldn't install the requirements. Please install selenium and beautifulsoup4 modules manually.")

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227' \
             '.1 Safari/537.36'

SEARCH_URL = r'http://animeheaven.eu/search.php?q='
BASE_URL = r'http://animeheaven.eu/'


# step 1 _ anime search: complete


def anime_search(query: str):
    if query is None:
        raise ValueError
    else:
        search_query = query.replace(" ", "+")
        search_url = SEARCH_URL + search_query

        search_page = requests.get(search_url)
        search_soup = BeautifulSoup(search_page.text, "lxml")

        list_of_animes = []

        for anime_link in search_soup.find_all(class_="cona"):
            if anime_link not in list_of_animes:
                list_of_animes.append(anime_link)

        # TODO : check condition for zero search results

        print("The search results are :")

        for anime_link, num in zip(list_of_animes, range(0, len(list_of_animes))):
            print("[{0}] {1}".format(num + 1, anime_link.text))

        while True:
            choice = int(input("Enter your preferred anime\n"))
            if not 0 < choice <= len(list_of_animes):
                print("Enter a valid choice between 1 and {}".format(len(list_of_animes)))
            else:
                break

        return list_of_animes[choice - 1].text, list_of_animes[choice - 1]['href']


# Step 2 _ get all the episode number and there links (hopefully) : complete


def reporthook(blocknum, blocksize, totalsize):
    """
    function copied from https://stackoverflow.com/questions/13881092/download-progressbar-for-python-3
    """
    global start_time
    if blocknum==0:
        start_time = time.time()
        return
    if totalsize > 0:
        duration = time.time() - start_time
        readsofar = blocknum * blocksize
        if duration == 0:
            duration+=0.001
        speed = int(readsofar / (1024 * duration))
        percent = readsofar * 1e2 / totalsize
        s = '\rPercentage : %5.1f%% (%5.2f MB out of %d MB, Download Speed %d KB/s, %d seconds passed )' % (
            percent, readsofar / 1048576, totalsize // 1048576, speed, duration)
        sys.stderr.write(s)
        if readsofar >= totalsize:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))


def download_file(url, filename, folder):
    print("Downloading file : ", filename)
    urlretrieve(url, os.path.join(folder, filename), reporthook)
    print("Download Complete")
    return True


# Next step Implement same by Anime class


class Anime:
    def __str__(self):
        return self.about

    def __init__(self, name, url):
        self.name: str = name
        self.url: str = url
        self.episodes_avail: int = 0
        self.about: str = ""
        self.episodes_dwnld: list = []  # List containing all the downloaded episodes
        # THE FOLLOWING FEATURE HAS BEEN SUSPENDED AS OF NOW @00-15-2018-12-07
        # self.ongoing: bool = False
        # self.follow: bool = False
        # self._check_ongoing()
        self.episodes_link: list = []

    def _check_ongoing(self):           # This function although is kept as it does not effect
        anime_page = requests.get(self.url)
        anime_soup = BeautifulSoup(anime_page.text, "lxml")

        for status in anime_soup.find_all(class_='textc'):
            if 'Ongoing' in status.text:
                self.ongoing = True
                break
        self.about = str(list(anime_soup.find_all(class_="infodes2"))[0].text)

    def update_avail_ep(self):
        anime_page = requests.get(self.url)
        anime_soup = BeautifulSoup(anime_page.text, "lxml")
        self.episodes_avail = len(anime_soup.find_all(class_="centerv")) // 3

    def check_new_episode(self):
        self.update_avail_ep()
        if max(self.episodes_dwnld) < self.episodes_avail:
            print("{1} new episode(s) out for anime {0}".format(self.name,
                                                                self.episodes_avail - max(self.episodes_dwnld)))
            # Todo implement auto download or not
            return True
        else:
            return False

    def dwnld_range(self, lowest: int, highest: int, cdriver):
        # Assuming that boundary condition have been checked
        for _epi in range(lowest, highest):
            if not self.dwnld_single(_epi, driver):
                break

    def dwnld_single(self, epi_num: int, cdriver):
        # Assuming boundary conditions are checked
        try:
            print("Downloading Episode num : {} | Total Available episodes : {}".format(epi_num, self.episodes_avail))
            driver.get(self.episodes_link[epi_num])
            time.sleep(3)
            inner_html = driver.execute_script("return document.body.innerHTML")
            epi_soup = BeautifulSoup(inner_html, 'lxml')
            # ERRC002 Abuse Protection
            for abuse in epi_soup.find_all(class_='now2'):
                if 'abuse protection' in abuse.text:
                    print("Triggered Abuse Protection, waiting for 60 seconds")
                    time.sleep(60)
                    driver.get(anime_ep_links[epi_num - 1])
                    time.sleep(3)
                    inner_html = driver.execute_script("return document.body.innerHTML")
                    epi_soup = BeautifulSoup(inner_html, 'lxml')
                    break
            while True:
                for abuse in epi_soup.find_all(class_='now2'):
                    if 'abuse protection' in abuse.text:
                        print("Again Triggered. Please close any browser window opening Animeheaven.eu site")
                        print('Waiting for another 60 seconds')
                        time.sleep(60)
                        driver.refresh()
                        time.sleep(3)
                        inner_html = driver.execute_script("return document.body.innerHTML")
                        epi_soup = BeautifulSoup(inner_html, 'lxml')
                abuse_counter = False
                for abuseagain in epi_soup.find_all(class_='now2'):
                    if 'abuse protection' in abuse.text:
                        abuse_counter = True
                        print("Again waiting..")
                        time.sleep(60)
                        driver.refresh()
                        time.sleep(3)
                        inner_html = driver.execute_script("return document.body.innerHTML")
                        epi_soup = BeautifulSoup(inner_html, 'lxml')

                if not abuse_counter:
                    break

            # ReinforcedPanda (Github username is finding Issue here gotta fix that.
            # https://github.com/uragirii/anYme-dl/issues/1
            # Maybe fixed

            dwnld_lnk = list(epi_soup.find_all(class_='an'))[0]['href']
            filename = "{} Ep {}.mp4".format(anime.name, epi_num)

            dwnld_status = download_file(dwnld_lnk, filename, anime.name)
            if dwnld_status:
                self.episodes_dwnld.append(epi_num)
            else:
                return False

        except Exception as e:
            print("Error Occured!! Downloading Stopped.")
            print(e)
        return True


# ------------------------------ MAIN PROGRAM -----------------------------
print("Welcome to BETA phase of anime downloader")
print("Please make sure to report any problems faced\n\n")

# THIS PART IS AT HALT
"""
anime_data = {}
anime_data['followed'] = []
anime_data['searched'] = []
if not os.path.exists("Files"):  # Will store the program files in this folder
    os.mkdir("Files")
if not os.path.exists(os.path.join("Files", "anime_data")):
    pic = open(os.path.join("Files", "anime_data"), 'wb')
    pickle.dump(anime_data, pic)
    pic.close()
else:
    pic = open(os.path.join("Files", "anime_data"), 'r')
    anime_data = pickle.load(pic)
    for ani in anime_data['followed']:
        print(ani.name)
"""
anime_query: str = input("Enter the name of the anime you want search\n")
pref_anime, pref_anime_link = anime_search(anime_query)
pref_anime_link = BASE_URL + pref_anime_link

anime = Anime(pref_anime, pref_anime_link)
print("Anime Name : {}".format(anime.name))
print(anime)
anime.update_avail_ep()
print("Total Episodes Available : {}".format(anime.episodes_avail))
# HALTED CODE
"""
if anime.ongoing:
    choice = input("{} is not a complete anime.Do you want to follow this anime to automatically check for new episodes"
                   "next time you run the program?[Y/N]".format(anime.name))
    if choice == 'Y':
        anime.follow = True
        print("You are now following {}".format(anime.name))
"""
# I will only initialize chrome driver once and it will be used everywhere
# As it will save time and memory

# ------------------------- Initialize Chrome Driver --------------------------------------------
options = Options()
options.add_argument('log-level=3')
options.headless = True
chrome_driver = r'./Files/chromedriver.exe'
# For linux based ^ path will not contain '.exe', for Mac OS yet to check
if not os.path.exists(chrome_driver):
    print("Chrome driver does not exist. Downloading it and saving in {Files} folder")
    # TODO Download chrome driver for platform specific
    # check using sys.platform, win32, linux, darwin
    download_file("https://chromedriver.storage.googleapis.com/2.44/chromedriver_win32.zip", "chromedriver.zip",
                  "Files")
    print("Extracting components")
    with zipfile.ZipFile(os.path.join("Files", "chromedriver.zip"), "r") as zip_ref:
        zip_ref.extractall("./Files")
    print("Complete.")

driver = webdriver.Chrome(chrome_driver, chrome_options=options)

print("Getting all the episodes links:")
driver.get(anime.url)
time.sleep(3)
inner_html = driver.execute_script("return document.body.innerHTML")
anime_page_soup = BeautifulSoup(inner_html, 'lxml')
anime_ep_links = []             # todo implement this using class functions
# Todo  before checking with online make anime != ongoing and also database
for link in anime_page_soup.find_all(class_="infovan"):
    anime_ep_links.append(BASE_URL + link['href'])

anime_ep_links = anime_ep_links[::-1]  # Episodes are displayed in reverse order
anime.episodes_link = anime_ep_links
# Step 3 _Begin  downloading the anime episodes
# By default will save episodes in ./{anime-name}/
print("\nSaving the episodes in the directory {0}   ".format(anime.name))
if not os.path.exists(anime.name):
    os.mkdir(anime.name)
# Now supporting range of episodes or single episode download

while True:
    episode_pref = input(
        "Enter the range/episode you want to download.\n\n[ Enter '0' for downloading complete anime or two"
        "numbers between 1 and {} separated by '-' or just enter the episode number]\n".format(anime.episodes_avail))

    if episode_pref == '0':
        anime.dwnld_range(1, anime.episodes_avail, driver)
        break
    elif '-' in episode_pref:
        lowest, highest = map(int, episode_pref.split('-'))
        if lowest < highest and 0 < lowest < anime.episodes_avail and 0 < highest <= anime.episodes_avail:
            anime.dwnld_range(lowest, highest, driver)
            break
        else:
            print("You entered Invalid episode range.")
    else:
        anime.dwnld_single(int(episode_pref), driver)
        break
driver.close()
# Assuming Keyboard Iterruption or succesful excetution
"""
print("Saving data...")
anime_data['searched'].append(anime)
if anime.follow:
    anime_data['followed'].append(anime)
pic = open(os.path.join("Files", "anime_data"), 'wb')
pickle.dump(anime_data, pic)
pic.close()
print("Completed")
"""