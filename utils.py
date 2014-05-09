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