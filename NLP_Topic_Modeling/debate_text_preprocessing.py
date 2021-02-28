'''
The purpose of this code is to preprocess debate transcript text, to prepare for Vectorization and Topic Modelling.
'''
#Importing Needed Packages to run this code:
from __future__ import print_function
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import re
import string
from nltk.corpus import stopwords
import numpy as np

def word_lemmatizer(df_column):
    '''
    Arguments: takes in a column of text data from a Pandas Dataframe, that already has stopwords removed and is word tokenized.
    Returns: a lemmatized list of words
    '''
    #Initializing the Lemmatizer:
    lemma = nltk.stem.WordNetLemmatizer()

    #Looping through the input column to lemmatize:
    lemmed_list = []
    for i, text in enumerate(df_column):
        lemmed_words = [lemma.lemmatize(word) for word in text]
        lemmed_list.append(lemmed_words)
    return lemmed_list 

def master_preprocessor(text_df, stop_words):
    '''
    Arguments: takes in a pandas dataframe containing text data and a list of stop words to use.
    Returns: new columns on the original dataframe with the following text preprocessing done:
        - text made lowercase
        - text w/ punctuation removed
        - word tokenized
        - stop words removed
        - lemmatized
        -re-joined as a string
    Output includes texts to alert user of which steps have been done.
    NOTE: text to pre-process must be in a column named 'Transcript'!
    '''
    #Removing punctuation and making text lowercase:
    alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)
    punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower())
    text_df['no_punc'] = text_df.Transcript.map(alphanumeric).map(punc_lower) 
    print('Text made lowercase and punctuation removed!')

    #Word-tokenizing the lowercase/punctuation removed text:
    text_df['token'] = text_df['no_punc'].apply(word_tokenize)
    print('Text has been word tokenized!')

    #Removing the user-inputted stop-words:
    text_df['no_stop_words'] = text_df['token'].apply(lambda x: [word for word in x if word not in stop_words])
    print('Stop words have been removed!')

    #Lemmatization of the tokenized text:
    lemmed_list = word_lemmatizer(text_df['no_stop_words'])
    text_df['lemmed'] = lemmed_list
    print('Text has been lemmatized!')

    #Resetting index of new dataframe:
    new_df = text_df['lemmed'].reset_index()

    #Re-strining the lemmatized text:
    new_df['string'] = 0
    for i, text in enumerate(new_df['lemmed']):
        new_df.iloc[i, 2] = ' '.join(text)
    print('Text has been put back together as a string!')

    #Adding Line lengths:
    new_df['line_length'] = 0
    for i, text in enumerate(new_df.line_length):
        new_df['line_length'].iloc[i] = len(new_df.lemmed.iloc[i])

    return new_df




