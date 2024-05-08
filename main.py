
# from translate import Translation
# from sentiment import classifier
# from conversion import Conversion
import tweepy
import re
from twitter import Twitteruse
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

import requests
from app import app
import uvicorn

from dataplotting import plotpie, plotlc

import re
import logging
logging.basicConfig(level=logging.INFO,filename="twitter_project.log",filemode='w',format="%(asctime)s - %(levelname)s - %(message)s")

import streamlit as st
from streamlit_kpi import streamlit_kpi
import time
import plotly.express as px

import datetime

if 'twitter_insta' not in st.session_state:
    st.session_state.twitter_insta = False
    


if 'search_button' not in st.session_state:
    st.session_state.search_button = False

if 'Analyze_tweets' not in st.session_state:
    st.session_state.Analyze_tweets = False

if 'tweet_count_slider' not in st.session_state:
        st.session_state.tweet_count_slider = 10



st.header("Twitter Sentiment Analysis")
st.subheader("Please Enter your search string or #")
search_string = st.text_input(" ")
search_button = st.button("Search")


    


if search_button or st.session_state.search_button:
    
    
    # st.session_state.twitter_insta = twitter_insta

    st.session_state.search_button=True
    onesearch=True
    print(f"search_string = {search_string} ")
    logging.info(f"\n\n Twitter API Got Initialized")
    twitter_insta = Twitteruse()

    if search_button:
        search_button = False
        response = twitter_insta.get_tweets_count(search_string)
    
    tweet_count = pd.read_csv("tweetcount.csv",parse_dates=['date_only'])
    logging.info(tweet_count)

   

    c1,c2,c3 = st.columns((6,1,3))
    
    c1.subheader("Tweet count by week")
    c1.line_chart(tweet_count,x='date_only',y='tweets_count')
    
    c2.empty()
    
    c3.subheader("Pick the Date and #tweets for analysis")
    min_date = c3.date_input("Start Date",min_value=min(tweet_count['date_only'])+datetime.timedelta(days=1),max_value=max(tweet_count['date_only']),value=min(tweet_count['date_only'])+datetime.timedelta(days=1),)
    max_date = c3.date_input("End Date",min_value=min_date,max_value=max(tweet_count['date_only']),value=max(tweet_count['date_only']))
    tweet_count_selection = tweet_count.query("date_only>=@min_date and date_only<=@max_date")
    tweet_count_value = sum(tweet_count_selection['tweets_count'])
    tweet_count_slider=c3.slider(label ="#tweets",min_value=10,max_value=tweet_count_value)

    
    st.session_state.tweet_count_slider = tweet_count_slider
    
    print(min_date)
    print(max_date)
    print(st.session_state.tweet_count_slider)



Analyze_tweets = st.button("   Get Tweets and Analyze  ")

# Analyze_tweets = True

if Analyze_tweets or st.session_state.Analyze_tweets:
    
    # Analyze_tweets = False
    twitter_insta = Twitteruse()
   

    # print(f"tweet_count_slider{st.session_state.tweet_count_slider}")
    if Analyze_tweets:
        st.session_state.Analyze_tweets = True
        # progress_text = "Operation in progress. Please wait."
        # my_bar = st.progress(0, text=progress_text)

        # for percent_complete in range(100):
        #     time.sleep(0.1)
        #     my_bar.progress(percent_complete + 1, text=progress_text)

        tweet_data = twitter_insta.get_tweets(search_string,str(min_date)+"T00:00:00.000Z",str(max_date)+"T00:00:00.000Z",st.session_state.tweet_count_slider)
        # my_bar.progress(percent_complete + 1, text="Sentiment Analysis Results are ready")
    
   
                                    
    # tweet_data = pd.read_excel("tweetdata_checking.xls")
        like_count = sum(tweet_data['like_count'])
        retweet_count = sum(tweet_data['retweet_count'])
        # impression_count = sum(tweet_data['impression_count'])

                                        
        s1,s2 = st.columns(2)
        with s1:
            streamlit_kpi(key="zero",height=100,title="Likes ",value=like_count,icon="fa-solid fa-thumbs-up")
        with s2:
            streamlit_kpi(key="one",height=100,title="Retweets ",value=retweet_count,icon="fa-solid fa-retweet")
        # with s3:
        #     streamlit_kpi(key="two",height=100,title="Impressions ",value=impression_count,icon="fa-solid fa-eye")

                                            

        fig = px.pie(names=tweet_data['sentiment'].unique(),values=tweet_data['sentiment'].value_counts())
        col1,col2,col3 = st.columns((4,1,3))
        with col1:
            col1.subheader("Sentiment Analysis")
            col1.plotly_chart(fig,use_container_width=True)

        with col2:
            col2.empty()
        with col3:
            if retweet_count>0:
                tweet_data = twitter_insta.get_influencers_retweets()
                col3.dataframe(tweet_data)
            col3.empty()

            if like_count>0:
                col3.empty()
                tweet_data = twitter_insta.get_influencers_likes()
                col3.dataframe(tweet_data)  
       



    # try:
    #     tweets_df.to_csv('tweetdata_updated.csv', index=True) 
    
    # except "tweetdata_updated.csv file and tweetusers_updated.csv is already open" as e:
    #     logging.error("\n\n Please close the tweetdata_updated.csv and tweetusers_updated.csv file as it cannot write it and it will process only the old data")
    #     pass






