'''
    ----How to use this script----
    
    1)  Check that the libraries used in the script are installed.
        To install a library use the pip command at the python prompt.
        Command example: pip install stop_words
    2)  Change the value of the filename variable on line 34 to the name of the collected json base.
        Example: filename = 'tweets_05_january', where the base of tweets has the filename tweets_05_january.json
    3)  At the python prompt, access the folder where the summary script file is located.
        Command example: cd C:/Users/Maria/
    4)  To start the script, enter the command at the Python prompt: python summary.py
    5)  Wait for your execution. 
        After that, the file containing the collection summary will be in the same folder where this script is located.

'''

'''
https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/entities-object
https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/extended-entities-object
https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/geo-objects
'''

import json
import time
import csv
from datetime import date
from collections import defaultdict
from collections import Counter
from stop_words import get_stop_words


filename = 'barcelona'
f = open(filename+'.json')

status_texts = defaultdict( int )
screen_names = defaultdict( int )
hashtags = defaultdict( int )
retweets = defaultdict( list )
retweeted = defaultdict( int )
rts = defaultdict( int )

repliers = defaultdict( int )
replies = defaultdict( list )
reps = defaultdict( int )

totaltw = 0
totalrt = 0
totalrep = 0
first = True

# load data
for l in f:
    try:
        t = json.loads(l)

        date = time.strptime(t['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        hour, min = date.tm_hour, date.tm_min

        date = "%02d-%02d-%02d" % (date.tm_year, date.tm_mon, date.tm_mday)
        hour_min = "%02d:%02d" % (hour,min)

        totaltw += 1

        if first:
           date_first = date
           hour_min_first = hour_min
           first = False
           print(date_first)

        status_texts[t['text']] += 1
        sn = t['user']['screen_name']
        screen_names[sn] += 1
        for h in t['entities']['hashtags']:
            hl = h['text'].lower()
            hashtags[hl] += 1

        if ('retweeted_status' in t):
           totalrt += 1
           id_str=t['retweeted_status']['id_str']
           rts[id_str] += 1
           osn=t['retweeted_status']['user']['screen_name']
           retweeted[osn] += 1
           if ( rts[id_str] == 1 ):
               link='http://twitter.com/'+osn+'/status/'+id_str
               if 'extended_tweet' in t['retweeted_status']:
                   text = t['retweeted_status']['extended_tweet']['full_text']
               else:
                   text = t['retweeted_status']['text']

               favorite = t['retweeted_status']['favorite_count']
               retweets[id_str] = [osn, link, text, favorite, id_str]

        if ('in_reply_to_screen_name' in t):
           repto_sn = t['in_reply_to_screen_name']
           if repto_sn is not None:
              totalrep += 1
              repliers[t['user']['screen_name']] += 1
              repto_id=t['in_reply_to_status_id_str']
              if repto_id is not None:
                 reps[repto_id] += 1
                 if (reps[repto_id] == 1):
                    link='http://twitter.com/'+repto_sn+'/status/'+repto_id
                    replies[repto_id] = [repto_sn, link, '', '', repto_id]

    except:
        continue

f.close()

print(date)

stop_words = get_stop_words('english')
stop_words += get_stop_words('portuguese')

# remove no alpha from words
words = [w.lower() for t in status_texts for w in t.split() if len(w)>3 and w.lower() not in stop_words and w.isalpha()]

fcsv = open(filename +'_summary.csv','w', newline='', encoding='utf-8')
writer = csv.writer(fcsv)

# generates a header in csv
writer.writerow(['Date/time of the 1st processed tweet (Greenwich)', date_first, hour_min_first ])
writer.writerow(['Date/time of the last tweet (Greenwich)', str(date), hour_min])
writer.writerow(['Tweets count',totaltw])
writer.writerow(['Retweets count',totalrt, totalrt/totaltw])
writer.writerow(['Replies count',totalrep, totalrep/totaltw])
writer.writerow(['.','.'])

for label, data in (('Most common terms', words), 
                    ('Most used hashtags', hashtags),
                    ('Profiles that most tweeted (RT, Reply or new post)', screen_names),
                    ('Most retweeted profiles:', retweeted),
                    ('Profiles that most commented:', repliers)):
    writer.writerow([label, 'Count'])
    c = Counter(data)
    l = c.most_common()[:10]
    writer.writerows(l)
    writer.writerow(['.','.'])

c = Counter(rts)
l = c.most_common()[:20]
writer.writerow(['Most retweeted tweets:'])
writer.writerow(['RTs count', 'Profile', 'Link', 'Text', 'Favourites count', 'id_str'])
for rt in l:
    row = [rt[1]] # count
    li = retweets[rt[0]]
    if li is not None:
        for field in li:
            row.append(field)
        writer.writerow(row)
writer.writerow(['.','.'])

c = Counter(reps)
l = c.most_common()[:20]
writer.writerow(['Most commented tweets:'])
writer.writerow(['Replies count', 'Profile', 'Link', '', '', 'id_str'])

for rep in l:
    row = [rep[1]] # count
    li = replies[rep[0]]
    if li is not None:
        for field in li:
            row.append(field)
        writer.writerow(row)
writer.writerow(['.','.'])

fcsv.close()