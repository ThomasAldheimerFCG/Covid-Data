#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get covid daily data from ecdc url
"""

import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd


def get_cases():
    """ Download latest covid cases and saves as pickel, with today datestamp """
    url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'

    # Hide chromedriver window
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", {"download.default_directory": "data",
                                                     "download.prompt_for_download": False,
                                                     "download.directory_upgrade": True,
                                                     "safebrowsing.enabled": True})

    # Download data
    driver = webdriver.Chrome('/Applications/chromedriver', chrome_options=chrome_options)
    driver.get(url)
    time.sleep(10)
    driver.close()

    # Resave as pickle
    today = str(date.today()).replace('-', '')
    df = pd.read_csv('data/download')
    df.to_pickle('data/covid_cases_'+today)
    return None

get_cases()
#url = 'https://ourworldindata.org/grapher/covid-19-tests-country'
