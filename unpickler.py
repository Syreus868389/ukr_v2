import pickle
import itertools

def unpickle_corpus(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

    tweets_corpus = list(loadall('corpus_en_ukraine_zelensky_putin_nuclear.pickle'))

    tweets = list(itertools.chain.from_iterable(tweets_corpus))

    return tweets

