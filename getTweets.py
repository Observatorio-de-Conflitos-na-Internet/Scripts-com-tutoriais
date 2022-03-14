'''
    ----How to use this script----
    
    1)  Check that the libraries used in the script are installed.
        To install a library use the pip command at the python prompt.
        Command example: pip install twython
    2)  Change the value of the self.f variable on line 39 to the desired name for the tweet base.
        Enter the file name followed by .json
        Example: self.f = open('tweets_05_january.json', 'a+'), where the base of tweets will have the filename tweets_05_january.json
    3)  Place the values ​​of the keys API key and API secret key obtained from the Twitter API in the variables 
        APP_KEY and APP_SECRET on lines 54 and 55.
    4)  Place the values ​​of the tokens Acess token and Acess token secret obtained from the Twitter API in the variables 
        OAUTH_TOKEN and OAUTH_TOKEN_SECRET on lines 60 and 61.
    5)  Change the value of the subjects variable to the terms to be searched when collecting tweets.
        Examples: subjects = ['term1', 'term2'], collect tweets with terms 'term1' OR 'term2'
                  subjects = ['term1 term2'],  collect tweets with terms 'term1' AND 'term2'
                  subjects = ['term1', 'term2 term3'], collect tweets with terms 'term1' OR 'term2' AND 'term3'
    6)  The language of the tweets can be modified by changing at line 73 the language attribute for the language abbreviation.
        Example: language='pt' for Portuguese or language='es' for Spanish
    7)  At the python prompt, access the folder where the script file is located.
        Command example: cd C:/Users/Maria/
    8)  To start the script, enter the command at the Python prompt: python getTweets.py
    9)  From that moment the collection is being made.
        To end the collection, end the script execution.    
        After that, the file containing the base of tweets will be in the same folder where this script is located.

'''

# -*- coding: cp1252 -*-
from twython import Twython, TwythonStreamer
import time
import json
import sys
        
class MyStreamer(TwythonStreamer):
    def __init__(self,APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
        TwythonStreamer.__init__(self,APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.f = open('barcelona.json', 'a+')

        
    def on_success(self, data):
        if 'text' in data:
            try:
                json.dump(data,self.f)
                self.f.write('\n')
            except KeyboardInterrupt:
                self.disconnect()

    def on_error(self, status_code, data):
        print (status_code)
        time.sleep(1200)

APP_KEY = ''
APP_SECRET = ''

twitter = Twython(APP_KEY, APP_SECRET)

auth = twitter.get_authentication_tokens()
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''


subjects = ['Barcelona']
query =  ','.join(subjects)

stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

while True:
    try:
        #stream.statuses.filter(track=query, tweet_mode='extended',language='pt')
        stream.statuses.filter(track=query, tweet_mode='extended',language='es')
    except:
        e = sys.exc_info()[0]
        print ('ERROR:', e)
        continue