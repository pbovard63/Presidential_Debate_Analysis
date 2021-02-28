# Presidential Debate Analysis :horse: :us: :elephant:
## Analyzing Presidential Debates Using Natural Language Processing
## *Metis Project 4*
## By: Patrick Bovard

### PROJECT IN PROGRESS

**Project Description:** 
The goal of this project is to use Natural Language Processing (NLP) techniques to better understand how presidential debates in the United States have evolved over time.  Going into the project, major questions to be explored were:  
1. How have debates changed over time?
2. Do parties or moderators tend to focus on certain topics?  Have these changed?
3. Do election winners and losers have patterns in their sentiment or topics?

**Data Sources:** Data has been scraped using BeautifulSoup from the following sites for this project:  
- [Commission for Presidential Debates:](https://www.debates.org/voter-education/debate-transcripts/) used for official transcripts on the General Election Debates, 1960-present  
-  [The American President Project from UC Santa Barbara:](https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/presidential-campaigns-debates-and-endorsements-0) used for transcripts of primary debates for Republican and Democrat candidates, 2000-present  

**Tools Used:**  
- Webscraping: BeautifulSoup
- Data Analysis and Model Building: Python, Pandas, Scikit-Learn
- Natural Language Processing: TF-IDF Vectorization, Topic Modeling via NMF, Count Vectorization, Lemmatization, NLTK, VADER Sentiment Analysis

**Navigating the Repo:**
- **Data folder**: houses data generated throughout this progress in .pickle format
- **Final_Presentation Folder:** Slides prepared for my presentation of this project are in the Final_Presentation folder.  This includes slides in both PDF and Powerpoint format.
- **Webscraping-Data_Collection Folder:** This folder houses the following files used for webscraping and initial gathering of the data:  
  -   debate_scraping.ipynb: Initial webscraping of transcript data from the Commission for Presidential Debates and American Presidency Projects sites.  
  -   model_tagging.ipynb: Scraping of speaker information from the APP and CPD sites to utilize in properly tagging the speaking lines.  
  -   debate_scraping_functions.py: related python functions for webscraping these sites. 
-  **Text_Cleaning Folder:** This folder contains files related to cleaning and pre-processing the debate text, prior to topic modeling and sentiment analysis.  
  -  text_cleaning.ipynb: cleaning and beginning to pre-process text data from the original transcript data, such as adding in Speaker Name, Speaker Type, etc. in a dataframe.  This prepares the data for NLP work.  
  -  secondary_text_clean_speakers.ipynb: correctly tagging each row with a speaker, includes handling matching up speakers to rows.
- **Sentiment Analysis Folder:** This folder houses code to conduct sentiment analysis using VADER sentiment analysis. 
  - sentiment_analysis_work.ipynb: VADER sentiment analysis on the transcript corpus.  
- **NLP_Topic_Modeling Folder:** This folder contains code for some NLP pre-processing and running topic modeling on the debate text data.  Different methods were attempted in the following files:  
  - final_dataframe_cleanup.ipynb: 
  - debate_text_preprocessing.py: contains functions for text pre-processing (i.e. lemmatization, lower-case, removing numbers and punctuation, etc.) that is used in final_dataframe_cleanup.ipynb.
  - tf-idf_vectorizer_topic_modeling.ipynb: 
  - topic_modeling_lda_lsa.ipynb: file running topic modeling via TF-IDF Vectorization and Latent dirichlet allocation (LDA) / Latent semantic analysis (LSA).  These were ultimately not utilized in the final topic model, after comparison.  
  - corex_model_testing.ipynb: file containing code on utilizing Corex for topic modeling of the debate data.  
