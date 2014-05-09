import json
import os
import commands as cmd
import sqlite3 as sq
import sys


def email_to_tuple(filenames, to_file=False, output="out"):
    """ Converts a list of the Enron emails to a list of tuples.
    """
    emails = list()
    for mail in filenames:
        f = open(mail, 'r')
        email = dict()
        while True:
            line = f.readline()
            if not line:
                break
            elif line.startswith("From: "):
                email["sender"] = line.lstrip("From: ").rstrip()
            elif line.startswith("To: "):
                email["recipient"] = line.lstrip("To: ").rstrip()
            elif line.startswith("Date: "):
                email["date"] = line.lstrip("Date: ").rstrip()
            elif line.startswith("X-FileName: "):
                break
        email["message"] = f.read().strip()
        f.close()
        emails.append(email)
    if to_file:
        with open(output, 'w') as f:
            f.write(json.dumps(emails))
    else:
        json.dumps(emails)
    return emails

# gather all enron email files under specified location directory


def walkdir(location):
    filelist = list()
    for dirname, dirnames, filenames in os.walk(location):
        for filename in filenames:
            if filename.endswith("."):
                filelist.append(os.path.join(dirname, filename))
    return filelist


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
