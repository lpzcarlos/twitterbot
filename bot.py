import tweepy
import os 
import logging
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
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

def printNewTweet(data):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '00df95b4-07b9-4fe5-bed8-304fc7ce9c47',
    }
    symbolCrypto = data["text"].split()[1]
    print("symbol: " + symbolCrypto)
    parameters = {
        'symbol': symbolCrypto
    }
    session = Session()
    session.headers.update(headers)
    
    try:
        response = session.get(url, params=parameters)
        valueCrypto = json.loads(response.text)
        print(valueCrypto["data"][symbolCrypto][0]["quote"]["USD"]["price"])
       # print(valueCrypto["price"])
        return valueCrypto["data"][symbolCrypto][0]["quote"]["USD"]["price"]
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        reply_id = data["id"]
        api = create_bot_api()
        respuesta = printNewTweet(data)
        print("TweeT:" + "@" + data["user"]["screen_name"] + " " + str(respuesta))
        api.update_status("@" + data["user"]["screen_name"] + " " + str(respuesta), in_reply_to_status_id=reply_id)
        
def main():
    api = create_bot_api()
    while True:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
        myStream.filter(track=["@BotBolsa"])
    
if __name__=="__main__":
    main()



