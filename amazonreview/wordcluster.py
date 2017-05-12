import numpy as np
from cleanwords import Textprocessing
from gensim.models import  Word2Vec as w2v
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.ensemble import  RandomForestClassifier
from sklearn.metrics import accuracy_score



def create_centroid_feature(wordlst, word_to_tag, numCluster):
    centroid_feature = np.zeros(numCluster, dtype="float32")
    for w in wordlst:
        if w in word_to_tag:
            tag = word_to_tag[w]
            centroid_feature[tag] += 1
    return centroid_feature



if __name__ == '__main__':
    model = w2v.load("review_to_vec")
    word_to_vectors = model.syn0
    clusterNum = word_to_vectors.shape[0]/20

    print "Running Kmean..."
    clustering = KMeans(n_clusters=clusterNum)
    clustering.fit(word_to_vectors)
    tag = clustering.predict(word_to_vectors)

    word_to_tag = dict(zip(model.index2word, tag))
    train = pd.read_csv("data/train_data.csv", header=0)
    test = pd.read_csv("data/test_data.csv", header=0)

    Text = Textprocessing()
    print "Processing training reviews..."
    cleanTrain = []
    for text in train['Text']:
        cleanTrain.append(Text.get_wordlist(text, True))
    print "Processing test reviews..."
    cleanTest = []
    for text in test['Text']:
        cleanTest.append(Text.get_wordlist(text,True))

    print "Creating training features.."
    train_centroids = np.zeros((train["Text"].size, clusterNum), dtype="float32")
    num = 0
    for review in cleanTrain:
        train_centroids[num] = create_centroid_feature(review, word_to_tag, clusterNum)
        num += 1
    print "Creating test features"
    test_centroid = np.zeros((test['Text'].size, clusterNum), dtype="float32")
    num = 0
    for review in cleanTest:
        test_centroid[num] = create_centroid_feature(review, word_to_tag, clusterNum)
        num += 1

    print "Fitting a random forest model..."
    forest = RandomForestClassifier(n_estimators= 100)
    forest.fit(train_centroids, train['Score'])
    result = forest.predict(test_centroid)

    # output = pd.DataFrame(data={'Id':test['Id'], 'Score': result})
    # output.to_csv("WordCluster.csv", index=False, quoting=3)
    # print "Writing to WordCluster.csv"

    pred_data = result
    true_data = test['Score']
    x = accuracy_score(true_data, pred_data)
    print "Presicion: %f" % x




