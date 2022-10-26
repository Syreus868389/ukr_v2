import pickle

string = False

with open('fetch_index.pickle', 'wb') as file:
    pickle.dump(string,file, protocol=pickle.HIGHEST_PROTOCOL)