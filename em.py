import random
import math

COG = 0.01 

'''-----------------------------------------

A posterio has type String -> list double. list double represent a distribution.
A cnt has type list (String -> double). 
A prio has type list double.

regularize(p)[i] = exp(p[i]) / sum_i exp(p[i])

Possibility is a float number. Possibility after log is (bool, float).

-----------------------------------------'''

def logg(x):
    if (x < 1e-10):
        return (False, 0)
    else:
        return (True, math.log(x))

def addd((b1, x1), (b2, x2)):
    if (b1 and b2):
        return (True, x1 + x2)
    else:
        return (False, 0)

def regularize(p):
    (lb, lx) = (False, 0)
    for (b, x) in p:
        if b:
            lx = max(lx, x)
            lb = True
    pp = []
    sum = 0
    for (b, x) in p:
        if (not b):
            pp.append((b, x))
        elif (x < lx - 20):
            pp.append((False, x))
        else:
            pp.append((True, math.exp(x)))
            sum = sum + math.exp(x)
    q = []
    for (b, x) in pp:
        if b:
            q.append(x/sum)
        else:
            q.append(0)
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
    def __init__(self, K, getNameList, getMsgList):
        self.K = K
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

    # this initPosterior does not ensure a legal post as return value
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
            res = logg(possible(count[0], [msg[0]]))
            for i in range(len(msg)):
                if i > 0:
                    res = addd(res, logg(possible(count[1], msg[max([0, i - self.N + 1]): i + 1])))
            return res
        else:
            return (True, 0)
            
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
                pi = logg(prior[i])
                for msg in msgs:
                    pi = addd(pi, self.loglihood(msg, cnt[i]))
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

    def solve(self, init_post):
        post = init_post
        for i in range(10):
            (prior, cnt) = self.MStep(post)
            post = self.EStep(prior, cnt)
            print prior
            # print cnt`
            print post
        return (post, cnt)

    def eval(self, nm, msg, (post, cnt)):
        res = 0.0
        for i in range(self.K):
            pi = self.loglihood(msg, cnt[i])
            if (pi[0]):
                res += post[nm][i] * math.exp(pi[1])
        return res

em_sample = EMAlgorithm (4, lambda : ["P1", "P2"], lambda x: [])
print em_sample.nameList
em_sample.msgs["P1"] = [["a", "b", "a", "b", "c", "a", "a", "b", "a", "b", "b", "a", "b", "a", "b"]]
em_sample.msgs["P2"] = [["a", "a", "a", "a", "c", "a", "a", "b", "b", "b", "b", "b", "b", "b", "b"]]

post = em_sample.initPosterior()
post = {'P2': [0.65, 0.05, 0.2, 0.1], 'P1': [0.05, 0.55, 0.1, 0.30000000000000004]}
print post

para = em_sample.solve(post)
print em_sample.eval("P1", ["a", "b", "a", "b", "c", "a", "a", "b", "a", "b", "b", "a", "b", "a", "b"], para)





em_sample = EMAlgorithm (1, lambda : ["P1", "P2"], lambda x: [])
print em_sample.nameList
em_sample.msgs["P1"] = [["a", "b", "a", "b", "c", "a", "a", "b", "a", "b", "b", "a", "b", "a", "b"]]
em_sample.msgs["P2"] = [["a", "a", "a", "a", "c", "a", "a", "b", "b", "b", "b", "b", "b", "b", "b"]]

post = em_sample.initPosterior()
post = {'P2': [1.0], 'P1': [1.0]}
print post

para = em_sample.solve(post)
print em_sample.eval("P1", ["a", "b", "a", "b", "c", "a", "a", "b", "a", "b", "b", "a", "b", "a", "b"], para)



