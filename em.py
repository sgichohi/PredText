import random

def regularize(p):
    double sum = 0
    for x in p:
        sum = sum + x
    q = []
    for x in p
        q.append (x/sum)
    return q

def possible(msg, (W, D)):
    ''' To be written '''

def count(cnt, msg, post):
    ''' To be written '''

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


def main():
    K = 4;
    N = 5;


main()
