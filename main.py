from fetcher import fetcher
import pandas as pd

corpus = {}

query = "zelensky"
languages = ['fr','ru']

tweets = fetcher(query, date_from="2022-06-01", date_to="2022-10-30", date_interval=3, languages=languages)