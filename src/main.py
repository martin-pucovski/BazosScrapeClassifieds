#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script scrapes data from site www.bazos.sk
"""

__author__ = "Martin Pucovski"
__copyright__ = "Copyright 2023, Martin Pucovski"
__credits__ = ["Martin Pucovski"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Martin Pucovski"
__email__ = "pucovsky.martin@gmail.com"
__status__ = "Production"


import configparser
import datetime
import logging
from pathlib import Path
import sys
import os
from urllib.parse import urlparse
import csv
import requests
from bs4 import BeautifulSoup


# -------------------------------------------------- #
# SET INITIAL CONSTANTS

# Get config file name from argument
# TEST CONFIG_NAME = sys.argv[1]
CONFIG_NAME = 'config_TEST.ini'

PROJECT_DIRECTORY = Path(os.getcwd())
LOGS_FOLDER = "logs"
DATA_PATH = Path(PROJECT_DIRECTORY) / "data"

# -------------------------------------------------- #
# READ CONFIG FILE

# Read main config file
config = configparser.ConfigParser(interpolation=None)
config_path = Path(PROJECT_DIRECTORY) / "config" / CONFIG_NAME
config.read(config_path)
config_default = config["DEFAULT"]

# -------------------------------------------------- #
# SET LOGGING

current_date = datetime.datetime.now().strftime("%Y%m%d")
log_file_name = f"log_{current_date}.log"
log_file = Path(PROJECT_DIRECTORY) / LOGS_FOLDER / log_file_name
file_handler = logging.FileHandler(
    filename=log_file, mode="a", encoding=None, delay=False)
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(handlers=handlers,
                    encoding='utf-8',
                    level=os.environ.get(
                        "LOGLEVEL", config_default['Loggin_Level']),
                    format='%(asctime)s:%(levelname)s:%(message)s')

# -------------------------------------------------- #

logging.info("# ------------------------------ #")

# Create data folders if they do not exist
DATA_PATH.mkdir(parents=True, exist_ok=True)


class Classified():
    """
    Main class for one classified ad
    """
    def __init__(self, title, link):
        self._title = title
        self._link = link
        self._description = ""
        self._price = ""
        self._location = ""

    @property
    def title(self):
        return self._title

    @property
    def link(self):
        return self._link

    @property
    def description(self):
        return self._description

    @property
    def price(self):
        return self._price

    @property
    def location(self):
        return self._location

    @title.setter
    def title(self, title):
        self._title = title

    @link.setter
    def link(self, link):
        self._link = link

    @description.setter
    def description(self, description):
        self._description = description

    @price.setter
    def price(self, price):
        self._price = price

    @location.setter
    def location(self, location):
        self._location = location


def index_classifieds() -> list:
    """
    Index all classifieds that are found with filter

    :return: List of classfied ads objects
    """

    logging.info("Start getting all pages")

    all_classifieds = []
    bazos_link = config_default['Bazos_link']

    # Build the base link for bazos
    parsed_link = urlparse(bazos_link)
    bazos_base = parsed_link.scheme + '://' + parsed_link.netloc

    # Get data from all pages
    while True:
        request = requests.get(bazos_link, timeout=30)
        soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), "lxml")

        # Scrape one page
        all_classifieds = index_one_page(soup, all_classifieds, bazos_base)

        # Check if there is next page
        pages_selector = soup.find('div', {'class': 'strankovani'})

        # If there is no pages selector, finish
        if pages_selector is None:
            break
        else:
            pages_a = pages_selector.find_all('a')
            text = pages_a[-1]

            # If there is a next page, get the link
            if text.text == "Ďalšia":
                bazos_link = bazos_base + text['href']
            # If no next page, finish
            else:
                break

    logging.info("Finish getting all pages")
    return all_classifieds


def index_one_page(soup: BeautifulSoup, all_classifieds: list, bazos_base: str) -> list:
    """
    Parse one page of classifieds

    :param soup: Page to parse in BeautifulSoup format
    :param all_classifieds: list of classified objects
    :retrun: updated list of classifieds objects
    """

    for div in soup.find_all('h2', {'class': 'nadpis'}):
        ad_link = bazos_base + div.find('a')['href']
        ad_title =  div.text
        ad_title = clean_text(ad_title)
        one_classified = Classified(title=ad_title, link=ad_link)
        all_classifieds.append(one_classified)

    return all_classifieds

def scrape_one(one_classified):
    """
    Scrape one classified ad. Get description and price.

    :param one_classified: object for one classified ad
    """

    # Get page
    request = requests.get(one_classified.link, timeout=30)

    # Parse Description
    soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), "lxml")
    text = soup.find('div', class_="popisdetail")
    one_classified.description = clean_text(text.text)

    # Parse Location
    soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), "lxml")
    for one_td in soup.find_all('td'):
        if one_td.text == "Lokalita:":
            location_value = one_td.find_next_sibling("td").find_next_sibling("td").text
            location_value = location_value.strip()
            one_classified.location = location_value
            break

    # Parse Price
    soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), "lxml")
    for one_td in soup.find_all('td'):
        if one_td.text == "Cena:":
            price_value = one_td.find_next_sibling("td").text
            price_value = price_value.strip()
            one_classified.price = price_value
            break


def clean_text(text: str) -> str:
    """
    Clean the scraped text

    :param text: input text
    :return: cleaned text
    """

    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.strip()
    text = " ".join(text.split())

    return text


def main():
    """
    Main function of the script
    """
    logging.info("Script started")

    # Index classifieds
    classifieds = index_classifieds()

    # Open and get data
    for i in classifieds:
        scrape_one(i)

    # Build export file name and path
    current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"scraped_{current_datetime}.csv"
    file_path = DATA_PATH / file_name

    # Save classifieds to csv file
    with open(file_path, 'w+', newline='', encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter='|')
        for one_ad in classifieds:
            writer.writerow([
                one_ad.title,
                one_ad.link,
                one_ad.price,
                one_ad.location,
                one_ad.description])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(str(e))


logging.info("Script ended")
logging.info("# ------------------------------ #")
