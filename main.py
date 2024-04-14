
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
    # response = client.get_recent_tweets_count(query = string_value.get('name'),granularity='day')

    # print(len(response))

    # dates_lc = []
    # tweets_count_lc = []    

    # for i in range(len(response.data)):
        # dates_lc.append(response.data[i]['start'][:10])
        # tweets_count_lc.append(response.data[i]['tweet_count'])


    # tweets_cnt_container= [[tweetcnt['start'][:10],tweetcnt['tweet_count']] for tweetcnt in response.data]  
    # columns=['date', 'tweets count']
  
    # tweetstweets_count_df = pd.DataFrame(tweets_cnt_container,columns=columns)
    # tweetstweets_count_df.to_csv('tweetcount.csv', index=True)  


    # plotlc(tweets_count_lc,dates_lc,encoded_string)
    # plotlc(tweets_count_lc,dates_lc,string_value.get('name'))



    # response = client.get_tweet(id=1775153735594819790,tweet_fields=['public_metrics'])
                                 
    # print(f"response {response.data.public_metrics['like_count']}")
  
    # print(f"response {response.data.public_metrics['like_count']}")



    # data = "1775208854936080704"
    # # data = client.get_user(username = user,user_fields = ["public_metrics"])
    # # followers = data[0].public_metrics['followers_count']
    # # following = data[0].public_metrics['following_count'] 
    # likecount = data.public_metrics.like_count
    # print(likecount)

    # working code from here

    response = client.search_recent_tweets(query = string_value.get('name') ,max_results=10, tweet_fields=['public_metrics','created_at'],expansions=['author_id'])
    print("response = ",response)
       
    tweets_container= [[tweetread.id,tweetread.text,tweetread.created_at,tweetread.public_metrics['like_count'],tweetread.public_metrics['retweet_count'],tweetread.public_metrics['impression_count']] for tweetread in response.data]  
    columns=['tweet_ids', 'tweets text','created_at','like_count','retweet_count','impression_count']
    print("\n\n")
    print(f"tweets{tweets_container}")

    tweets_df = pd.DataFrame(tweets_container,columns=columns)
    # tweets_df.to_csv('tweetdata.csv', index=True)  

    print(f"res cnt {response.meta['result_count']}")
    
    val = str(response.includes)
    print(val)

    userid = re.findall("User id=(.*?) name=",val)
    name = re.findall("name=(.*?) userna",val)
    username = re.findall("username=(.*?)>",val)
    tweets_df['userid'] = userid
    tweets_df['name'] = name
    tweets_df['username'] = username



   
    
   
    # print(f"userid {userid}")
    followers =[]
  
    for i in range(response.meta['result_count']):
        response = client.get_user(id=userid[i],user_fields=['public_metrics'])
        user_metrics = response.data['public_metrics']
        followers.append(user_metrics['followers_count'])
       

    print(f"followers = {followers}")
   
    tweets_df['followers']=followers

    # tweets_df.to_csv('tweetdatausers.csv', index=True) 



    
    # tweets_user_container= [val]  
    # columns=['username']
    # print("\n\n")
    # print(f"tweet users{tweets_user_container}")

    # tweets_df = pd.DataFrame(tweets_user_container,columns=columns)
    # tweets_df.to_csv('tweetdata_users.csv', index=True)  

    # df = pd.read_csv("tweetdata.csv")
    tweets_df['toenglish']=[Translation(twee) for twee in tweets_df['tweets text']]
    
    tweets_df['sentiment']=[classi['label'] for classi in classifier(list(tweets_df['toenglish']))]
    tweets_df['percent']=[round(classi['score'],4)*100 for classi in classifier(list(tweets_df['toenglish']))]
    
    # df['likes_count']=[ client.get_tweet(id=tweet_id,tweet_fields=['public_metrics']).data.public_metrics['like_count'] for tweet_id in df['tweet_ids'] ]
    # df['retweet_count']=[ client.get_tweet(id=tweet_id,tweet_fields=['public_metrics']).data.public_metrics['retweet_count'] for tweet_id in df['tweet_ids'] ]
    # df['impression_count']=[ client.get_tweet(id=tweet_id,tweet_fields=['public_metrics']).data.public_metrics['impression_count'] for tweet_id in df['tweet_ids'] ]

    # print(f"like counts {df['likes_count']}")
    # print(f"retweet counts {df['retweet_count']}")
    # print(f"impression counts {df['impression_count']}")


    tweets_df.to_csv('tweetdata_updated.csv', index=True) 
    # print(f"keys={df['sentiment'].value_counts().index.tolist()}")
    # print(f"values={df['sentiment'].value_counts().values}")


    # # declaring data 
    # data = df['sentiment'].value_counts().values
    # keys = df['sentiment'].value_counts().index.tolist() 

    # plotpie(data,keys,string_value.get('name'))
    
   
if __name__ == "__main__":
    run()


