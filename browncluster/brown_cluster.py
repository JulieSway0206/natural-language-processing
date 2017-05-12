import pickle
import math
from copy import deepcopy
from collections import Counter
from collections import defaultdict

class BrownCluster(object):
    def __init__(self, k, vocab, scan, text):
        self.k = k
        self.cluster = {}
        self.count = {}
        self.vocab = vocab
        self.weight = {}
        self.L = {}
        self.length = 0
        self.new_word = None
        self.index = self.k
        self.scan = scan
        self.text = text
        self.lexicon = dict(self.vocab)
        for i in range(len(self.text)):
            self.length += len(text[i])

    def initialization(self):
        for i in range(self.k):
            self.cluster[i] = []
            self.cluster[i].append(self.vocab[i][0])
            self.count[i] = defaultdict(int)
            self.weight[i] = {}
            self.L[i] = {}
        '''update count'''
        for i in self.cluster:
            for w in self.cluster[i]:
                for adj in self.scan[w]:
                    for j in self.cluster:
                        if adj in self.cluster[j]:
                            if j not in self.count[i]:
                                self.count[i][j] = self.scan[w][adj]
                            else:
                                self.count[i][j] += self.scan[w][adj]
        '''update weight'''
        for i in range(self.k):
            for j in range(self.k):
                self.calculate_weight(i, j)

        ''' update L'''
        keylst = self.cluster.keys()
        for i in range(len(keylst) - 1):
            for j in range(i + 1, len(keylst)):
                self.calculate_L(keylst[i], keylst[j])
        # for i in range(1, len(keylst)):
        #     for j in range(i):
        #         self.L[keylst[i]][keylst[j]] = self.L[keylst[j]][keylst[i]]


    def calculate_weight(self, i, j):
        total_i = 0
        total_j = 0
        for w in self.cluster[i]:
            total_i  += self.lexicon[w]
        for w in self.cluster[j]:
            total_j  += self.lexicon[w]
        if i == j:
            self.weight[i][j] = (float(self.count[i][j]) / self.length)* \
                                (math.log(self.length * (self.count[i][j]+0.1), 10) - math.log(total_i * total_j,10))
        else:
            self.weight[i][j] = (float(self.count[i][j]) / self.length) \
                                * (math.log(self.length * (self.count[i][j]+0.1), 10)
                                   - math.log(total_i * total_j, 10)) \
                                + (self.count[j][i] / self.length) \
                                  * (math.log(self.length * (self.count[j][i]+0.1), 10) - math.log(total_i * total_j,10))

    def calculate_L(self, i, j):

        assumed_count = deepcopy(self.count)
        assumed_count[i]  = Counter(assumed_count[i]) + Counter(assumed_count[j])
        del assumed_count[j]
        for t in assumed_count:
            assumed_count[t][i] += assumed_count[t][j]
            del assumed_count[t][j]

        #mergedCount = Counter(self.count[i])+Counter(self.count[j])

        assumed_weight = {}
        assumed_weight[i] = {}
        for tag in assumed_count:
            total_i = 0
            total_tag = 0
            for w in self.cluster[i]+self.cluster[j]:
                total_i += self.lexicon[w]
            for w in self.cluster[tag]:
                total_tag += self.lexicon[w]
            if i == tag:
                assumed_weight[i][tag] = (float(assumed_count[i][tag]) / self.length) \
                                    * (math.log(self.length * (assumed_count[i][tag]+0.1), 2) - math.log(
                    total_i * total_tag, 2))
            else:
                assumed_weight[i][tag] = (float(assumed_count[i][tag]) / self.length) \
                                    * (math.log(self.length * (assumed_count[i][tag]+0.1), 2)
                                       - math.log(total_i * total_tag, 2)) \
                                    + (assumed_count[tag][i] / self.length) \
                                      * (math.log(self.length * (assumed_count[tag][i]+0.1), 2) - math.log(total_i * total_tag, 2))

            old_sum = sum(self.weight[i].values()) + sum(self.weight[j].values())
            new_sum = sum(assumed_weight[i].values())
            self.L[i][j] = new_sum - old_sum

    def pop_out(self):
        index = self.index
        self.new_word = self.vocab[index][0]
        self.cluster[index] = []
        self.cluster[index].append(self.new_word)
    def count_after_new_cluster(self):
        index = self.index
        self.count[index] = defaultdict(int)
        for w in self.scan[self.new_word]:
            for tag in self.cluster:
                if w in self.cluster[tag]:
                    if tag not in self.count[index]:
                        self.count[index][tag] = self.scan[self.new_word][w]
                    else:
                        self.count[index][tag] += self.scan[self.new_word][w]
        for i in self.cluster:
            if i != index:
                for w in self.cluster[i]:
                    if self.new_word in self.scan[w]:
                        if index not in self.count[i]:
                            self.count[i][index] = self.scan[w][self.new_word]
                        else:
                            self.count[i][index] += self.scan[w][self.new_word]
    def weight_after_new_cluster(self):
        self.weight[self.index] = {}
        for j in self.cluster:
            self.calculate_weight(self.index, j)
        for tag in self.cluster:
            self.weight[tag][self.index] = self.weight[self.index][tag]
    def L_after_new_cluster(self):

        self.L[self.index] = {}
        for j in self.cluster:
            if j != self.index:
                self.calculate_L(self.index, j)
        keylst = self.cluster.keys()
        print keylst
        for i in range(len(keylst)-1):
            for j in range(i+1, len(keylst)):
                if keylst[j] == self.index:
                    self.L[keylst[i]][keylst[j]] = self.L[self.index][keylst[i]]
                else:
                    total_i = 0
                    total_index = 0
                    for w in self.cluster[keylst[i]]+self.cluster[keylst[j]]:
                        total_i += self.lexicon[w]
                    for w in self.cluster[self.index]:
                        total_index += self.lexicon[w]
                    assumed_count = {k: Counter(v) for k, v in self.count.iteritems()}
                    assumed_count[keylst[i]] += Counter(assumed_count[keylst[j]])
                    assumed_weight = (float(assumed_count[keylst[i]][self.index]) / self.length) \
                                                  * (math.log(self.length * (assumed_count[keylst[i]][self.index] + 0.1), 10)
                                                     - math.log(total_i * total_index, 10)) \
                                                  + (assumed_count[self.index][keylst[i]] / self.length) \
                                                    * (math.log(self.length * (assumed_count[self.index][keylst[i]] + 0.1),

                                                            10) - math.log(total_i * total_index, 10))
                    self.L[keylst[i]][keylst[j]] += assumed_weight - (self.weight[keylst[i]][self.index]+self.weight[keylst[j]][self.index])

        # for i in range(1, len(keylst)-1):
        #     for j in range(i):
        #         self.L[keylst[i]][keylst[j]] = self.L[keylst[j]][keylst[i]]

        self.index += 1


    def argmaxOfL(self):
        cur = float('-inf')
        argCur = 0
        for i in self.L:
            if len(self.L) != 0:
                for j in self.L[i]:
                    value = self.L[i][j]
                    if value > cur:
                        cur = value
                        argCur = (i,j)
        return argCur



    def merge(self):

        merge_1,merge_2 = self.argmaxOfL()
        print('winners are {} and {}, value being {}.'.format(merge_1,merge_2,self.L[merge_1][merge_2]))
        self.cluster[merge_1] += self.cluster[merge_2]
        del self.cluster[merge_2]
        self.count[merge_1] = Counter(self.count[merge_1])+Counter(self.count[merge_2])
        del self.count[merge_2]
        for t in self.count:
            self.count[t][merge_1] += self.count[t][merge_2]
            del self.count[t][merge_2]
    def update_after_merge(self):
        keylst = self.cluster.keys()
        self.weight = {}
        self.L = {}
        for i in range(len(keylst)-1):
            self.weight[keylst[i]] = {}
            self.L[keylst[i]] = {}
            for j in range(i + 1, len(keylst)):
                self.calculate_weight(keylst[i], keylst[j])
        for i in range(1,len(keylst)):
            if i == len(keylst)-1:
                self.weight[keylst[i]] = {}
                self.L[keylst[i]] = {}
            for j in range(0,i):
                self.weight[keylst[i]][keylst[j]] = self.weight[keylst[j]][keylst[i]]

        for i in range(len(keylst) - 1):
            for j in range(i + 1, len(keylst)):
                self.calculate_L(keylst[i], keylst[j])
        # for i in range(1, len(keylst)):
        #     for j in range(i):
        #         self.L[keylst[i]][keylst[j]] = self.L[keylst[j]][keylst[i]]


if __name__ == '__main__':
    with open('vocabulary.pickle', 'rb') as handle:
        vocab = pickle.load(handle)
    with open('scan.pickle', 'rb') as handle:
        scan = pickle.load(handle)
    with open('text.pickle', 'rb') as handle:
        text = pickle.load(handle)
    Bcluster = BrownCluster(40, vocab, scan, text)
    Bcluster.initialization()
    # print(Bcluster.count)
    for i in range(40, 200):
        if i % 10 == 0:
            print "processing %d words of % d words"%(i, len(vocab))
        Bcluster.pop_out()
        Bcluster.count_after_new_cluster()
        Bcluster.weight_after_new_cluster()
        Bcluster.L_after_new_cluster()
        # print Bcluster.L
        Bcluster.merge()
        Bcluster.update_after_merge()
    print Bcluster.cluster
