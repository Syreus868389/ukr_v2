import twint
from deep_translator import LibreTranslator

def fetcher(base_query: str, date_from: str, date_to: str, hide_output=True, languages = ["fr"]):
    """
    Args:
        base_query (string): can be multiple words
        languages (list): has to be a list
        dates (string): format YYYY-MM-DD
    
    Results:
        returns a dict of twint tweet objects
    """

    base_query = base_query

    results = {}

    languages = languages
    queries = [base_query]


    for lang in languages:
        queries.append(LibreTranslator(source='en',target=lang).translate(base_query))

    languages.insert(0, 'en')

    with open('queries.txt', 'w', encoding='utf-8') as query_file:
        query_file.write(' '.join(queries))
        query_file.close()


    c = twint.Config()
    c.Custom = ['datestamp','username', 'name', 'user_id', 'tweet', 'hashtags', 'link', 'likes_count', 'replies_count', 'retweets_count', 'lang']
    c.Filter_retweets = True
    c.Retries_count = 40
    c.Until = date_to
    c.Since = date_from
    c.Hide_output = hide_output
    c.Utc = False
    c.Full_text = True
    c.Store_object = True
    c.Count = True

    for query, lang in zip(queries, languages):
        print(query)
        c.Search = query
        c.Lang = lang
        twint.run.Search(c)

        out_tweets = twint.output.tweets_list
        results[lang] = out_tweets
    
    return results






