PredText
========
424 Final project
Collaborators: Cao Qinxiang (CQ), Samuel Gichohi (SG), Nicole Loncke (NL)

Sunday April 27
---------------
Accomplished:
   1. established outline of EM model
   2. basic formatting of emails

Tasks:
   1. get database working with JSON dumps (SG + NL)
          - return all words with given prefix
          - return bag of words in each email (w/ frequency count)
          - return bag of all correspondents
          - return all messages between (person1, person2)
          - {word: frequency} dictionary for Google dataset

   2. begin coding EM for training our model (CQ)

NEXT MEETING: 4/30, 7PM Sherrerd Hall!
------------------------------------------------------


Sunday April 30
---------------
Interface required by Qinxiang:

getMsg(p1, p2): p1, p2 are string which represents persons' name. return value should be a list of lists of strings, in which every list of strings represent one email and every string represent a word. All words should be in lower cases.

getSender(): return value is a list of strings. Every string represents a person's name.

getReceiver(sender): return value is a list of strings. Every string represents a person's name to whom sender has sent emails.

getWordList(): return value is a list of strings. Every string represents a word appear in Enron data. All words should be in lower cases.

getGoogleData(word_chain): return value is a integers. in which if word_chain is [A; B; C] and output is 10, it means, "A B C" appears for 10 times in google data. Input is ensure to be appeared in Enron data.



