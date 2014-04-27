import re

def email_to_tuple(filenames):
    """ Converts a list of the Enron emails to a list of tuples.
    """
    emails = list()
    for mail in filenames:
        f = open(mail, 'r')
        email = dict()
        for line in f:
            if line.startswith("From: "):
                print line.lstrip("From: ").rstrip()
                email["sender"] = line.lstrip("From: ").rstrip()
            elif line.startswith("To: "):
                email["recipient"] = line.lstrip("To: ").rstrip()
                print line.lstrip("To: ").rstrip()
            elif line.startswith("Date: "):
                email["recipient"] = line.lstrip("Date: ").rstrip()
                print line.lstrip("Date: ").rstrip()
            elif line.startswith("X-Filename: "):
                break
        email["message"] = f.read().strip()
        f.close()
        emails.append(email)
    return emails
        
            
