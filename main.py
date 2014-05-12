import words
import utils
import sys
import em
import getngram


def insert_by_sender(location, sender, agent):
    """Specify relative path or absolute path for location."""

    keywords = [sender, "sent"]
    filenames = utils.walkdir(location, keywords)
    emails = utils.email_to_tuple(filenames)
    #agent = words.EmailAgent("maintest.db")
    agent.insert_email(emails)
    # print emails

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "First argument is directory, second is the sender you want to filter by."
        # python main.py emails/solberg-g/ solberg-g
    elif len(sys.argv) > 3:
        print "Ask Nicole for help."

    agent = words.EmailAgent("maintest.db", True)
    insert_by_sender(sys.argv[1], sys.argv[2], agent)

    # print getngram.reqNgram("Princeton *, lol")

    ema = em.TestEMAlgorithm(
        agent.getMsg, agent.getSenders, agent.getReceiver, ())
    
    # print getngram.reqNgram(ema.getGoogleRequests()[: 50])
    rt = []
    rtb = []
    for rec in ema.nameList:
        rt.append(ema.test(rec))
        rtb.append(ema.test_baseline(rec))


    print ""
    print "Testing finished."
        
    print rt
    print rtb

    
