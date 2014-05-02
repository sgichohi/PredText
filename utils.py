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


def set_up():
    with con:
        cur.execute(
            "CREATE TABLE Emails(Sender TEXT, Recipient TEXT, Message TEXT")


def insert_email(con, emails):

    with con:
        cur = con.cursor()
        cur.executemany("INSERT INTO Emails VALUES(?, ?,?)", emails)


def get_emails(sender, recipient):
    con = sq.connect("test.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT Message from Emails where Recipient=?, Sender=?" recipient, sender)
        rows = cur.fetchall()
        return rows
def

con = sq.connect("test.db")
emails = ("today", "sam", "cool")
set_up(con)
insert_email(con, emails)
