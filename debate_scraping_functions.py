'''
Functions for utilizing BeautifulSoup to scrape Presidential Debate transcripts from the web.
'''
#Importing needed packages:
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 20,10
import numpy as np
import glob
from scipy import stats
from bs4 import BeautifulSoup
import requests
import re
from IPython.core.display import display, HTML 
import time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver

#Below functions are for pulling from Commission on Presidential Debates Site:
def cpd_individual_soup_maker(link):
    '''
    Arguments: takes in a link, and creates a BeautifulSoup object for that page.
    Returns: a BeatifulSoup Object.
    '''
    if link[0:3] == '/vo':
        link = 'https://www.debates.org' + link
    response = requests.get(link)
    page = response.text
    soup_object = BeautifulSoup(page, 'lxml')
    return soup_object   

def cpd_soup_maker(link):
    '''
    Arguments: takes in the URL for the Commission on Presidential Debates site, for Debate transcripts.
    Returns: a BeautifulSoup object of the given links.
    '''
    #Creating a BeautifulSoup Object from the CPD homepage:
    response = requests.get(link)
    page = response.text
    soup_object = BeautifulSoup(page, 'lxml')

    #Pulling individual links from the homepage:
    links = soup_object.find('div', id='content-sm').find_all('a')
    url_list = [link.get('href') for link in links]

    #Running each individual link through the individual_soup_maker function:
    soup_list = [cpd_individual_soup_maker(url) for url in url_list]
    return soup_list

def cpd_transcript_puller(link):
    '''
    Arguments: takes in a link to the Commission for Presidential Debate homepage.
    Returns: a list of transcripts from Presidential Debates, 1960-present.  
    Utilized: cpd_soup_maker and individual_soup_maker functions.
    '''
    #Running the cpd_soup_maker function to get the list of BeautifulSoupObjects:
    soup_list = cpd_soup_maker(link)

    #Pulling each soup object's transcript:
    transcript_list = []
    for soup in soup_list:
        transcript = soup.find('div', id='content-sm').find_all('p')
        ind_list = [item.get_text().replace(u'\xa0', ' ') for item in transcript]
        transcript_list.append(ind_list)
    return transcript_list

#Below functions are for scraping from American Presidency Project site:

def app_individual_soup_maker(link):
    '''
    Arguments: takes in a link, and creates a BeautifulSoup object for that page.
    Returns: a BeatifulSoup Object.
    '''
    response = requests.get(link)
    page = response.text
    soup_object = BeautifulSoup(page, 'lxml')
    return soup_object   

def app_soup_maker(link):
    '''
    Arguments: takes in the URL for the American Presidency Project debates site, for Debate transcripts.
    Returns: a BeautifulSoup object of the given links.
    '''
    #Creating a BeautifulSoup Object from the CPD homepage:
    response = requests.get(link)
    page = response.text
    soup_object = BeautifulSoup(page, 'lxml')

    #Pulling individual links from the homepage:
    links = soup_object.find('tbody').find_all('a')
    url_list = [link.get('href') for link in links]

    #Running each individual link through the individual_soup_maker function:
    soup_list = [app_individual_soup_maker(url) for url in url_list]
    return soup_list

def app_transcript_puller(link):
    '''
    Arguments: takes in a link to the American Presidency Project debates homepage.
    Returns: a list of transcripts from Presidential Debates, 1960-present.  
    Utilized: app_soup_maker and app_individual_soup_maker functions.
    '''
    #Running the cpd_soup_maker function to get the list of BeautifulSoupObjects:
    soup_list = app_soup_maker(link)

    #Pulling each soup object's transcript:
    transcript_list = []
    for soup in soup_list:
        transcript = soup.find('div', class_='field-docs-content').find_all('p')
        ind_list = [item.get_text().replace(u'\xa0', ' ') for item in transcript]
        transcript_list.append(ind_list)
    return transcript_list

