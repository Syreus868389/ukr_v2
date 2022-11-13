import pickle
import itertools

def unpickle_corpus(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

#tweets_corpus = list(unpickle_corpus('corpus_en_zelensky.pickle'))
#
#tweets = list(itertools.chain.from_iterable(tweets_corpus))

