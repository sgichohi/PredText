import random
import math

COG = 0.01 

'''-----------------------------------------

A posterio has type String -> list double. list double represent a distribution.
A cnt has type list (String -> double). 
A prio has type list double.

regularize(p)[i] = exp(p[i]) / sum_i exp(p[i])

-----------------------------------------'''

def regularize(p):
    largest = max(p)
    pp = []
    sum = 0
    for x in p:
        if (x < largest - 20):
            pp.append(0)
        else:
            pp.append(math.exp(x))
            sum = sum + math.exp(x)
    q = []
    for x in pp:
        q.append (x/sum)
    return q

def connect(word_list):
    return ",".join(word_list)

def possible(count_data, n_words):
    # print "----- FOR TEST: ", count_data, n_words
    while (not (connect(n_words[:-1]) in count_data)):
        n_words = n_words[1:]
    if (connect(n_words) in count_data):
        return count_data[connect(n_words)]/ count_data[connect(n_words[:-1])]
    else:
        return 0

def dic_add(dic, key, v):
    if (v == 0):
        return
    key0 = connect(key)
    if (dic.has_key(key0)):
        dic[key0] = dic[key0] + v
    else:
        dic[key0] = v

class EMAlgorithm:
    def __init__(self, getNameList, getMsgList):
        self.K = 4
        self.N = 5
        self.nameList = getNameList()
        self.msgs = {}
        for nm in self.nameList:
          self.msgs[nm] = getMsgList(nm)

    def emptyPrior(self):
        prior = []
        for i in range(self.K):
            prior.append(0.0)
        return prior

    def emptyPosterior(self):
        post = {}
        for nm in self.nameList:
            post[nm] = []
            for i in range(self.K):
                post[nm].append(0.0)
        return post

    def emptyCount(self):
        cnt = []
        for i in range(self.K):
            cnt.append(({}, {}))
        return cnt

    def initPosterior(self):
        post = self.emptyPosterior()
        for nm in self.nameList:
            post[nm][random.randrange(0, self.K)] += 0.5   # randrange (0,K) gives return in [0, K - 1]
        for nm in self.nameList:
            post[nm][random.randrange(0, self.K)] += 0.2   # randrange (0,K) gives return in [0, K - 1]
        for nm in self.nameList:
            post[nm][random.randrange(0, self.K)] += 0.1   # randrange (0,K) gives return in [0, K - 1]
        for nm in self.nameList:
            post[nm][random.randrange(0, self.K)] += 0.1   # randrange (0,K) gives return in [0, K - 1]
        for nm in self.nameList:
            post[nm][random.randrange(0, self.K)] += 0.05   # randrange (0,K) gives return in [0, K - 1]
        for nm in self.nameList:
            post[nm][random.randrange(0, self.K)] += 0.05   # randrange (0,K) gives return in [0, K - 1]
        return post
    
    def loglihood(self, msg, count):
        # print "----- FOR TEST: ", msg, count
        if (len(msg) >= self.N):
            res = math.log(possible(count[0], [msg[0]]))
            for i in range(len(msg)):
                if i > 0:
                    res += math.log(possible(count[1], msg[max([0, i - self.N + 1]): i + 1]))
            return res
        else:
            return 0
            
    def count(self, count, msg, post_p):
        if (len(msg) >= self.N):
            dic_add(count[0], [], post_p)
            dic_add(count[0], [msg[0]], post_p)
            for i in range(len(msg) - self.N):
                for j in range(self.N + 1):
                    dic_add(count[1], msg[i: i + j], post_p)

    def EStep(self, prior, cnt):
        post = self.emptyPosterior()
        for nm in self.nameList:
            msgs = self.msgs[nm]
            p = []
            for i in range(self.K):
                pi = math.log(prior[i])
                for msg in msgs:
                    pi += self.loglihood(msg, cnt[i])
                p.append(pi)
            post[nm] = regularize(p)
        return post

    def MStep(self, post):
        cnt = self.emptyCount()
        prior = self.emptyPrior()
        for nm in self.nameList:
            for i in range(self.K):
                prior[i] += post[nm][i] / len(self.nameList)
                for msg in self.msgs[nm]:
                    self.count(cnt[i], msg, post[nm][i])
        return (prior, cnt)

em_sample = EMAlgorithm (lambda : ["P1", "P2"], lambda x: [])
print em_sample.nameList
em_sample.msgs["P1"] = [["a", "b", "a", "b", "c", "a", "a", "b", "a", "b", "b", "a", "b", "a", "b"]]
em_sample.msgs["P1"] = [["a", "a", "a", "a", "c", "a", "a", "b", "b", "b", "b", "b", "b", "b", "b"]]

post = em_sample.initPosterior()
post = {'P2': [0.65, 0.05, 0.2, 0.1], 'P1': [0.55, 0.1, 0.30000000000000004, 0.05]}
print post


(prior, cnt) = em_sample.MStep(post)
print prior
print cnt
post = em_sample.EStep(prior, cnt)
print post


