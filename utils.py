import json, os, re, string, sys
import commands as cmd


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
            elif line.startswith("X-From: ") and "sender" not in email.keys():
                email["sender"] = line.lstrip("X-From: ").rstrip()
            elif line.startswith("X-To: ") and "recipient" not in email.keys():
                email["recipient"] = line.lstrip("X-To: ").rstrip()
            elif line.startswith("X-FileName: "):
                break
        body = f.read().strip()
        f.close()
        email["message"] = parse_message(body)
        emails.append( tuple([email["sender"], email["recipient"], email["message"]]) )
    return tuple(emails)


def walkdir(location, keywords=[""]):
    """ Gather all enron email files under specified location
    directory. Returns list of relative paths, e.g. location/whatever...
    """
    filelist = list()
    for dirname, dirnames, filenames in os.walk(location):
        if all([query in dirname for query in keywords]):
            for filename in filenames:
                if filename.endswith("."):
                    filelist.append(os.path.join(dirname, filename))
    return filelist


def parse_message(body):
    """ Given the body of an email as a string, returns a
    comma-separated string of ALL words, all lowercase, punctuation
    removed.  If message is forwarded, ignores forwarded text.
    """
    orig = body.split("-Original Message-")[0]
    allpunc = string.punctuation.replace('\'', "")  # keep apostrophes in words
    transtable = string.maketrans(allpunc, len(allpunc)*" ")
    nopunc = orig.translate(transtable)
    tokens = [word.lower() for word in nopunc.split()]
    return ",".join(tokens)