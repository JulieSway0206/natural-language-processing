from trainer import getFeatures
from trainer import  tokenizer
from math import log
import  glob

# def getFeatProb(corpus):
#     prob = {}
#     dict = getFeatures(corpus)
#     comedyNum = 0
#     tragedyNum = 0
#     for i in dict:
#         comedyNum += dict[i]['comedy']
#         tragedyNum += dict[i]['tragedy']
#     totalNum = comedyNum + tragedyNum
#     for word in dict:
#         prob[word] = {}
#         prob[word]['comedy'] = log(float(dict[word]['comedy'] + 0.1) / (0.1 * totalNum + comedyNum), 2)
#         prob[word]['tragedy'] = log(float(dict[word]['tragedy'] + 0.1) / (0.1 * totalNum + tragedyNum), 2)
#     return prob
#
#
# def NBmodel(play):
#     classProb = {}
#     array = []
#     com = glob.glob('shakespeare/comedies/*.txt')
#     tra = glob.glob('shakespeare/tragedies/*.txt')
#     for file in com + tra:
#         if play != file:
#             array.append(file)
#     lib = getFeatProb(array)
#     if play in com:
#         trueLabel = 'comedy'
#     else:
#         trueLabel = 'tragedy'
#     classProb[play] = {}
#     classProb[play]['comedy'] = 0
#     classProb[play]['tragedy'] = 0
#     for word in tokenizer(play):
#         if word in lib:
#             classProb[play]['comedy'] += lib[word]['comedy']
#             classProb[play]['tragedy'] += lib[word]['tragedy']
#         else:
#             classProb[play]['comedy'] = classProb[play]['comedy']
#             classProb[play]['tragedy'] = classProb[play]['tragedy']
#     if classProb[play]['comedy'] > classProb[play]['tragedy']:
#         label = 'comedy'
#     else:
#         label = 'tragedy'
#     ratio = classProb[play]['comedy'] - classProb[play]['tragedy']
#     print("Observed: %s , Expected: %s, Likelihood ratio: %0.5f \n" % (label, trueLabel, ratio))
#     if label == trueLabel:
#         return 1
#     else: return 0
#
#
#
#
#
#
# if __name__ == '__main__':
#
#     t = glob.glob('shakespeare/comedies/*.txt') + \
#         glob.glob('shakespeare/tragedies/*.txt')
#     sum = 0
#     for play in t:
#         sum += NBmodel(play)
#     accuracy = sum * 100.0 / len(t)
#     print "Accuracy: %0.2f%s" % (accuracy, "%")



