import json, os, re, string
import commands as cmd
# import sqlite3 as sq
import sys


def email_to_tuple(filenames, to_file=False, output="out"):
    """ Converts a list of the Enron emails to a list of tuples.
    Input:
    ------
    List of filenames with absolute paths.

    Output:
    -------
    Tuple representation of an email.
    (sender, recipient, message)
    """

    emails = list()
    for mail in filenames:
        is_forwarded = False
        f = open(mail, 'r')
        email = dict()
        while True:
            line = f.readline()
            if not line:
                break
            elif line.rfind("-Original Message-") is not -1:
                is_forwarded = True
                break
            elif line.startswith("From: "):
                email["sender"] = line.lstrip("From: ").rstrip()
            elif line.startswith("To: "):
                email["recipient"] = line.lstrip("To: ").rstrip()
            elif line.startswith("Date: "):
                email["date"] = line.lstrip("Date: ").rstrip()
            elif line.startswith("X-FileName: "):
                break
        if is_forwarded:
            body = "".join([line, f.read().strip()])
        else:
            body = f.read().strip()
        f.close()
        email["message"] = body
        # email["message"] = parse_message(body, is_forwarded)
        emails.append( tuple([email["sender"], email["recipient"], email["message"]]) )
    return tuple(emails)


def walkdir(location):
    """ Gather all enron email files under specified
    location directory.
    """
    filelist = list()
    for dirname, dirnames, filenames in os.walk(location):
        for filename in filenames:
            if filename.endswith("."):
                filelist.append(os.path.join(dirname, filename))
    return filelist


def parse_message(body, is_forwarded):
    """ Given the body of an email as a string, returns a
    comma-separated string of ALL words, all lowercase.  If
    message is forwarded, ignores forwarded text.
    """
    if is_forwarded:


    tokens = re.findall(r"[\w']+" + string.punctuation, body)

    return



def set_up(con, keepold=True):
    with con:
        cur = con.cursor()
        if not keepold:
            cur.execute(
                "DROP TABLE IF EXISTS Emails")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Emails(Sender TEXT, Recipient TEXT, Message TEXT)")


def insert_email(con, emails):

    with con:
        cur = con.cursor()
        cur.executemany("INSERT INTO Emails VALUES(?, ?,?)", emails)


def getMsg(sender, recipient):
    """p1, p2 are string which represents persons' name. return value should be a
     list of lists of strings, in which every
     list of strings represent one email and every string represent a word. 
     All words should be in lower cases."""
    con = sq.connect("test.db")
    with con:
        cur = con.cursor()
        cur.execute(
            "SELECT Message from (SELECT * from Emails where Recipient=?) where Sender=?", (recipient, sender, ))
        rows = cur.fetchall()
        package = []
        for r in rows:
            words = r[0].split(',')
            package.append(words)
        return package


def getSender():
    """return value is a list of strings. Every string represents a person's name."""
    pass


def getReceiver(sender):
    """return value is a list of strings. Every string represents a person's name
     to whom sender has sent emails."""
    pass


def getWordList():
    """return value is a list of strings. 
    Every string represents a word appear in Enron data. All words should be in lower cases."""
    pass
