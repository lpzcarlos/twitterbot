import tweepy
import os 
import logging
import json
import math
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

def newCryptoValue(data):
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
        #print(valueCrypto["data"][symbolCrypto][0]["quote"]["USD"]["price"])
        return valueCrypto#["data"][symbolCrypto][0]["quote"]["USD"]["price"]
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        reply_id = data["id"]
        #api = create_bot_api()
        jsonCrypto = newCryptoValue(data)
        priceCrypto = round((jsonCrypto["data"][data["text"].split()[1]][0]["quote"]["USD"]["price"]), 2)
        last1h = round((jsonCrypto["data"][data["text"].split()[1]][0]["quote"]["USD"]["percent_change_1h"]), 2)
        last24h = round((jsonCrypto["data"][data["text"].split()[1]][0]["quote"]["USD"]["percent_change_24h"]), 2)
        last7d = round((jsonCrypto["data"][data["text"].split()[1]][0]["quote"]["USD"]["percent_change_7d"]), 2)
        #print("Tweet:" + "@" + data["user"]["screen_name"] + " " + str(respuesta))
        #return ("@" + data["user"]["screen_name"] + " " + str(respuesta))
        api.update_status("@" + data["user"]["screen_name"] + " " 
                          + "Price: " + str(priceCrypto) + "$"
                          + "\n Last 1h: " + str(last1h) + "%"
                          + "\n Last 24h: " + str(last24h) + "%"
                          + "\n Last 7d: " + str(last7d) + "%"
                          + "\n\n #cryptocurrency #bot", 
                          in_reply_to_status_id=reply_id)
        
def main():
    global api
    api = create_bot_api()
    while True:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
        myStream.filter(track=["@BotBolsa"])
    
if __name__=="__main__":
    main()



