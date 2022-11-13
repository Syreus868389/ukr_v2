from fetcher import fetcher
import pandas as pd

corpus = {}

query = "lfl"
languages = ['fr','ru']

tweets = fetcher(query, date_from="2022-11-05", date_to="2022-11-10", date_interval=3, languages=languages)