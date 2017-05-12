import glob
from collections import Counter
import pickle
if __name__ == '__main__':
    files = glob.glob('brown/c*')
    lst = []
    for file in files:
        with open(file, 'r') as ct_file:
            txt = ct_file.read().lower().splitlines()
            for line in txt:
                if len(line) != 0:
                    for w in line.split(" "):
                        word = w.split('/')[0]
                        if word:
                            lst.append(word)
    wordlist = []
    for w in lst:
        if len(w.split('\t')) == 2:
            wordlist.append(w.split('\t')[1])
        else:
            wordlist.append(w.split('\t')[0])

    minorlst = []
    dct = Counter(wordlist)
    dct['UNK'] = 0
    a = []
    for w in dct:
        if dct[w] < 11:
            minorlst.append(w)
            dct['UNK'] += dct[w]
            a.append(w)
    for word in a:
        del dct[word]
    vocabulary = sorted(dct.items(), key = lambda (k,v):(-v,k))
    # print vocabulary
    # print len(vocabulary)


    '''prepare for next question'''
    with open('vocabulary.pickle', 'wb') as handle:
        pickle.dump(vocabulary, handle, protocol=pickle.HIGHEST_PROTOCOL)


    vocablst = []
    for w in vocabulary:
        vocablst.append(w[0])
    scan = {}
    for w in vocablst:
        scan[w] = {}
    text = []
    for file in files:
        with open(file, 'r') as ct_file:
            txt = ct_file.read().lower().splitlines()
            for line in txt:
                lst1 = []
                if len(line) != 0:
                    for w in line.split(" "):
                        word = w.split('/')[0]
                        if word:
                            lst1.append(word)
                wordlist = []
                for w in lst1:
                    if len(w.split('\t')) == 2:
                        wordlist.append(w.split('\t')[1])
                    else:
                        wordlist.append(w.split('\t')[0])
                if len(wordlist) != 0:
                    text.append(wordlist)
    for line in text:
        for j in range(len(line) - 1):
            if line[j] not in vocablst:
                head = 'UNK'
            else:
                head = line[j]
            if line[j+1] not in vocablst:
                tail = 'UNK'
            else:
                tail = line[j+1]
            if tail not in scan[head]:
                scan[head][tail] = 1
            else:
                scan[head][tail] += 1
    # print scan
    with open('scan.pickle', 'wb') as handle:
        pickle.dump(scan, handle,protocol=pickle.HIGHEST_PROTOCOL)
    with open('text.pickle', 'wb') as handle:
        pickle.dump(text, handle,protocol=pickle.HIGHEST_PROTOCOL)
    print scan['UNK']