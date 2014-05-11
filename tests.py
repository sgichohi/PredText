import commands as cmd
import sqlite3 as sq
import utils
import words
import unittest
import em


class TestUtilFunctions(unittest.TestCase):

    """Tests that run the functions in utils.py and words.py
    """

    def setUp(self):
        """Set up any class values you need here"""
        self.testdb = "test.db"
        self.emailag = words.EmailAgent(self.testdb, True)
        emails = (("today", "sam", "cool,hey"), )
        self.emailag.insert_email(emails)
        # self.emailag.set_up(False)

    def test_getMsg(self):

        self.assertEqual(
            self.emailag.getMsg("today", "sam"), [["cool", "hey"]])

      # self.assertEqual(self.seq, range(10))

      # should raise an exception for an immutable sequence
      # self.assertRaises(TypeError, random.shuffle, (1,2,3))

      # self.assertTrue(element in self.seq)
    def test_getSenders(self):

        self.assertEqual(self.emailag.getSenders(), ["today"])

    def test_getReceiver(self):
        self.assertEqual(self.emailag.getReceiver("today"), ["sam"])

    def test_getWordList(self):
        print self.emailag.getWordList()
        self.assertEqual(
            sorted(self.emailag.getWordList()), sorted(["cool", "hey"]))

    def test_parse_message_punctuation(self):
        body = "hey,girl,  hey! \n\n What's up??? :)"
        self.assertEqual(utils.parse_message(body), "hey,girl,hey,what's,up")

    def test_parse_message_fwd(self):
        body = "hey,girl,  hey! \n\nLook at this :) \n\n-----Original Message-----\n\nSEND TO ALL YOUR FRIENDS..."
        self.assertEqual(
            utils.parse_message(body), "hey,girl,hey,look,at,this")

    def test_parse_message_fwd_empty(self):
        body = "\n\n-----Original Message-----\n\n SEND TO ALL YOUR FRIENDS..."
        self.assertEqual(utils.parse_message(body), "")

    def test_parse_message_empty(self):
        body = ""
        self.assertEqual(utils.parse_message(body), "")


def gm(x, y):
    if y == "P1":
        return [
            ["a", "b", "a", "b", "c", "a", "a", "b",
                "a", "b", "b", "a", "b", "a", "b"],
            ["a", "b", "b", "c", "a", "a", "b", "a", "b", "a", "b", "a", "b", "a", "b"]]
    else:
        return [
            ["a", "a", "a", "a", "c", "a", "a", "b",
                "b", "b", "b", "b", "b", "b", "b"],
            ["a", "a", "a", "a", "c", "a", "a", "a", "b", "b", "b", "b", "b", "b", "b", "a", "a", "a", "a", "a", "b"]]


class TestEM(unittest.TestCase):

    def testHEYYYY(self):
        print "HEYYYYYYYYYYYYYY"
        gs = lambda: ["s"]
        gr = lambda x: ["P1", "P2"]
        tt = em.TestEMAlgorithm(gm, gs, gr, (), ())
        print tt.test("P1")
        print tt.test_baseline("P1")

if __name__ == '__main__':
    unittest.main()
