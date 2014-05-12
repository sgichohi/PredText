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

---------------------------------------------------------------------


Sunday April 30
---------------
Interface required by Qinxiang:

getMsg(p1, p2): p1, p2 are string which represents persons' name. return value should be a list of lists of strings, in which every list of strings represent one email and every string represent a word. All words should be in lower cases.

getSender(): return value is a list of strings. Every string represents a person's name.

getReceiver(sender): return value is a list of strings. Every string represents a person's name to whom sender has sent emails.

getWordList(): return value is a list of strings. Every string represents a word appear in Enron data. All words should be in lower cases.

getGoogleData(word_chain): return value is a integers. in which if word_chain is"A,B,C" and output is 10, it means, "A B C" appears for 10 times in google data. Input is ensure to be appeared in Enron data.

---------------------------------------------------------------------

Friday May 9
------------
Accomplished:
   1. Established testing module (SG)
   2. Tested database functions (SG)
   3. Tested EM Algorithm (CQ)
   
Tasks:
   1. write script that puts emails from one sender into the database (NL)
         - inputs: name of one of the enron correspondnets
         - walks the mail directory and gets all their sent items
         - parses the message body into the tuple format
         - puts the comma-separated body string into database using EmailAgent.insert_email()

   2. finish parsing email message body (NL)
         - handle forwarded messages!
         - remove punctuation and whitespace but don't ignore any words

   3. Write unit tests (ALL!)

NEXT MEETING: 5/10, SPELMAN!

---------------------------------------------------------------------


Saturday May 10
---------------
Accomplished:
   1. Added tests for utils.parse_message().
   2. Edited utils.walkdir() to filter by keyword.
   3. Wrote insert_by_sender() in main.py.
   4. Tested EM Algorithm on some samples!

   
Tasks:
   1. Test main.insert_by_sender().

NEXT MEETING: 5/11, SPELMAN!

---------------------------------------------------------------------

Sunday May 11
-------------
Accomplished:
   1. Cleaned up enron email directory and pushed some sample emails to repo.
   2. Computed the probabilities of some emails and got realistic results.
   3. Issue: It may take a long time to get data from Google ngrams API due to its large size and that we only care about ngrams that appear in the Enron dataset.  Solution: use BigQuery in order to make requests.
   4. Issue: Online text prediction---can we suggest words as the user is typing?  Solution: sure.


Miscellaneous
-------------
Here are just some musings worth documenting in preparation for the writeup.  Feel free to add your thoughts.

Improvements/Future Work:
   1. Better handling of punctuation.  Exclamations, questions, periods can be very expressive and telling of relationship dynamics.
 
   2. Spelling correction?  Sometimes our algorithm will get stumped when it finds an unknown prefix.  If we had more time we could compute word distance in order to try to match the user input with words that we know from the Google dataset.