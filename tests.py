import commands as cmd
import sqlite3 as sq
import utils
import unittest


class TestUtilFunctions(unittest.TestCase):

    def setUp(self):
        """Set up any class values you need here"""
        self.con = sq.connect("test.db")
        utils.set_up(self.con, False)

    def test_getMsg(self):
        emails = (("today", "sam", "cool,hey"), )
        utils.insert_email(self.con, emails)
        self.assertEqual(utils.getMsg("today", "sam"), [["cool", "hey"]])

        #self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))

        #self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()
