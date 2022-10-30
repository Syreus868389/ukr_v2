import pickle

string = False
done = []

with open('fetch_index.pickle', 'wb') as file:
    pickle.dump(string, file, protocol=pickle.HIGHEST_PROTOCOL)

with open('langs_done.pickle', 'wb') as langs_done:
    pickle.dump(done, langs_done, protocol=pickle.HIGHEST_PROTOCOL)