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


def summ(p):
    (lb, lx) = (False, 0)
    for (b, x) in p:
        if b and lb:
            lx = max(lx, x)
            lb = True
        elif b and not lb:
            lx = x
            lb = True
    pp = []
    sum = 0
    for (b, x) in p:
        if (not b):
            pp.append((b, x))
        elif (x < lx - 20):
            pp.append((False, x))
        else:
            pp.append((True, math.exp(x - lx)))
            sum = sum + math.exp(x - lx)
    print sum * math.exp(lx)
    return (True, math.log(sum) + lx)


def regularize(p):
    # print p
    (lb, lx) = (False, 0)
    for (b, x) in p:
        if b and lb:
            lx = max(lx, x)
            lb = True
        elif b and not lb:
            lx = x
            lb = True
    pp = []
    sum = 0
    for (b, x) in p:
        if (not b):
            pp.append((b, x))
        elif (x < lx - 20):
            pp.append((False, x))
        else:
            pp.append((True, math.exp(x - lx)))
            sum = sum + math.exp(x - lx)
    # print pp
    q = []
    for (b, x) in pp:
        if b:
            q.append(x / sum)
        else:
            q.append(0)
    # print q
    return q


def connect(word_list):
    return ",".join(word_list)


def possible(count_data, n_words):
    # print "----- FOR TEST: ", count_data, n_words
    if (not (connect(n_words[:-1]) in count_data)):
        return possible(count_data, n_words[1:])
    else:
        if (connect(n_words) in count_data):
            if (n_words[1:] == []):
                return count_data[connect(n_words)] / count_data[connect(n_words[:-1])]
            else:
                return (possible(count_data, n_words[1:]) + count_data[connect(n_words)]) / (1 + count_data[connect(n_words[:-1])])
        else:
            if (n_words[1:] == []):
                return 0.0
            else:
                return possible(count_data, n_words[1:]) / (1 + count_data[connect(n_words[:-1])])
'''        
    while (not (connect(n_words[:-1]) in count_data)):
        n_words = n_words[1:]
    if (connect(n_words) in count_data):
        return count_data[connect(n_words)]/ count_data[connect(n_words[:-1])]
    else:
        return 0
'''


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
        self.N = 3
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
            # randrange (0,K) gives return in [0, K - 1]
            post[nm][random.randrange(0, self.K)] += 0.5
        for nm in self.nameList:
            # randrange (0,K) gives return in [0, K - 1]
            post[nm][random.randrange(0, self.K)] += 0.2
        for nm in self.nameList:
            # randrange (0,K) gives return in [0, K - 1]
            post[nm][random.randrange(0, self.K)] += 0.1
        for nm in self.nameList:
            # randrange (0,K) gives return in [0, K - 1]
            post[nm][random.randrange(0, self.K)] += 0.1
        for nm in self.nameList:
            # randrange (0,K) gives return in [0, K - 1]
            post[nm][random.randrange(0, self.K)] += 0.05
        for nm in self.nameList:
            # randrange (0,K) gives return in [0, K - 1]
            post[nm][random.randrange(0, self.K)] += 0.05
        return post

    def loglihood(self, msg, count):
        # print "----- FOR TEST: ", msg, count
        if (len(msg) >= self.N):
            res = logg(possible(count[0], [msg[0]]))
            # print res
            for i in range(len(msg)):
                if i > 0:
                    res = addd(
                        res, logg(possible(count[1], msg[max([0, i - self.N + 1]): i + 1])))
                    # print res
            return res
        else:
            return (True, 0)

    def count(self, count, msg, post_p):
        if (len(msg) >= self.N):
            dic_add(count[0], [], post_p)
            dic_add(count[0], [msg[0]], post_p)
            # print msg
            for i in range(len(msg) - self.N + 1):
                for j in range(self.N + 1):
                    dic_add(count[1], msg[i: i + j], post_p)
                    # print msg[i: i + j]

    def EStep(self, prior, cnt):
        post = self.emptyPosterior()
        for nm in self.nameList:
            msgs = self.msgs[nm]
            p = []
            # print nm
            for i in range(self.K):
                pi = logg(prior[i])
                # print pi
                for msg in msgs:
                    pi = addd(pi, self.loglihood(msg, cnt[i]))
                    # print pi
                p.append(pi)
                # print "------------", p
            post[nm] = regularize(p)
            # print "------------", post[nm]
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

    def solve(self, init_post, loop_num):
        post = init_post
        for i in range(loop_num):
            print i
            (prior, cnt) = self.MStep(post)
            post = self.EStep(prior, cnt)
            # print prior
            # print cnt
            # print post
        return (post, cnt)

    def eval(self, nm, msg, (post, cnt)):
        p = []
        print "-------------"
        for i in range(self.K):
            pi = self.loglihood(msg, cnt[i])
            p.append(addd(logg(post[nm][i]), pi))
        return summ(p)


class TestEMAlgorithm:

    def __init__(self, getMsg, getSenders, getReceivers, getWordList):
        self.sender = getSenders()[0]
        self.nameList = getReceivers(self.sender)
        self.msgs = lambda nm: getMsg(self.sender, nm)

    def getGoogleRequests(self):
        em_sample = EMAlgorithm(1, lambda: self.nameList, self.msgs)
        post = em_sample.initPosterior()
        (prior, cnt) = em_sample.MStep(post)
        res = cnt[0][1].keys()
        ress = []
        for word in res:
            ress.append(word.replace(',', ' '))
        return (ress)

    def test(self, rcv):
        em_sample = EMAlgorithm(4, lambda: self.nameList, self.msgs)
        print "Testing sender: ", self.sender
        print "Receiver number: ", len(self.nameList)
        post = em_sample.initPosterior()
        para = em_sample.solve(post, 30)
        print para
        print self.msgs(rcv)[0]
        return em_sample.eval(rcv, self.msgs(rcv)[0], para)

    def test_baseline(self, rcv):
        em_sample = EMAlgorithm(1, lambda: self.nameList, self.msgs)
        post = em_sample.initPosterior()
        # print post
        para = em_sample.solve(post, 10)
        print para
        print self.msgs(rcv)[0]
        return em_sample.eval(rcv, self.msgs(rcv)[0], para)


'''
em_sample = EMAlgorithm (2, lambda : ["P1", "P2", "P3"], lambda x: [])
# print em_sample.nameList
em_sample.msgs["P1"] = [["a", "b", "a", "b", "c", "a", "a", "b", "a", "b", "b", "a", "b", "a", "b"],
                        ["b", "a", "b", "b", "a", "b", "a", "a", "b", "a", "b", "c", "a", "a", "b"],
                        ["a", "b", "b", "c", "a", "a", "b", "a", "b", "a", "b", "a", "b", "a", "b"]]
em_sample.msgs["P2"] = [["a", "a", "a", "a", "c", "a", "a", "b", "b", "b", "b", "b", "b", "b", "b"],
                        ["b", "a", "a", "a", "a", "c", "a", "a", "b", "b", "b", "b", "b", "b", "b"],
                        ["a", "a", "a", "a", "c", "a", "a", "a", "b", "b", "b", "b", "b", "b", "b", "a", "a", "a", "a", "a", "b"]]
em_sample.msgs["P3"] = [["xx", "yy", "xx", "xx", "xx", "yy", "xx", "xx", "xx", "yy", "xx", "xx", "xx"],
                        ["xx", "xx", "xx", "yy", "xx", "xx", "xx", "yy", "xx", "xx", "xx", "yy", "xx"],
                        ["xx", "yy", "xx", "xx", "yy", "xx", "yy", "xx", "xx", "xx", "xx", "xx", "xx"]]

post = em_sample.initPosterior()
for nm in em_sample.nameList:
    for i in range(em_sample.K):
        post[nm][i] = post[nm][i] * 0.1 + 0.9 / em_sample.K
# post = {'P2': [0.65, 0.05, 0.2, 0.1], 'P1': [0.05, 0.55, 0.1, 0.30000000000000004]}
# post = {'P2': [0.545, 0.455], 'P3': [0.48000000000000004, 0.52], 'P1': [0.545, 0.455]}
print post

para = em_sample.solve(post, 10)
print para[0]
print em_sample.eval("P1", ["a", "b", "a", "b", "c", "a", "a", "b", "a", "b", "b", "a", "b", "a", "b"], para)





em_sample = EMAlgorithm (1, lambda : ["P1", "P2", "P3"], lambda x: [])
# print em_sample.nameList
em_sample.msgs["P1"] = [["a", "b", "a", "b", "c", "a", "a", "b", "a", "b", "b", "a", "b", "a", "b"],
                        ["b", "a", "b", "b", "a", "b", "a", "a", "b", "a", "b", "c", "a", "a", "b"],
                        ["a", "b", "b", "c", "a", "a", "b", "a", "b", "a", "b", "a", "b", "a", "b"]]
em_sample.msgs["P2"] = [["a", "a", "a", "a", "c", "a", "a", "b", "b", "b", "b", "b", "b", "b", "b"],
                        ["b", "a", "a", "a", "a", "c", "a", "a", "b", "b", "b", "b", "b", "b", "b"],
                        ["a", "a", "a", "a", "c", "a", "a", "a", "b", "b", "b", "b", "b", "b", "b", "a", "a", "a", "a", "a", "b"]]
em_sample.msgs["P3"] = [["xx", "yy", "xx", "xx", "xx", "yy", "xx", "xx", "xx", "yy", "xx", "xx", "xx"],
                        ["xx", "xx", "xx", "yy", "xx", "xx", "xx", "yy", "xx", "xx", "xx", "yy", "xx"],
                        ["xx", "yy", "xx", "xx", "yy", "xx", "yy", "xx", "xx", "xx", "xx", "xx", "xx"]]

post = em_sample.initPosterior()
# post = {'P2': [1.0], 'P1': [1.0]}
print post

para = em_sample.solve(post, 10)
print para[0]
print em_sample.eval("P1", ["a", "b", "a", "b", "c", "a", "a", "b", "a", "b", "b", "a", "b", "a", "b"], para)
'''

'''
{'P2': [0.545, 0.455], 'P3': [0.48000000000000004, 0.52], 'P1': [0.545, 0.455]}
{'P2': [1.0, 0], 'P3': [0, 1.0], 'P1': [1.0, 0]}
(True, -8.200638876455583)
{'P2': [1.0], 'P3': [1.0], 'P1': [1.0]}
{'P2': [1.0], 'P3': [1.0], 'P1': [1.0]}
(True, -8.606103984563749)
'''
