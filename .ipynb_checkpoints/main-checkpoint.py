from translate import Translation
from sentiment import classifier
import tweepy

from twitter import search_twitter as tweet
import os
from dotenv import load_dotenv




def run():
    

    client = tweet.initialise()
                                             
    
    # print(client)
    
    # response = client.search_recent_tweets(query = "#BJP" ,max_results=10)
    # print("response = ",response)
    translated = Translation("RT @aruna_dk: పాలమూరు తల్లి ఒడ  డిలో పెరిగిన బిడ్డ.. చెమట చుక్కై ఎదిగిన నేత... ప్రజల మనసును గెలిచిన నాయకురాలు అరుణమ్మ ....\n@narendramodi @JPNa…")
    print("translated text ",translated )
    print(classifier(translated))
    # response = client.create_tweet(text="learning to tweet by machine")
    # print("response = ",response)
    # my_userid = client.get_me()
    # print(my_userid)
    # user_id = client.get_user(username="narendramodi")
    # print(user_id)
   


if __name__ == "__main__":
    run()


