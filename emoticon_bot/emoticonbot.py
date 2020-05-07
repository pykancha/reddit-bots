import datetime
import itertools
import json
import os
import random
import time

import praw
from praw.exceptions import RedditAPIException

from emoticons import emoticons_data
from replies import replies_data

# Reddit time limit for simultaneous comment is 7 minutes
TIME_LIMIT = (7 * 60) + 3


def login():
    print("Logging in...")
    reddit = praw.Reddit(
        client_id=os.getenv("EMUJIBOT_ID"),
        client_secret=os.getenv("EMUJIBOT_SECRET"),
        user_agent=os.getenv("EMUJIBOT_USERAGENT"),
        username="emuji-bot",
        password=os.getenv("EMUJIBOT_PASS"),
    )
    print(f"Logged in. read_only: {reddit.read_only}")
    print(reddit.auth.limits)
    return reddit


def get_replied_data():
    with open("replied_to.json", "r") as rf:
        data = json.load(rf)
    return data


def update_replied_data(element_id):
    data = get_replied_data()
    ids = data["EMUJI_BOT"]
    ids.append(element_id)
    data["EMUJI_BOT"] = ids
    with open("replied_to.json", "w") as wf:
        json.dump(data, wf)


def get_comments_and_submissions(reddit, subreddit="nepal"):
    rnepal = reddit.subreddit(subreddit)
    comments = []
    submissions = []

    hot = rnepal.hot(limit=20)
    controversial = rnepal.controversial(time_filter="day", limit=20)
    scan_list = itertools.chain(hot, controversial)

    for index, submission in enumerate(scan_list):
        print(f"Scanning {index} submission {submission.title} |{submission.id}|")
        surface_comments = submission.comments.list()
        single_comments = [
            cmt
            for cmt in surface_comments
            if type(cmt) is praw.models.reddit.comment.Comment
        ]
        parent_comments = [
            get_children_comments(cmt)
            for cmt in surface_comments
            if type(cmt) is praw.models.reddit.more.MoreComments
        ]
        for comment_group in parent_comments:
            single_comments += comment_group

        comments += single_comments
        submissions.append(submission)

        print(f"Scanned {submission.id}. Got {len(single_comments)} comments.")

    return comments, submissions


def inspect_submissions_and_reply(submissions):
    for submission in submissions:
        print(f"Inspecting submission {submission.id} for emoticons")
        text = submission.title + submission.selftext
        detect_and_reply(text, post=submission)


def inspect_comments_and_reply(comments):
    for cmt in comments:
        print(f"Inspecting comment {cmt.id} for emoticons under {cmt.submission.id}")
        detect_and_reply(cmt.body, cmt=cmt)


def detect_and_reply(text, post=None, cmt=None):
    element = post if post else cmt
    reply_message = ""
    emotions = replies_data.keys()
    for emotion in emotions:
        if detected(emotion, text):
            reply_message = gen_reply_message(element, emotion)
            break
    else:
        return

    reply(reply_message, post=post, cmt=cmt)


def get_children_comments(parent):
    comments = []
    for cmt in parent.comments():
        if type(cmt) is praw.models.reddit.more.MoreComments:
            comments += get_children_comments(cmt)
        elif type(cmt) is praw.models.reddit.comment.Comment:
            comments.append(cmt)
        else:
            print(f"Unrecognized comment type {type(cmt)}")
    return comments


def reply(reply_message, cmt=None, post=None):
    submission = cmt.submission if not post else post
    submission_closed = submission.locked or submission.archived
    # Since both comment and element will have property author and reply
    # We will refer them both as element
    element = cmt if cmt else submission
    print(f"replying to {element.id} under submission {submission.id}")
    replied_ids = get_replied_data()["EMUJI_BOT"]

    if not submission_closed and element.id not in replied_ids:
        print("Submission open commenting...")
        try_commenting(element, reply_message)
    else:
        print(f"Submission {submission.id} closed: Archived or Locked. Cannot comment ")


def try_commenting(element, reply_message):
    try:
        element.reply(reply_message)
        print(f"Replied {element.author} {reply_message}")
        update_replied_data(element.id)
    except RedditAPIException as e:
        print(f"LIMIT REACHED: {e} sleeping ")
        time.sleep(TIME_LIMIT)
        try_commenting(reply_message)


def gen_reply_message(element, emotion):
    replies = replies_data[emotion]
    random.shuffle(replies)
    core_reply = random.choice(replies)
    author = f"u/{element.author}" if element.author else ""
    full_message = core_reply.format(author=author)
    print(f"Generated reply message {full_message}")
    return full_message


def detected(emotion, text):
    emoticons = emoticons_data[emotion]
    for emoticon in emoticons:
        if emoticon in text:
            print(f"detected {emotion} {emoticon}")
            return True
    print(f"No {emotion} emotion Detected")
    return False


def load_emoticons_from_db():
    with open("emojidb.json", "r") as rf:
        data = json.load(rf)
    emojis = data["all_emojis"]
    return emojis


if __name__ == "__main__":
    reddit = login()
    comments, submissions = get_comments_and_submissions(reddit, subreddit="nepal")
    print(f"Scanned {len(submissions)} submissions and {len(comments)} comments")
    inspect_comments_and_reply(comments)
    inspect_submissions_and_reply(submissions)
