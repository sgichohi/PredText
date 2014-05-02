import random

def regularize(p):
    double sum = 0
    for x in p:
        sum = sum + x
    q = []
    for x in p
        q.append (x/sum)
    return q

def dis_add(dic, key, v)
    if (dic.has_key(key)):
        dic[key] = dic[key] + v
    else:
        dic[key] = v

class EMAlgorithm:
    def __init__(self):
        self.K = 4;
        self.N = 5;
        nameList

    def possible(msg, (W, D)):
    ''' To be written '''

    def count(count, msgs, post):
        for msg in msgs:
            if (length(msg) >= self.N):
                for i in range(self.K):
                    dic_add(count[i][0], msg[:(self.N - 1)], post[i])
                    for j in range(length(msg) - self.N):
                        dic_add(count[i][1], msg[j:j+self.N], post[i])

    def init():
        post = emptyPosterior()
        for s1 in nameList:
            for s2 in nameList:
                post[s1][s2][randrange(0, K)]
        return post
    
    def EStep(cnt):
        post = emptyPosterior()
        for s1 in nameList:
            for s2 in nameList:
                msg = getMsg(s1, s2)
                p = []
                for i in range(K):
                    p.append(possible(msg, cnt[i]))
                post[s1][s2] = regularize(p)
        return post

    def MStep(post):
        cnt = emptyCount()
        for s1 in nameList:
            for s2 in nameList:
                msg = getMsg(s1, s2)
                count(cnt, msg, post[s1][s2])
        return cnt

