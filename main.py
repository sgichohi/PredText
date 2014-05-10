import words
import utils
import sys


def insert_by_sender(location, sender):
	"""Specify relative path or absolute path for location."""

	filenames = utils.walkdir(location, sender)
	emails = utils.email_to_tuple(filenames)
	agent = words.EmailAgent("test.db")
	agent.insert_email(emails)

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "First argument is directory, second is the sender you want to filter by."
	elif len(sys.argv) > 3:
		print "Ask Nicole for help."
	insert_by_sender(sys.argv[1], sys.argv[2])
