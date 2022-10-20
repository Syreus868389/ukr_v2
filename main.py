from fetcher import fetcher
import pandas as pd

tweets = fetcher("ukraine zelensky putin nuclear", date_from="2022-10-17", date_to="2022-10-18")

for lang, values in tweets.items():
    for tweet in values:
        print(tweet.__dict__)



