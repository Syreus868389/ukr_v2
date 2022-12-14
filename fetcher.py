import twint
import translators as ts
from datetime import datetime
import pickle
from time_utils import *
import vaex
import pandas
import os
from operations import remove_duplicates_from_df

cwd = os.getcwd()

def nukedir(dir):
    if dir[-1] == os.sep: dir = dir[:-1]
    files = os.listdir(dir)
    for file in files:
        if file == '.' or file == '..': continue
        path = dir + os.sep + file
        if os.path.isdir(path):
            nukedir(path)
        else:
            os.unlink(path)
    os.rmdir(dir)

def fetcher(base_query: str, date_from: str, date_to: str, date_interval: int, hide_output=True, english = True, languages = ["fr"], translate = True):
    """
    Args:
        base_query (string): can be multiple words
        english: use english language - default is true
        languages (list): has to be a list
        dates (string): format YYYY-MM-DD
        date_interval : number of days for a chunk
    
    Returns:
        a list of strings indicating the paths of the exported files
    """

    with open("fetch_index.pickle", "rb") as index_ledger:
        saved_i = pickle.load(index_ledger) 
    
    with open("langs_done.pickle", "rb") as langs_ledger:
        langs_done = pickle.load(langs_ledger)

    final_files = []

    datespans = list(resolve_interval(date_from, date_to, date_interval))

    if english:
        task_amount = (len(datespans) - 1) * (len(languages) + 1)
    else:
        task_amount = (len(datespans) - 1) * (len(languages))

    base_query = base_query

    languages = languages
    queries = [base_query]


    if translate:
        for lang in languages:
            queries.append(ts.google(base_query, from_language='en', to_language=lang).lower())
    else:
        for lang in languages:
            queries.append(base_query)

    if english:
        languages.insert(0, 'en')

    with open('queries.txt', 'w', encoding='utf-8') as query_file:
        query_file.write(' '.join(queries))
        query_file.close()


    c = twint.Config()
    c.Custom = ['datestamp','username', 'name', 'user_id', 'tweet', 'hashtags', 'link', 'likes_count', 'replies_count', 'retweets_count', 'lang']
    c.Filter_retweets = True
    c.Retries_count = 40
    c.Hide_output = hide_output
    c.Utc = False
    c.Full_text = True
    c.Store_object = True
    c.Count = True

    for outer_i, (query, lang) in enumerate(zip(queries, languages)):
        dir = os.path.join(cwd, f'{query.replace(" ", "_")}_{lang}_{date_from}_to_{date_to}')

        if not os.path.exists(dir):
            os.mkdir(dir)

        if saved_i is False or saved_i['query'] !=base_query:
                saved_i = {}
                saved_i['query'] = base_query
                saved_i['index'] = 0
                saved_i['lang'] = lang
                langs_done = []

                with open("fetch_index.pickle", "wb") as index_ledger:
                    pickle.dump(saved_i, index_ledger, protocol=pickle.HIGHEST_PROTOCOL)

                with open("langs_done.pickle", "wb") as langs_ledger:
                    pickle.dump(langs_done, langs_ledger, protocol=pickle.HIGHEST_PROTOCOL)

        if lang not in langs_done:
            corpus_filename = f'corpus_{lang}_{query.replace(" ", "_")}_{date_from}_to_{date_to}'

            slice = saved_i['index'] + 1

            for i, span in enumerate(datespans[slice:]):

                c.Until = span
                c.Since = datespans[slice + i - 1]
                c.Search = query
                c.Lang = lang
                twint.run.Search(c)

                out_tweets = twint.output.tweets_list

                if out_tweets:

                    tweet_list = []

                    for tweet in out_tweets:
                        tweet_list.append({"tweet": tweet.tweet, "id": tweet.id, "datetime": tweet.datetime, "username" : tweet.username, "name": tweet.name, "mentions": " ".join([(mention["name"] + " " + mention["id"]) for mention in tweet.mentions]), "reply_to" : " ".join([(reply_to["name"] + " " + reply_to["id"]) for reply_to in tweet.reply_to]), "replies_count": tweet.replies_count, "retweets_count": tweet.retweets_count, "likes_count": tweet.likes_count, "hashtags": " ".join(tweet.hashtags), "retweet": tweet.retweet, "link": tweet.link})

                    df_p = remove_duplicates_from_df(pandas.DataFrame.from_records(tweet_list))

                    df_v = vaex.from_pandas(df_p)

                    df_v.export_hdf5((os.path.join(dir, f'{corpus_filename}_{slice+i}.hdf5')))

                new_saved_i = {'query': base_query, 'index': slice + i, 'lang': lang}

                with open("fetch_index.pickle", "wb") as index_ledger:
                    pickle.dump(new_saved_i, index_ledger, protocol=pickle.HIGHEST_PROTOCOL)

                status_msg = f'Chunk {(slice+i) + ((len(datespans)-1) * outer_i)}/{task_amount} has been fetched'

                print(status_msg)

            print("Merging and exporting data")

            fetched_files_list = [os.path.join(dir, filepath) for filepath in os.listdir(dir)]


            fetched_files_df = vaex.open_many(fetched_files_list)

            fetched_files_df.export_hdf5(f'{corpus_filename}.hdf5')

            final_files.append(f'{corpus_filename}.hdf5')

            fetched_files_df.close()

            print("Export successful!")

            langs_done = languages[0:outer_i]

            with open("langs_done.pickle", "wb") as index_ledger:
                    pickle.dump(langs_done, index_ledger, protocol=pickle.HIGHEST_PROTOCOL)

            print(f'Lang {languages[outer_i]} done')

            next_lang= outer_i+1

            if next_lang in range(len(languages)):
                print(f"Next language is {languages[next_lang]}")
                saved_i = {'query': base_query, 'index': 0, 'lang': languages[next_lang]}

                with open("fetch_index.pickle", "wb") as index_ledger:
                    pickle.dump(saved_i, index_ledger, protocol=pickle.HIGHEST_PROTOCOL)
            
    for lang, query in zip(languages, queries):
        nukedir(os.path.join(cwd, f'{query.replace(" ", "_")}_{lang}_{date_from}_to_{date_to}'))

    end_msg = f"Fetching done for query '{base_query}'"
    
    print(end_msg)

    return final_files