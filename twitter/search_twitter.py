import tweepy
from translate import google
from sentiment import sentiment
from conversion import extraction_username,unicode
import re





## Load the secret variables
from dotenv import load_dotenv
import os
import pandas as pd
import multiprocessing

import deep_translator
from deep_translator import GoogleTranslator

from transformers import pipeline
import torch


from memory_profiler import profile

log_file = open('memory.log','w+')

@profile(stream=log_file)
class Twitteruse:
    def __init__(self):
        load_dotenv(override=True)
        bearertoken = os.getenv("BEARER_TOKEN")
        consumerkey = os.getenv("CONSUMER_KEY")
        consumersecret = os.getenv("CONSUMER_SECRET")
        accesstoken = os.getenv("ACCESS_TOKEN")
        accesssecret = os.getenv("ACCESS_SECRET")
                                            
        client = tweepy.Client(bearer_token=bearertoken,consumer_key=consumerkey,consumer_secret=consumersecret,
                        access_token=accesstoken,access_token_secret=accesssecret)
        auth = tweepy.OAuth1UserHandler(consumer_key=consumerkey,consumer_secret=consumersecret,
                        access_token=accesstoken,access_token_secret=accesssecret)
        api = tweepy.API(auth)
        self.client = client
        
    
    def get_tweets_count(self,search_string):
        self.search_string = search_string
        response = self.client.get_recent_tweets_count(query = self.search_string, granularity='day')
        tweets_cnt_container= [[tweetcnt['start'],tweetcnt['tweet_count']] for tweetcnt in response.data]  
        columns=['date', 'tweets_count']
        tweetstweets_count_df = pd.DataFrame(tweets_cnt_container,columns=columns)
        tweetstweets_count_df['date_only'] = [tweets[:10] for tweets in tweetstweets_count_df['date']]
        tweetstweets_count_df.to_csv('tweetcount.csv', index=True)
        return True
    
    
    def get_tweets(self,search_string1,min_date,max_date,tweet_count_slider):
        self.search_string1 = search_string1
        self.min_date = min_date
        self.max_date = max_date
        self.tweet_count_slider = tweet_count_slider

        # pool = multiprocessing.Pool()

        tweets_container= [[tweetread.id,tweetread.text,tweetread.created_at,tweetread.public_metrics['like_count'],tweetread.public_metrics['retweet_count'],tweetread['author_id']]for tweetread in tweepy.Paginator(self.client.search_recent_tweets, self.search_string1,max_results=10,start_time=self.min_date,end_time=self.max_date,tweet_fields=['public_metrics','created_at'],expansions=['author_id']).flatten(limit=self.tweet_count_slider)]  
        columns=['tweet_ids', 'tweets text','created_at','like_count','retweet_count','userid']
        tweets_df = pd.DataFrame(tweets_container,columns=columns)
        # tweets_df['conv_tweets'] = tweets_df['tweets text'].apply(lambda x : Conversion(x).unicode())
        # logging.info(f"\n\n conv_tweets formed")
        # result = pool.map(extraction_username, tweets_df['tweets text'])
        # tweets_df['user_mentions'] = pd.concat(result)

        # result = pool.map(google, tweets_df['tweets text'])
        # tweets_df['toenglish'] = pd.concat(result)

        # result = pool.map(sentiment, tweets_df['toenglish'])
        # tweets_df['sentiment'] = pd.concat(result)

        # print(tweets_df['user_mentions'])

        # classify = pipeline("sentiment-analysis",model="cardiffnlp/xlm-twitter-politics-sentiment")
        # res = classify(text)
        # return "".join(map(str, re.findall("'label': '(.*?)'",str(res))))

        # tweets_df['tweets text'].apply(GoogleTranslator(source='auto').translate[:1000])
        

        tweets_df['user_mentions'] = tweets_df['tweets text'].apply(extraction_username)
        # tweets_df['toenglish'] = tweets_df['tweets text'].apply(google)
        # tweets_df['sentiment'] = sentiment(tweets_df['tweets text'].to_list())
        
        tweets_df.to_csv('tweetdata_checking.csv') 
        # pool.close()
        
    
    def get_influencers_retweets(self):
        tweets_df = pd.read_csv('tweetdata_checking.csv')
        tweets_df__rem_user = tweets_df.copy()
        tweets_df__rem_user.dropna(axis=0,inplace=True)
        
        retweeted_tweets_df = tweets_df__rem_user.groupby('user_mentions').aggregate('max').sort_values('retweet_count',ascending=False).reset_index()[:3]
        print(retweeted_tweets_df['user_mentions'])

        followers =[]
        # location =[]

        for i in range(len(retweeted_tweets_df)):
                response = self.client.get_user(username=retweeted_tweets_df['user_mentions'].iloc[i],user_fields=['public_metrics','location'])
                user_metrics = response.data['public_metrics']
                followers.append(user_metrics['followers_count'])
                # loc_details = response.data['location']
                # location.append(loc_details)

        retweeted_tweets_df['followers']=followers
        # retweeted_tweets_df['location']=location
        
        retweeted_tweets_df = retweeted_tweets_df.drop(columns =['tweet_ids','tweets text','created_at','like_count','userid','Unnamed: 0','retweet_count'])
     

        print(retweeted_tweets_df)
        retweeted_tweets_df.to_csv('Top_influencers_from_retweeted_tweets.csv', index=True) 

         
    
    def get_influencers_likes(self):
        tweets_df = pd.read_csv('tweetdata_checking.csv',)
     

        liked_tweets_df = tweets_df.sort_values('like_count',ascending=False)[:3]

        usernames = []  
        followers =[]
 

        for i in range(len(liked_tweets_df)):
    
                response = self.client.get_user(id=liked_tweets_df['userid'].iloc[i],user_fields=['username','public_metrics','location'])
                usernames.append(response.data['username'])
                user_metrics = response.data['public_metrics']
                followers.append(user_metrics['followers_count'])
                # loc_details = response.data['location']
                # location.append(loc_details)

        liked_tweets_df['username']=usernames
        liked_tweets_df['followers']=followers
        # liked_tweets_df['location']=location
        liked_tweets_df = liked_tweets_df.drop(columns =['tweet_ids','tweets text','created_at','retweet_count','userid','Unnamed: 0','user_mentions','like_count'])

        liked_tweets_df.to_csv('Top_influencers_from_liked_tweets.csv', index=True) 
        
            
            



# my_userid = client.get_me()
# print(my_userid)
# client.create_tweet(text="I'm working on api very very new one")
# # # query=471741741
# # # response = client.get_list_tweets(my_userid)
# # print(my_userid)
# # print(get_tweet_id)
# client.delete_tweet(get_tweet_id.data.id)

# user_id = client.get_user(username = "PMOIndia")

# user_id = 471741741 
# query = "#BJP"
# response = client.search_recent_tweets(query)
# print("response = ",response)

# for i in range(10):
#     print(response[0][i].text)

# client.get_retweeters("1770295047990186190")
# # print(response)