import re
from math import log
f = open('afp1k.txt','r')
text = f.read()
text = re.sub(r'[^\w\s]','',text).lower()


unigram = {}
bigram = {}
trigram = {}
w2 = '<<>>'
w1 = '<>'
for w in text:
    if w in unigram:
        unigram[w] += 1
    else: unigram[w] = 1
    if w1 not in bigram:
        bigram[w1] = {}
    if w not in bigram[w1]:
        bigram[w1][w] = 1
    else: bigram[w1][w] += 1

    if w2 not in trigram:
        trigram[w2] = {}
    if w1 not in trigram[w2]:
        trigram[w2][w1] = {}
    if w not in trigram[w2][w1]:
        trigram[w2][w1][w] = 1
    else: trigram[w2][w1][w] += 1
    w2 = w1
    w1 = w

def biCount(word, word1):
    if (word1 not in bigram) or (word not in bigram[word1]):
        return 0
    else: return bigram[word1][word]
def triCount(word, word1, word2):
    if (word2 not in trigram) or (word1 not in trigram[word2]) or (word not in trigram[word2][word1]):
        return 0
    else: return trigram[word2][word1][word]
def smoothedProb(c1, c2):
    return float(c1 + 0.1) / (c2 + 0.1 * len(unigram))


def trigramPro(word, word1, word2):
    return smoothedProb(triCount(word, word1, word2), biCount(word1, word2))
def computeCrossEntropy(sentence):
    word2 = '<<>>'
    word1 = '<>'
    crossEntropy = 0
    for word in sentence:
        crossEntropy -= log(trigramPro(word, word1, word2), 2)
        word2 = word1
        word1 = word
    return crossEntropy / len(sentence)
str1 = "he somehow made this analogy sound exciting instead of hopeless "
str2 = "no living humans had skeletal features remotely like these"
str3 = "frequent internet and social media users do not have higher stress levels"
str4 = "the sand the two women were sweeping into their dustpans was transferred into plastic bags"
print computeCrossEntropy(str1)
print computeCrossEntropy(str2)
print computeCrossEntropy(str3)
print computeCrossEntropy(str4)