import json
import os
import re
import string
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
        body = f.read().strip()
        f.close()
        email["message"] = body
        # email["message"] = parse_message(body)
        emails.append(
            tuple([email["sender"], email["recipient"], email["message"]]))
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


def parse_message(body):
    """ Given the body of an email as a string, returns a comma-separated
    string of words, all lowercase.  Words deemed unimportant include: one-letter
    words, numbers, punctuation...
    """
    tokens = re.findall(r"[\w']+" + string.punctuation, body)

    # handle forwarded emails
