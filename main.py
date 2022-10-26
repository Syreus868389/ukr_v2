from fetcher import fetcher
import pandas as pd

corpus = {}

tweets = fetcher("ukraine zelensky putin nuclear", date_from="2022-10-01", date_to="2022-10-18", date_interval=3)