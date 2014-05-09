import commands as cmd
import sqlite3 as sq
import utils
import words
import unittest


class TestUtilFunctions(unittest.TestCase):

    """
    Tests that run the functions in util.py
    """

    def setUp(self):
        """Set up any class values you need here"""
        self.testdb = "test.db"
        self.emailag = words.EmailAgent(self.testdb)
        self.emailag.set_up(False)

    def test_getMsg(self):

        emails = (("today", "sam", "cool,hey"), )
        self.emailag.insert_email(emails)
        self.assertEqual(
            self.emailag.getMsg("today", "sam"), [["cool", "hey"]])

    # self.assertEqual(self.seq, range(10))

    # should raise an exception for an immutable sequence
    # self.assertRaises(TypeError, random.shuffle, (1,2,3))

    # self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()
