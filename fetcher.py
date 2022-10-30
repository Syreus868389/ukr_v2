import twint
import translators as ts
from datetime import datetime
import pickle
from time_utils import *

def fetcher(base_query: str, date_from: str, date_to: str, date_interval: int, hide_output=True, languages = ["fr"]):
    """
    Args:
        base_query (string): can be multiple words
        languages (list): has to be a list
        dates (string): format YYYY-MM-DD
        date_interval : number of days for a chunk
    
    Results:
        only return a string indicating that the fetching is finished
    """

    with open("fetch_index.pickle", "rb") as index_ledger:
        saved_i = pickle.load(index_ledger) 
    
    with open("langs_done.pickle", "rb") as langs_ledger:
        langs_done = pickle.load(langs_ledger)

    datespans = list(resolve_interval(date_from, date_to, date_interval))

    task_amount = (len(datespans) - 1) * (len(languages) + 1)

    base_query = base_query

    languages = languages
    queries = [base_query]


    for lang in languages:
        queries.append(ts.google(base_query, from_language='en', to_language=lang))

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

        if lang not in langs_done:
            corpus_filename = f'corpus_{lang}_{query.replace(" ", "_")}.pickle'

            if saved_i is False or saved_i['query'] !=base_query:
                saved_i = {}
                saved_i['query'] = base_query
                saved_i['index'] = 0
                saved_i['lang'] = lang

                with open("fetch_index.pickle", "wb") as index_ledger:
                    pickle.dump(saved_i, index_ledger, protocol=pickle.HIGHEST_PROTOCOL)

            slice = saved_i['index'] + 1

            for i, span in enumerate(datespans[slice:]): 
                c.Until = span
                c.Since = datespans[slice + i - 1]
                c.Search = query
                c.Lang = lang
                twint.run.Search(c)

                new_saved_i = {'query': base_query, 'index': slice + i, 'lang': lang}

                with open("fetch_index.pickle", "wb") as index_ledger:
                    pickle.dump(new_saved_i, index_ledger, protocol=pickle.HIGHEST_PROTOCOL)

                out_tweets = twint.output.tweets_list

                with open(corpus_filename, "ab") as corpus:
                    pickle.dump(out_tweets, corpus, protocol=pickle.HIGHEST_PROTOCOL)

                status_msg = f'Chunk {(slice+i) + ((len(datespans)-1) * outer_i)}/{task_amount} has been fetched'

                print(status_msg)

            langs_done = languages[0:outer_i]
            with open("langs_done.pickle", "wb") as index_ledger:
                pickle.dump(langs_done, index_ledger, protocol=pickle.HIGHEST_PROTOCOL)

    end_msg = f"Fetching done for query '{base_query}'"
    
    print(end_msg)






