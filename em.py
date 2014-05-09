import random
import math

COG = 0.01 

'''-----------------------------------------

A posterio has type String -> list double. list double represent a distribution.
A cnt has type list (list String -> double). 
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

def possible(n_words, count_data):
    while (not (n_words[:-1] in count_data)):
        n_words = n_words[1:]
    if (n_words in count_data):
        return count_data[n_words]/ count_data[n_words[:-1]]
    else:
        return 0

def dic_add(dic, key, v):
    if (dic.has_key(key)):
        dic[key] = dic[key] + v
    else:
        dic[key] = v

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
            prior.append(0)
        return prior

    def emptyPosterior(self):
        post = {}
        for nm in self.nameList:
            post[nm] = []
            for i in range(self.K):
                post[nm].append(0)
        return post

    def emptyCount(self):
        cnt = []
        for i in range(self.K):
            cnt.append({})
        return cnt

    def initPosterior(self):
        post = self.emptyPosterior()
        for nm in self.nameList:
            post[nm][random.randrange(0, self.K)] = 1   # randrange (0,K) gives return in [0, K - 1]
        return post
    
    def loglihood(self, msg, cnti):
        if (length(msg) >= self.N):
            res = math.log(possible(cnt[0], msg[:(self.N - 1)]))
            for i in range(length(msg) - self.N + 1):
                res += math.log(possible(cnt[1], msg[i: i + self.N + 1]))
            return res
        else:
            return 0
            
    def count(self, count, msg, post_p):
        if (length(msg) >= self.N):
            dic_add(count[0], msg[:(self.N - 1)], post_p)
            for i in range(length(msg) - self.N):
                dic_add(count[1], msg[i: i + self.N + 1], post_p)

    def EStep(self, cnt, prior):
        post = emptyPosterior()
        for nm in self.nameList:
            msg = self.msg[nm]
            p = []
            for i in range(K):
                p.append(loglihood(msg, cnt[i]) + math.log(prior[i]))
            post[nm] = regularize(p)
        return post

    def MStep(self, post):
        cnt = self.emptyCount()
        prior = self.emptyPrior()
        for nm in self.nameList:
            for i in range(self.K):
                prior[i] += post[nm][i]
                for msg in self.msgs[nm]:
                    count(cnt[i], msg, post[nm][i])
        return cnt

em_sample = EMAlgorithm (lambda : ["aaa", "bbb"], lambda x: ["a"])
print em_sample.nameList
print em_sample.msgs
print em_sample.initPosterior()
