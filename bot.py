import tweepy
import os 
import logging
import json
import request
from tweepy.streaming import StreamListener

def create_bot_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    #Create an API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print("API Created")
    except:
        print("Error during API creation")
    return api

class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        print("Ha habido una mencion")
        print(data)
        data = json.loads(data)
        print(data["text"])
        respuesta = "tu mas &#128156;"
        api = create_bot_api()
        api.update_status("@" + data["user"]["screen_name"] + " " + respuesta, in_reply_to_status_id=data["id"])
        
def main():
    api = create_bot_api()
    #api.update_status("Hola??")
    while True:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
        myStream.filter(track=["@BotBolsa"])
    
if __name__=="__main__":
    main()



