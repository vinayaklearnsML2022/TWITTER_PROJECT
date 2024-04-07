import tweepy



## Load the secret variables
from dotenv import load_dotenv
import os


   

def initialise():
    
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
    return client



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