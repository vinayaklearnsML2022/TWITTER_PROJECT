
from translate import Translation
from sentiment import classifier
# from sentiment import sentiment_value
import tweepy

import re

from twitter import search_twitter as tweet
import os
from dotenv import load_dotenv
import pandas as pd

import requests
from app import app

import uvicorn

from dataplotting import plotpie, plotlc


def run():
    
    
    api_url = "http://127.0.0.1:8000/search_query/1"
    request =requests.get(api_url)
    
    if request.status_code == 200:
        string_value = request.json()
        print("processed_string:", string_value.get('name'))
    else:
        return {"error": "Failed to retrieve string from website"}
    

    client = tweet.initialise()
    response = client.get_recent_tweets_count(query = string_value.get('name'),granularity='day')

    print(len(response))

    dates_lc = []
    tweets_count_lc = []    

    for i in range(len(response.data)):
        dates_lc.append(response.data[i]['start'][:10])
        tweets_count_lc.append(response.data[i]['tweet_count'])


    tweets_cnt_container= [[tweetcnt['start'][:10],tweetcnt['tweet_count']] for tweetcnt in response.data]  
    columns=['date', 'tweets count']
  
    tweetstweets_count_df = pd.DataFrame(tweets_cnt_container,columns=columns)
    tweetstweets_count_df.to_csv('tweetcount.csv', index=True)  



    response = client.search_recent_tweets(query = string_value.get('name') ,max_results=10, tweet_fields=['public_metrics','created_at'],expansions=['author_id'])
    print("response = ",response)
       
    tweets_container= [[tweetread.id,tweetread.text,tweetread.created_at,tweetread.public_metrics['like_count'],tweetread.public_metrics['retweet_count'],tweetread.public_metrics['impression_count']] for tweetread in response.data]  
    columns=['tweet_ids', 'tweets text','created_at','like_count','retweet_count','impression_count']
    print("\n\n")
    print(f"tweets{tweets_container}")

    tweets_df = pd.DataFrame(tweets_container,columns=columns)
    print(f"res cnt {response.meta['result_count']}")
    
    val = str(response.includes)
    print(val)

    userid = re.findall("User id=(.*?) name=",val)
    name = re.findall("name=(.*?) userna",val)
    username = re.findall("username=(.*?)>",val)
    tweets_df['userid'] = userid
    tweets_df['name'] = name
    tweets_df['username'] = username



    
   

    followers =[]
    image =[]
  
    for i in range(response.meta['result_count']):
        response = client.get_user(id=userid[i],user_fields=['public_metrics','profile_image_url'])
        user_metrics = response.data['public_metrics']
        followers.append(user_metrics['followers_count'])
        image_details = response.data['profile_image_url']
        image.append(image_details)
       

    print(f"followers = {followers}")
   
    tweets_df['followers']=followers
    tweets_df['image']=image

    tweets_df['toenglish']=[Translation(twee) for twee in tweets_df['tweets text']]
    
    tweets_df['sentiment']=[classi['label'] for classi in classifier(list(tweets_df['toenglish']))]
    tweets_df['percent']=[round(classi['score'],4)*100 for classi in classifier(list(tweets_df['toenglish']))]
    
    
    tweets_df.to_csv('tweetdata_updated.csv', index=True) 
    
   
if __name__ == "__main__":
    run()


