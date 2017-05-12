import re
import glob

def general_func(alg, model, input_txt):
    return alg(model, input_txt)
def tokenizer(file):
    txt = None
    with open(file, 'r') as ct_file:
        txt = ct_file.read()
        txt = re.findall("\w+",str.lower(txt))
    return txt
def Vocabulary(folder):
    dict = {}
    for file in folder:
        lsw = None
        lsw = tokenizer(file)
        filename = file.split('/')[2]
        for w in lsw:
            if w in dict:
                if file in dict[w]:
                    dict[w][filename] += 1
                else: dict[w][filename] = 1
            else:
                dict[w] = {}
                dict[w][filename] = 1
    for file in folder:
        lsw = None
        lsw = tokenizer(file)
        filename = file.split('/')[2]
        for w in lsw:
            if w in dict:
                if filename in dict[w]:
                    dict[w][filename] += 1
                else: dict[w][filename] = 1
            else:
                dict[w] = {}
                dict[w][filename] = 1
    return dict

def wordFeatures(unigram):

    a = []
    for i in unigram:
        if len(unigram[i]) < 2:
            a.append(i)
        total = 0
        for j in unigram[i]:
            total += unigram[i][j]
        if total < 5:
            if i not in a:
                a.append(i)
    for word in a:
        del unigram[word]
    return unigram
def getFilesList(files):
    a = []
    for i in files:
        i = i.split('/')[2]
        a.append(i)
    return a


def combinedFeatures(dict):
    t = glob.glob('shakespeare/comedies/*.txt')
    list = getFilesList(t)
    biclass = {}
    for i in dict:
        biclass[i] = {}
        biclass[i]['comedy'] = 0
        biclass[i]['tragedy'] = 0
        for j in dict[i]:
            if j in list:
                biclass[i]['comedy'] += dict[i][j]
            else:
                biclass[i]['tragedy'] += dict[i][j]
    for word in biclass:
        if biclass[word]['comedy'] < 5:
            biclass[word]['comedy'] = 0
        if biclass[word]['tragedy'] < 5:
            biclass[word]['tragedy'] = 0
    a = []
    for i in biclass:
        total = 0
        for j in biclass[i]:
            total += biclass[i][j]
        if total < 5:
            if i not in a:
                a.append(i)
    for word in a:
        del biclass[word]



    return biclass

def getFeatures(input):
    return combinedFeatures(wordFeatures(Vocabulary(input)))


if __name__== '__main__':
    t = glob.glob('shakespeare/comedies/*.txt') + \
        glob.glob('shakespeare/tragedies/*.txt')
    s = combinedFeatures(wordFeatures(Vocabulary(t)))
    print  s



