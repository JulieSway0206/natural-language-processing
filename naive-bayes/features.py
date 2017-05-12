from naivebayes import getFeatProb
import  operator
import glob
def feat(listfiles):
    comedy = {}
    tragedy = {}
    dict = getFeatProb(listfiles)
    prob = {}
    for word in dict:
        prob[word] = dict[word]['comedy'] - dict[word]['tragedy']
    sorted_comedy = sorted(prob.items(), key=operator.itemgetter(1),reverse=True)
    sorted_tragedy = sorted(prob.items(), key=operator.itemgetter(1),reverse=False)
    print '20 most comic features:'
    for index, feature in enumerate(sorted_comedy):
        if index == 19:
            break
        print '%s likelihood ratio: %0.2f' % (feature[0], feature[1])
    print '\n20 most tragic features:'
    for index, feature in enumerate(sorted_tragedy):
        if index == 19:
            break
        print '%s likelihood ratio: %0.2f' % (feature[0], feature[1])






if __name__ == '__main__':
    t = glob.glob('shakespeare/comedies/*.txt') + \
    glob.glob('shakespeare/tragedies/*.txt')
    feat(t)