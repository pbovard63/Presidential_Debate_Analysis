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
    Returns: a BeatifulSoup Object for the given link.
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
    Returns: a BeautifulSoup object of the given links located on the CPD homepage.
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
    Utilized: cpd_soup_maker and cpd_individual_soup_maker functions.
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

def cpd_url_puller(links):
    '''
    Arguments: takes in the URL for Commission for Presidential Debates debate transcript.
    Returns: a BeautifulSoup object of the given links.
    '''
    #Creating a BeautifulSoup Object from the CPD homepage:
    response = requests.get(links)
    page = response.text
    soup_object = BeautifulSoup(page, 'lxml')

    #Pulling individual links from the homepage:
    new_links = soup_object.find('div', id='content-sm').find_all('a')
    url_list = [link.get('href') for link in new_links]
    new_url_list = []
    for url in url_list:
        if url[0:3] == '/vo':
            url = 'https://www.debates.org' + url
        new_url_list.append(url)
    return new_url_list

def cpd_group_speaker_puller(link_list):
    '''
    Arguments: takes in a list of url links to the Commission for Presidential Debates Transcripts.
    Returns: a list of speakers from transcripts from Presidential Debates, 1960-present.  
    Utilized: cpd_soup_maker and cpd_individual_soup_maker functions.
    '''
    
    #Pulling the speaker from each transcript:
    speaker_list = []
    for link in link_list:
        page_speaker_list = []

        #Creating a beautiful soup object:
        soup = app_individual_soup_maker(link)

        #All information on these is in "Group 3" format:
        paragraphs = soup.find('div', id='content-sm').find_all('p')
        for paragraph in paragraphs:
            if paragraph.get_text().split(':')[0].isupper() or paragraph.get_text().split(':')[0] == 'MR. McGEE':
                speaker = paragraph.get_text().split(':')[0]
            else:
                speaker = 'no speaker!'
            page_speaker_list.append(speaker)
        speaker_list.append(page_speaker_list)
    return speaker_list


##########################

#Below functions are for scraping from American Presidency Project site:

###########################

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
    Returns: a BeautifulSoup object of the given links on the APP main page.
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

def app_group_speaker_puller(link_list):
    '''
    Arguments: takes in a list of tuples with group number and link.
    Returns: a list of speakers from transcripts from Presidential Debates, 1960-present.  
    Utilized: app_soup_maker and app_individual_soup_maker functions.
    '''
    
    #Pulling the speaker from each transcript:
    speaker_list = []
    for group_link_pair in link_list:
        page_speaker_list = []

        #Pair is a tuple, first object is group number, second is link:
        group_number = group_link_pair[0]
        link = group_link_pair[1]

        #Creating a beautiful soup object:
        soup = app_individual_soup_maker(link)
        #Checking if the transcript is in group 1 (bold speaker names):
        if group_number == 1:
            paragraphs = soup.find('div', class_='field-docs-content').find_all('p')
            for paragraph in paragraphs:
                if paragraph.find('b'): #Seeing if there is any bold text in the paragraph:
                    speaker = paragraph.find('b').get_text().strip(':')
                elif paragraph.find('strong'):
                    speaker = paragraph.find('strong').get_text().strip(':')
                else:
                    speaker = 'no speaker!'
                page_speaker_list.append(speaker)
        #Seeing if transcript is in group_two (i.e. italics speaker name)
        elif group_number == 2:
            paragraphs = soup.find('div', class_='field-docs-content').find_all('p')
            for paragraph in paragraphs:
                if paragraph.find('i'): #Seeing if there is any italics text in the paragraph:
                    speaker = paragraph.find('i').get_text().strip('.')
                elif paragraph.find('em'):
                    speaker = paragraph.find('em').get_text().strip('.')
                else:
                    speaker = 'no speaker!'
                page_speaker_list.append(speaker)
        #Seeing if transcript in group 3: (i.e. upper case speaker with :)
        elif group_number == 3:
            paragraphs = soup.find('div', class_='field-docs-content').find_all('p')
            for paragraph in paragraphs:
                if paragraph.get_text().split(':')[0].isupper() or paragraph.get_text().split(':')[0] == 'MR. McGEE':
                    speaker = paragraph.get_text().split(':')[0]
                else:
                    speaker = 'no speaker!'
                page_speaker_list.append(speaker)
        speaker_list.append(page_speaker_list)
    return speaker_list

def app_url_puller(link):
    '''
    Arguments: takes in the URL for an American Presidency Project debate transcript.
    Returns: a BeautifulSoup object of the given links on the APP homepage.
    '''
    #Creating a BeautifulSoup Object from the CPD homepage:
    response = requests.get(link)
    page = response.text
    soup_object = BeautifulSoup(page, 'lxml')

    #Pulling individual links from the homepage:
    links = soup_object.find('tbody').find_all('a')
    url_list = [link.get('href') for link in links]
    return url_list