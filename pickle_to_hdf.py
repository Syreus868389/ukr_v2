import pickle
import pandas as pd
import vaex
from unpickler import unpickle_corpus

i = 0

pickle_gen = unpickle_corpus('corpus_en_zelensky.pickle')

for tweets in pickle_gen:
    print (len(tweets))
    tweets_list = []
    for tweet in tweets:
        tweets_list.append({"tweet": tweet.tweet, "id": tweet.id, "datetime": tweet.datetime, "username" : tweet.username, "name": tweet.name, "mentions": " ".join([(mention["name"] + " " + mention["id"]) for mention in tweet.mentions]), "reply_to" : " ".join([(reply_to["name"] + " " + reply_to["id"]) for reply_to in tweet.reply_to]), "replies_count": tweet.replies_count, "retweets_count": tweet.retweets_count, "likes_count": tweet.likes_count, "hashtags": " ".join(tweet.hashtags), "retweet": tweet.retweet, "link": tweet.link})
    print(tweets_list[0])

    df = None

    df = pd.DataFrame.from_records(tweets_list)
    df_v = None
    df_v = vaex.from_pandas(df)

    if i == 0:
        df_concat = df_v
    else:
        df_concat.concat(df_v)
    
    i += 1
    tweets_list=[]
        
df_concat.export_hdf5("corpus_en_zelensky.hdf5")

