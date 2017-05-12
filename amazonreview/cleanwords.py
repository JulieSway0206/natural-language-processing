from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords

class Textprocessing(object):


    def get_wordlist(self, text, remove_stopword):
        review = BeautifulSoup(text).get_text()
        review = re.sub("[^a-zA-Z]", " ", review)
        words = review.lower().split()
        if remove_stopword:
            stop = set(stopwords.words("english"))
            words = [w for w in words if not w in stop]
        return words

    def text_to_sentences(self, text, tokenizer):
        remove_stopword = False
        data = text.decode("utf8")
        raw_sentences = tokenizer.tokenize(data.strip())
        sentences = []
        for sentence in raw_sentences:
            if len(sentence) > 0:
                sentences.append(Textprocessing.get_wordlist(self, sentence,remove_stopword))
        return sentences
