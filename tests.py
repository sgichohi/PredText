import commands as cmd
import sqlite3 as sq
import utils
import words
import unittest

class TestUtilFunctions(unittest.TestCase):
   """Tests that run the functions in utils.py and words.py
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

   def test_parse_message_punctuation(self):
      body = "hey,girl,  hey! \n\n What's up??? :)"
      self.assertEqual(utils.parse_message(body), "hey,girl,hey,what's,up")

   def test_parse_message_fwd(self):
    body = "hey,girl,  hey! \n\nLook at this :) \n\n-----Original Message-----\n\nSEND TO ALL YOUR FRIENDS..."
    self.assertEqual(utils.parse_message(body), "hey,girl,hey,look,at,this")

   def test_parse_message_fwd_empty(self):
      body = "\n\n-----Original Message-----\n\n SEND TO ALL YOUR FRIENDS..."
      self.assertEqual(utils.parse_message(body), "")

   def test_parse_message_empty(self):
      body = ""
      self.assertEqual(utils.parse_message(body), "")
      
class TestEMAlgorithm:
    def __init__(self, getMsg, getSenders, getReceivers, getWordList, getGoogleData):
        self.sender = getSenders() [0]
        self.nameList = getReceivers(self.sender)
        self.msgs = lambda nm: getMsg(self.sender, nm)

    def test(self, msg):
        em_sample = EMAlgorithm (4, lambda : self.nameList, self.msgs)
        post = em_sample.initPosterior()
        para = em_sample.solve(post, 10)
        return em_sample.eval(self.nameList[0], self.msgs(self.nameList[0])[0], para)

    def test_baseline(self, msg):
        em_sample = EMAlgorithm (1, lambda : self.nameList, self.msgs)
        post = em_sample.initPosterior()
        para = em_sample.solve(post, 10)
        return em_sample.eval(self.nameList[0], self.msgs(self.nameList[0])[0], para)

class TestEM:
    def gm(x, y):
        if y == "P1":
            return [["a", "b", "a", "b", "c", "a", "a", "b", "a", "b", "b", "a", "b", "a", "b"]]
        else:
            return [["a", "a", "a", "a", "c", "a", "a", "b", "b", "b", "b", "b", "b", "b", "b"]]
        
    def main(self):
        gs = lambda: ["s"]
        gr = lambda x: ["P1", "P2"]
        
        tt = TestEMAlgorithm(gm, gs, gr)
    
if __name__ == '__main__':
   unittest.main()
