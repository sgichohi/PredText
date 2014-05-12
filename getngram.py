#!/usr/bin/env python


import gevent.monkey
gevent.monkey.patch_all()

from ast import literal_eval
import gevent.pool
import re
import requests               # http://github.com/kennethreitz/requests
import subprocess
import sys
import gevent
from em import connect


corpora = dict(eng_us_2012=17, eng_us_2009=5, eng_gb_2012=18, eng_gb_2009=6,
               chi_sim_2012=23, chi_sim_2009=11, eng_2012=15, eng_2009=0,
               eng_fiction_2012=16, eng_fiction_2009=4, eng_1m_2009=1,
               fre_2012=19, fre_2009=7, ger_2012=20, ger_2009=8, heb_2012=24,
               heb_2009=9, spa_2012=21, spa_2009=10, rus_2012=25, rus_2009=12,
               ita_2012=22)


def getNgrams(query, corpus, startYear, endYear, smoothing, caseInsensitive):
    params = dict(content=query, year_start=startYear, year_end=endYear,
                  corpus=corpora[corpus], smoothing=smoothing,
                  case_insensitive=caseInsensitive)
    if "you said it" in query:
        log("We found you in query!")
    log("-----&&&&&-----           " + query)
    if params['case_insensitive'] is False:
        params.pop('case_insensitive')
    if '?' in params['content']:
        params['content'] = params['content'].replace('?', '*')
    if '@' in params['content']:
        params['content'] = params['content'].replace('@', '=>')
    hdr = {'User-Agent': "Magic Browser"}
    req = requests.get(
        'http://books.google.com/ngrams/graph', headers=hdr, params=params)
    res = re.findall('var data = (.*?);\\n', req.text)
    try:
        data = {qry['ngram']: sum(qry['timeseries']) / float(len(qry['timeseries']))
                for qry in literal_eval(res[0])}
    except IndexError:
        print "No result"
        data = {}
    if "you said it" in data:
        log("We found you 46!")
    return data


def runQuery(argumentString):
    #argumentString = connect(argumentString)

    arguments = argumentString.split()
    query = ' '.join([arg for arg in arguments if not arg.startswith('-')])
    if '?' in query:
        query = query.replace('?', '*')
    if '@' in query:
        query = query.replace('@', '=>')
    params = [arg for arg in arguments if arg.startswith('-')]
    corpus, startYear, endYear, smoothing = 'eng_2012', 1950, 2005, 0
    printHelp, caseInsensitive, allData = False, True, False
    toSave, toPrint, toPlot = False, False, False

    # parsing the query parameters
    for param in params:
        if '-nosave' in param:
            toSave = False
        elif '-noprint' in param:
            toPrint = False
        elif '-plot' in param:
            toPlot = True
        elif '-corpus' in param:
            corpus = param.split('=')[1].strip()
        elif '-startYear' in param:
            startYear = int(param.split('=')[1])
        elif '-endYear' in param:
            endYear = int(param.split('=')[1])
        elif '-smoothing' in param:
            smoothing = int(param.split('=')[1])
        elif '-caseInsensitive' in param:
            caseInsensitive = True
        elif '-alldata' in param:
            allData = True
        elif '-help' in param:
            printHelp = True
        else:
            print 'Did not recognize the following argument: %s' % param
    if printHelp:
        print 'See README file.'
    else:
        if '*' in query and caseInsensitive is True:
            caseInsensitive = False
            notifyUser = True
            warningMessage = "*NOTE: Wildcard and case-insensitive " + \
                             "searches can't be combined, so the " + \
                             "case-insensitive option was ignored."
        elif '_INF' in query and caseInsensitive is True:
            caseInsensitive = False
            notifyUser = True
            warningMessage = "*NOTE: Inflected form and case-insensitive " + \
                             "searches can't be combined, so the " + \
                             "case-insensitive option was ignored."
        else:
            notifyUser = False
        data = getNgrams(query, corpus, startYear, endYear,
                         smoothing, caseInsensitive)
        return data


def log(thing):
    with open("log.txt", "arw") as log:
        log.write(thing + "\n")


def reqNgram(pattern_list):
    log("hey")

    chunks = [connect(pattern_list[x:x + 10])
              for x in xrange(0, len(pattern_list), 10)]

    pool = gevent.pool.Pool(5)
    results = pool.map(runQuery, chunks)
    big_dict = {}
    for dic in results:
        for d in dic:
            log(d)

            if "(ALL)" in d:
                d = d.replace("(ALL)", "")

            if d in big_dict:
                big_dict[d] += dic[d]
            else:
                big_dict[d] = dic[d]

    return big_dict

if __name__ == '__main__':
    argumentString = ' '.join(sys.argv[1:])
    if argumentString == '':
        argumentString = raw_input('Enter query (or -help):')
    else:
        try:
            print reqNgram(argumentString)
        except:
            print 'An error occurred.'
