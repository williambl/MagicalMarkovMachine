import markovify
import praw
import sys
import argparse
from progress.bar import Bar


# Reddit instance and UserAgent
UA = "Markov"
r = praw.Reddit(UA)
inputType = ""
inReddit = None
inUser = None
inPath = None
count = 0

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
args = parser.parse_args()

count = int(args.count)
if (args.subreddit != "None"):
    inputType = "subreddit"
    inReddit = args.subreddit
    print(inReddit)
elif (args.reddit_user != "None"):
    inputType = "user"
    inUser = args.reddit_user
    print(inUser)
elif (args.file != "None"):
    inputType = "file"
    inPath = args.file
    print(inPath)
else:
    inputType = input("Subreddit, reddit user or file? ")


# Methods to get markov material
def textFromSubreddit(subredditIn):
    bar = Bar("Fetching comments from /r/" + subredditIn + "...", max=1000)
    try:
        subreddit = r.get_subreddit(subredditIn)
        comments = subreddit.get_comments(limit=1000)
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


def textFromUser(userIn):
    try:
        redditor = r.get_redditor(userIn)
        bar = Bar("Fetching /u/" + userIn + "'s comments...", max=1000)
        comments = redditor.get_comments(limit=1000)
        text = ""
        for comment in comments:
            text += comment.body + "\n"
            bar.next()
        bar.finish()
    except praw.errors.NotFound:
        print("User not found. Please try again.")
    return(text)


if (inputType == "subreddit"
        or inputType == "s" or inputType == "r" or inputType == "reddit"
        or inputType == "sub"):
    if (inReddit is None):
        inReddit = input("Subreddit: ")
    text = textFromSubreddit(inReddit)

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
    text = textFromUser(inUser)

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
