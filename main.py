
from translate import Translation
from sentiment import classifier
# from sentiment import sentiment_value
import tweepy

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

    print(response)

    dates_lc = []
    tweets_count_lc = []    

    for i in range(len(response.data)):
        dates_lc.append(response.data[i]['start'][:10])
        tweets_count_lc.append(response.data[i]['tweet_count'])
  


    # plotlc(tweets_count_lc,dates_lc,encoded_string)
    plotlc(tweets_count_lc,dates_lc,string_value.get('name'))



    # response = client.get_tweet(id=1775153735594819790,tweet_fields=['public_metrics'])
                                 
    # print(f"response {response.data.public_metrics['like_count']}")
  
    # print(f"response {response.data.public_metrics['like_count']}")



    # data = "1775208854936080704"
    # # data = client.get_user(username = user,user_fields = ["public_metrics"])
    # # followers = data[0].public_metrics['followers_count']
    # # following = data[0].public_metrics['following_count'] 
    # likecount = data.public_metrics.like_count
    # print(likecount)

    response = client.search_recent_tweets(query = string_value.get('name') ,max_results=10)
    print("response = ",response)
       
    tweets_container= [[tweetread.id,tweetread.text] for tweetread in response.data]  
    columns=['tweet_ids', 'tweets text']

    tweets_df = pd.DataFrame(tweets_container,columns=columns)
    tweets_df.to_csv('tweetdata.csv', index=True)  

    df = pd.read_csv("tweetdata.csv")
    df['toenglish']=[Translation(twee) for twee in df['tweets text']]
    
    df['sentiment']=[classi['label'] for classi in classifier(list(df['toenglish']))]
    df['percent']=[round(classi['score'],4)*100 for classi in classifier(list(df['toenglish']))]
    # df['likes_count']=[ client.get_tweets(ids=df['tweet_ids'].to_list(),tweet_fields=['public_metrics']).data.public_metrics['like_count']]
    # df['likes_count']=[ client.get_tweet(id=tweet_id,tweet_fields=['public_metrics']).data.public_metrics['like_count'] for tweet_id in df['tweet_ids'] ]
    # df['sentiment_tblob']= [TextBlob(classi).sentiment.polarity for classi in df['toenglish']]

    df.to_csv('tweetdata_updated.csv', index=True) 
    print(f"keys={df['sentiment'].value_counts().index.tolist()}")
    print(f"values={df['sentiment'].value_counts().values}")


    # declaring data 
    data = df['sentiment'].value_counts().values
    keys = df['sentiment'].value_counts().index.tolist() 

    plotpie(data,keys,string_value.get('name'))
    
   
if __name__ == "__main__":
    run()


