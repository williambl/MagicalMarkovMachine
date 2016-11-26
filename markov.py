import markovify
import praw
import sys
import argparse
from progress.bar import Bar
import signal

# Reddit instance and UserAgent
UA = "William's MagicalMarkovMachine"
r = praw.Reddit(UA)
inputType = ""
inReddit = None
inUser = None
inPath = None
count = 0
comment_count = 0


# ctrl-C handling
def handler(signum, frame):
    print("\nCaught ^C, exiting...")
    sys.exit()


signal.signal(signal.SIGINT, handler)

# Command line arguments
parser = argparse.ArgumentParser(
    description="William Bradford Larcombe's Magical Markov Machine")

parser.add_argument(
        "-r", "--subreddit",
        help="uses a subreddit as material for the markov chain",
        metavar="SUBREDDIT", default="None")
parser.add_argument(
        "-u", "--reddit_user",
        help="uses a reddit user as material for the markov chain",
        metavar="USER", default="None")
parser.add_argument(
        "-f", "--file",
        help="uses a text file as material for the markov chain",
        metavar="PATH", default="None")
parser.add_argument(
        "-c", "--count",
        help="how many sentences to be generated",
        metavar="COUNT", default=0)
parser.add_argument(
        "-C", "--Comment_count",
        help="how many comments to be taken from reddit",
        metavar="COMMENTCOUNT", default=0)
args = parser.parse_args()

count = int(args.count)
if (args.subreddit != "None"):
    inputType = "subreddit"
    inReddit = args.subreddit
elif (args.reddit_user != "None"):
    inputType = "user"
    inUser = args.reddit_user
elif (args.file != "None"):
    inputType = "file"
    inPath = args.file
else:
    inputType = input("Subreddit, reddit user or file? ")
comment_count = int(args.Comment_count)


# Methods to get markov material
def textFromSubreddit(subredditIn, commentcount):
    bar = Bar("Fetching comments from /r/" + subredditIn + "...", max=commentcount)
    try:
        subreddit = r.get_subreddit(subredditIn)
        comments = subreddit.get_comments(limit=commentcount)
        text = ""
        for comment in comments:
            text += comment.body + "\n"
            bar.next()
        bar.finish()
    except praw.errors.InvalidSubreddit:
        print("Subreddit not found. Please try again.")
        sys.exit()
    return(text)


def textFromFile(fileIn):
    # Get raw text as string.
    try:
        with open(fileIn) as f:
            print("Reading file...")
            text = f.read()
    except FileNotFoundError:
        print("File not found. Please try again.")
        sys.exit()
    return(text)


def textFromUser(userIn, commentcount):
    try:
        redditor = r.get_redditor(userIn)
        bar = Bar("Fetching /u/" + userIn + "'s comments...", max=commentcount)
        comments = redditor.get_comments(limit=commentcount)
        text = ""
        for comment in comments:
            text += comment.body + "\n"
            bar.next()
        bar.finish()
    except praw.errors.NotFound:
        print("User not found. Please try again.")
    return(text)


if (inputType == "subreddit"
        or inputType == "s" or inputType == "r"
        or inputType == "reddit" or inputType == "sub"):
    if (inReddit is None):
        inReddit = input("Subreddit: ")
    if (comment_count == 0):
        comment_count = int(input("Comment count: "))
    text = textFromSubreddit(inReddit, comment_count)

elif (inputType == "file" or inputType == "f"
        or inputType == "path" or inputType == "txt"):
    if (inPath is None):
        inPath = input("Path to file: ")
    text = textFromFile(inPath)

elif (inputType == "user" or inputType == "u"
        or inputType == "reddituser" or inputType == "redditor"
        or inputType == "reddit user"):
    if (inUser is None):
        inUser = input("User: ")
    if (comment_count == 0):
        comment_count = int(input("Comment count: "))
    text = textFromUser(inUser, comment_count)

else:
    print("Please type subreddit, reddit user or file.")
    sys.exit()

if (count == 0):
    count = int(input("Sentence count: "))

print(text)
print("\n" + "-" * 80 + "\n")

# Build the model.
text_model = markovify.Text(text)

# Print five randomly-generated sentences
for i in range(count):
    print(text_model.make_sentence())
