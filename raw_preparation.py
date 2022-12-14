import vaex

paths = ['corpus_fr_#IStandWithUkraine_2022-02-24_to_2022-06-30_enriched.hdf5', 'corpus_fr_Boutcha_2022-02-24_to_2022-06-30_enriched.hdf5', 'corpus_fr_Marioupol_2022-02-24_to_2022-06-30_enriched.hdf5', 'corpus_fr_marioupol_AND_théâtre_2022-02-24_to_2022-06-30_enriched.hdf5']
queries = ['#IStandWithUkraine', 'boutcha', 'marioupol', 'marioupol & théâtre']

dfs = []

for path, query in zip(paths, queries):
    df = vaex.open(path)
    df['keyword'] = df.tweet.str.slice(0, 0) + query

    dfs.append(df)

new_df = vaex.concat(dfs, resolver = 'strict')

new_df.drop(['tweet','id','datetime','username','name','mentions','reply_to','replies_count','retweets_count','likes_count','hashtags','retweet','link'], inplace=True)

print(new_df)

new_df.export_csv('concat_cdcm.csv')
