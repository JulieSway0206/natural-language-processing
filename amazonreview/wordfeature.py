import pandas as pd
from cleanwords import Textprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
import numpy as np

if __name__ == '__main__':
    train = pd.read_csv("data/train_data.csv", header=0)
    test = pd.read_csv("data/test_data.csv", header=0)

    Text = Textprocessing()

    print "Processing training reviews..."
    cleanTrain = []
    for text in train['Text']:
        cleanTrain.append(" ".join(Text.get_wordlist(text, False)))
    print  "Processing test reviews..."
    cleanTest = []
    for text in test['Text']:
        cleanTest.append(" ".join(Text.get_wordlist(text, False)))

    print "Creating features..."
    featurer = CountVectorizer(analyzer="word",
                               tokenizer= None,
                               preprocessor= None,
                               stop_words='english',
                               max_features= 40)
    featurer.fit(cleanTrain)
    train_features = featurer.transform(cleanTrain)
    np.asarray(train_features)
    test_features = featurer.transform(cleanTest)
    np.asarray(test_features)
    print "Fitting a random forest model..."
    forest = RandomForestClassifier(n_estimators=100)
    forest.fit(train_features, train['Score'])
    result = forest.predict(test_features)

    # print "Writting to WordFeature.csv..."
    # output = pd.DataFrame(data={'Id':test['Id'], 'Score':result})
    # output.to_csv("WordFeature.csv", index=False, quoting=3)

    pred_data = result
    true_data = test['Score']
    x = accuracy_score(true_data, pred_data)
    print "Presicion: %f" % x

