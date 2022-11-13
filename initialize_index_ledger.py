import pickle

string = False
done = []

saved_i = {}
saved_i['query'] = ""
saved_i['index'] = 0
saved_i['lang'] = ""

with open('fetch_index.pickle', 'wb') as file:
    pickle.dump(saved_i, file, protocol=pickle.HIGHEST_PROTOCOL)

with open('langs_done.pickle', 'wb') as langs_done:
    pickle.dump(done, langs_done, protocol=pickle.HIGHEST_PROTOCOL)