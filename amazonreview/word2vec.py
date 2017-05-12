from cleanwords import Textprocessing
import pandas as pd
import nltk
import logging
import gensim.models.word2vec as w2v
import glob
import codecs
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.metrics import accuracy_score


def cleanReviews(reviews):
    cleantext = []
    for review in reviews['Text']:
        Text = Textprocessing()
        cleantext.append(Text.get_wordlist(review, True))
    return cleantext

def averageVec(words, num_features, model):
    featVec = np.zeros((num_features,), dtype="float32")
    num = 0

    modelvocab = set(model.index2word)
    for w in words:
        if w in modelvocab:
            num += 1
            featVec = np.add(featVec, model[w])
    featVec = np.divide(featVec, num)
    return featVec


def getAverageVecs(reviews, num_features, model):
    counter = 0
    featvecs = np.zeros((len(reviews), num_features), dtype="float32")
    for review in reviews:
        if counter % 1000. == 0.:
            print "progress at %d of %d review feature vector"%(counter, len(reviews))
        featvecs[int(counter)] = averageVec(review, num_features,model)
        counter += 1
    return featvecs



if __name__ == '__main__':
    train = pd.read_csv("data/train_data.csv", header=0)
    test = pd.read_csv("data/test_data.csv", header=0)

    nltk.download("punkt")
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

    sentences = []
    print "Parsing sentences from training set"
    for text in train['Text']:
        Text = Textprocessing()
        sentences += Text.text_to_sentences(text, tokenizer)

    book_filenames = glob.glob('data/review_polarity/txt_sentoken/neg/*.txt') \
                     + glob.glob('data/review_polarity/txt_sentoken/pos/*.txt')

    corpus_raw = u""
    for book_filenames in book_filenames:
        corpus_raw = u""
        with codecs.open(book_filenames, "r", "utf-8") as book_file:
            corpus_raw += book_file.read()
            Text = Textprocessing()
            sentences += Text.text_to_sentences(corpus_raw, tokenizer)


    num_features = 300
    min_word_count = 40
    num_workers = 4
    context_size = 10
    downsampling = 1e-3
    seed = 1

    print "Training Word2Vec model...."
    model = w2v.Word2Vec(sentences,
        seed=seed,
        workers=num_workers,
        size=num_features,
        min_count=min_word_count,
        window=context_size,
        sample=downsampling
    )
    model.init_sims(replace=True)
    model_name = "review_to_vec"
    model.save(model_name)

    # print model.doesnt_match("love hate like".split())
    # print model.doesnt_match("amazing  boring wonderful".split())
    # print model.doesnt_match("coffee chicken tea ".split())


    print "Creating average feature vectors for training dataset"

    trainVecs = getAverageVecs(cleanReviews(train), num_features, model)

    print "Creating average feature vectors for test dataset"

    testVecs = getAverageVecs(cleanReviews(test), num_features, model)

    print "Fitting a random forest to traning reviews....."
    forest = RandomForestClassifier(n_estimators=100)

    imp1 = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imp2 = Imputer(missing_values='NaN', strategy='mean', axis=0)

    forest.fit(imp1.fit_transform(trainVecs), train['Score'])
    result = forest.predict(imp2.fit_transform(testVecs))

    # output = pd.DataFrame(data={"Id":test["Id"],"Score":result})
    # output.to_csv("Word2Vec.csv",index=False,quoting=3)
    # print "Writing to  Word2Vec.csv"

    pred_data = result
    true_data = test['Score']
    x = accuracy_score(true_data,pred_data)
    print "Presicion: %f"%x

