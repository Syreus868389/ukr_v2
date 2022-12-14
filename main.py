from fetcher import fetcher
import pandas as pd

corpus = {}

query = "marioupol AND théâtre"
languages = ['fr']

tweets = fetcher(query, date_from="2022-02-24", date_to="2022-06-30", date_interval=2, languages=languages, english = False, translate=False)