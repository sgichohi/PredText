import sqlite3 as sq


class EmailAgent():

    def __init__(self, db):
        self.con = sq.connect(db)
        self.set_up()

    def set_up(self, keepold=True):

        with self.con as con:
            cur = con.cursor()
            if not keepold:
                cur.execute(
                    "DROP TABLE IF EXISTS Emails")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS Emails(Sender TEXT, Recipient TEXT, Message TEXT)")

    def insert_email(self, emails):

        with self.con as con:
            cur = con.cursor()
            cur.executemany("INSERT INTO Emails VALUES(?, ?,?)", emails)

    def getMsg(self, sender, recipient):
        """p1, p2 are string which represents persons' name. return value should be a
        list of lists of strings, in which every
        list of strings represent one email and every string represent a word.
        All words should be in lower cases."""

        with self.con as con:
            cur = con.cursor()
            cur.execute(
                "SELECT Message from (SELECT * from Emails where Recipient=?) where Sender=?", (recipient, sender, ))
            rows = cur.fetchall()
            package = []
            for r in rows:
                words = r[0].split(',')
                package.append(words)
        return package

    def getSenders(self, ):
        """return value is a list of strings. Every string represents a person's name."""
        pass

    def getReceiver(self, sender):
        """return value is a list of strings. Every string represents a person's name
         to whom sender has sent emails."""
        pass

    def getWordList(self, ):
        """return value is a list of strings.
        Every string represents a word appear in Enron data. All words should be in lower cases."""
        pass
