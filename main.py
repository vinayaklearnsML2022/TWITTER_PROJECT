
from translate import Translation
from sentiment import classifier
import tweepy
import re
from twitter import search_twitter as tweet
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

import requests
from app import app
import uvicorn

from dataplotting import plotpie, plotlc

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import ExpectedConditions
from time import sleep



import logging
logging.basicConfig(level=logging.INFO,filename="twitter_project.log",filemode='w',format="%(asctime)s - %(levelname)s - %(message)s")


def run():
    
    api_url = "http://127.0.0.1:8000/search_query/1"
    request =requests.get(api_url)
    
    try:
        request.status_code == 200
        string_value = request.json()
        logging.info(f"\n\n Search String = {string_value.get('name')}")
    except:
        logging.error("\n\n Unable to Get data from web server")

    
    try:
        client = tweet.initialise()
        logging.info(f"\n\n Twitter API Got Initialized")
        
    except "Tweet_initialize_error" as e:
        logging.error("\n\n Unable to Initialize Tweet")
    
    browser = webdriver.Chrome()
      
    # try:
    #     response = client.get_recent_tweets_count(query = string_value.get('name'), granularity='day')
    #     val = 1/len(response)
    #     logging.info(f"Recent tweets count for a week is received")

    #     tweets_cnt_container= [[tweetcnt['start'][:10],tweetcnt['tweet_count']] for tweetcnt in response.data]  
    #     columns=['date', 'tweets count']
    #     tweetstweets_count_df = pd.DataFrame(tweets_cnt_container,columns=columns)
    #     logging.info(f"tweets_count_df {tweetstweets_count_df}")

    #     tweetstweets_count_df.to_csv('tweetcount.csv', index=True)
    #     logging.info(f"\n\n tweets count written in tweetcount.csv")
        
        
            
    # except ZeroDivisionError as e:
    #     logging.info("\n\n No Recent tweets")
    #     pass

    # except "tweetcount.csv file is already open" as e:
    #     logging.error("\n\n Please close the tweetcount.csv file as it cannot write it and it will process only the old data")
    #     pass
    

    try:
        response = client.search_recent_tweets(query = string_value.get('name') ,max_results=10, tweet_fields=['public_metrics','created_at'],expansions=['author_id'])
        # response = client.search_recent_tweets(query = string_value.get('name') ,max_results=10, tweet_fields=['public_metrics','created_at','author_id'])
        value = 1/len(response)
        tweets_container= [[tweetread.id,tweetread.text,tweetread.created_at,tweetread.public_metrics['like_count'],tweetread.public_metrics['retweet_count'],tweetread.public_metrics['impression_count']] for tweetread in response.data]  
        columns=['tweet_ids', 'tweets text','created_at','like_count','retweet_count','impression_count']
        
        logging.info(f"\n\n tweets{tweets_container}")
        tweets_df = pd.DataFrame(tweets_container,columns=columns)
        logging.info(f"\n\n result count {response.meta['result_count']}")

        print(f"\n\nDebug the Response {response}")

        username=[]
        tweets_df['tweet_url']="https://twitter.com/twitter/status/"+tweets_df['tweet_ids'].astype(str)
    
    except ZeroDivisionError as e:
        logging.info("\n\nNo search Recent tweets")
        pass

    except "same user tweets so the user ID will be less" as e:
        logging.info("\n\nDebug the Response {tweet_response.data}")
        # logging.info("\n\nDebug the Response {response.includes}")
        pass

    # try :
        
    #     for tweets in tweets_df['tweet_url']:
            
    #         browser.get(tweets)
            # class1 = WebDriverWait(browser,5).until(
            # EC.presence_of_element_located((By.XPATH,"//span[@class='css-1qaijid r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-b88u0q']"))
            # )
            # WebDriverWait(browser,5).until(
            # EC.visibility_of_all_elements_located()
            # )

            # sleep(2)   
    #         username.append(re.findall(".com\/(\S.*)\/status",browser.current_url))
    # except "tweet scraping problem" as e:
    #     logging.info(f"The Problem is during loading this tweet {tweets}")
            
    usernames = [item for sublist in username for item in sublist]
    tweets_df['username'] = usernames
    # tweets_df['tweets_unichar'] = ord(tweets_df['tweets text'])
    followers =[]
    image =[]
    location=[]
  
    for i in range(response.meta['result_count']):
        response = client.get_user(username=usernames[i],user_fields=['public_metrics','profile_image_url','location'])
        user_metrics = response.data['public_metrics']
        followers.append(user_metrics['followers_count'])
        image_details = response.data['profile_image_url']
        image.append(image_details)
        loc_details = response.data['location']
        location.append(loc_details)
    


    
       

    tweets_df['followers']=followers
    tweets_df['image']=image
    tweets_df['location']=location
    tweets_df['toenglish']=[Translation(twee) for twee in tweets_df['tweets text']]
    tweets_df['sentiment']=[classi['label'] for classi in classifier(list(tweets_df['toenglish']))]
    tweets_df['percent']=[round(classi['score'],4)*100 for classi in classifier(list(tweets_df['toenglish']))]

    logging.info(f"\n\n tweets df {tweets_df}")


    try:
        tweets_df.to_csv('tweetdata_updated.csv', index=True) 
    
    except "tweetdata_updated.csv file is already open" as e:
        logging.error("\n\n Please close the tweetdata_updated.csv file as it cannot write it and it will process only the old data")
        pass

    browser.quit()
    # class1.quit()
    # class2.quit()

   
if __name__ == "__main__":
    run()


