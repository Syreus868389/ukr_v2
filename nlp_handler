import re
import spacy
from spellchecker import SpellChecker
from spacy_experimental.coref.coref_component import DEFAULT_COREF_MODEL
from spacy_experimental.coref.coref_util import DEFAULT_CLUSTER_PREFIX

config={
    "model": DEFAULT_COREF_MODEL,
    "span_cluster_prefix": DEFAULT_CLUSTER_PREFIX,
    }

def cleaner(text, lang):
    checker = SpellChecker(language=lang)
    no_urls = " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", text).split())
    spell_list = no_urls.split()
    for word in spell_list:
            if word not in checker:
                try:
                    cor = checker.correction(word)
                    clean_text = text.replace(word, cor)
                except:
                    continue
    return clean_text.lower()


class TweetHandler:
    def __init__(self, tweet_text, lang="fr"):
        self.text = cleaner(tweet_text)

        if lang == "fr":
            self.nlp = spacy.load("fr_dep_news_trf")
        elif lang == "en":
            self.nlp = spacy.load("en_core_web_trf")

        self.doc = self.nlp(self.text)
        
        return self.doc

    def get_clean_tokens(self):
        self.tokens = [token for token in self.doc if token.text not in self.nlp.Defaults.stop_words]

        return self.tokens

    def get_processed_tokens(self):
        self.processed_tokens = []
        for chunk in self.doc.noun_chunks:
            for token in chunk:
                token_content = TokenHandler(chunk, token)
                self.processed_tokens.append(token_content)

        return self.processed_tokens   


class TokenHandler:
    def __init__(self, chunk, token):
        self.chunk = chunk
        self.text = token.text
        self.token = token
        

def clusters(text, lang="fr"):
    if lang == "fr":
            nlp = spacy.load("fr_dep_news_trf", disable=["tagger", "attribute_ruler", "lemmatizer","ner"])
    elif lang == "en":
        nlp = spacy.load("en_core_web_trf")

    nlp.add_pipe("experimental_coref", config=config)

    doc = nlp(doc)

    return doc.spans["coref_clusters"]



