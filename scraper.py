#!/usr/bin/env python

# This file is a part of project (TENTATIVE)anYme-dl check `ideas` file
# File Creation : 01-01-2018-11-06
# Original FileName : `scraper@py`
# File Aim : To create search scraper
# OFF //~nyan~\\

# imports
import requests
import time
import os
import sys
from bs4 import BeautifulSoup
from requests import Response
from selenium import  webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# TODO Develop algorithm to make different type of timestamps

# Maynot need selenium for this:

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'

SEARCH_URL  = r'http://ww2.chia-anime.tv/search/'


def anime_search_query(query_name: str):
    """
    Extracts all the queries from the site and returns it
    :param query_name: The anime string to be searched
    :return:
    """
    if query_name is None:
        raise INVALID_ANIME_NAME
    else:
        search_url_final = SEARCH_URL+query_name.replace(" ", "%")
        search_page = requests.get(search_url_final)
        search_soup = BeautifulSoup(search_page.text, "lxml")

        anime_search_data = {}      # Format : { 1:['name','link','img_link']}
        counter = 0
        print("Search Results:")

        y: object
        for x, y in zip(search_soup.find_all(class_="title"), search_soup.find_all(class_="picture")):
            print('[{0}] {1}'.format(counter+1,x.a.text))
            anime_search_data[counter] = [x.a.text,x.a['href'], y.img['src']]
            counter = counter+1

        while True:
            
            choice = int(input('Enter a choice:'))
            
            if 0 < choice < counter:
                break

        return anime_search_data[choice-1]


def all_episode_of(anime_url: str) -> object:
    """
    Return the link of the page of all anime episode of given anime_url
    :param anime_url:
    :return:
    """
    anime_page: Response = requests.get(anime_url)
    anime_page_soup = BeautifulSoup(anime_page.text, "lxml")
    anime_ep_links = []

    for x in anime_page_soup.find_all('h3'):
        anime_ep_links.append(x.a['href'])

    # NOTE : I;m returning only first ep and as chiaanime shows revered list, also the episode length
    # Length is no longer needed (@02-45-09-11-2018) removed
    return anime_ep_links


def all_anime_premium_link(ep_link: list) -> list:
    """
    This returns the first link of anime premium server
    :param first_ep_link:
    :return:
    """

    # Strategy here is use this to find first link and then use another function to find all others(saves time)
    # above strategy didnt work now going with OG strategy
    all_eps_link  = []
    for first_ep_link in ep_link:
        header = {"User-Agent": USER_AGENT, "Referer": "http://chia-anime.tv"}
        episode_soup = BeautifulSoup(requests.get(first_ep_link, headers=header).text, "lxml")
        all_eps_link.append(episode_soup.find_all(id="download")[0]['href'])

    # (DOESNT APPLY @02-42-2018-11-09)Im thinking of merging two functions and returning the complete anime premium
    # list here only
    return all_eps_link


def main():
    """
    Well this is the  main functions
    :return:
    """
    user_anime_query = input('Enter the name of anime to be searched')
    user_anime_data = anime_search_query(user_anime_query)

    # ^ Got the anime name, anime cover image and original details
    # Now extract episode details
    # TODO Add MAL integration for details printing etc

    all_episode_anime: list
    all_episode_anime = all_episode_of(user_anime_data[1])

    # ^ After getting first ep i will get the anime premium link for it
    # Ive merged two functions and now i get all the links here only

    anime_all_episodes: list = all_anime_premium_link(all_episode_anime)
    print("Total episodes : {0}".format(len(anime_all_episodes)))
    print(anime_all_episodes)


if __name__ == '__main__':
    main()
