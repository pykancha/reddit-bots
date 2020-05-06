"""
A wrapper module on top of praw. This module is same for all projects and copied from root folder and only modified there.
"""

import itertools
import json
import os

import praw
from praw.exceptions import RedditAPIException


def login(username):
    # rnepal-bot -> RNEPALBOT | link_guru -> LINK_GURU
    BOT_NAME = username.replace("-", "").upper()
    print("Logging in ...")
    reddit = praw.Reddit(
        client_id=os.getenv(f"{BOT_NAME}_ID"),
        client_secret=os.getenv(f"{BOT_NAME}_SECRET"),
        user_agent=os.getenv(f"{BOT_NAME}_USERAGENT"),
        username=username,
        password=os.getenv(f"{BOT_NAME}_PASS"),
    )
    print(f"Logged in as {username}. read_only: {reddit.read_only}")
    return reddit


def get_submissions(reddit, categories=None, limit=20, subreddit="nepal"):
    subreddit = reddit.subreddit(subreddit)
    submissions = []
    categories = ["hot"] if not categories else categories

    category_map = {
        "hot": subreddit.hot(limit=limit),
        "new": subreddit.new(limit=limit),
        "top": subreddit.top("day", limit=limit),
        "controversial": subreddit.controversial("day", limit=limit),
    }
    categories_gen = [category_map[i] for i in categories if i in category_map.keys()]
    scanlist = itertools.chain(*categories_gen)

    return scanlist


def get_submission_comments(submission):
    submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()
    return all_comments


def reply(reply_message, cmt=None, post=None):
    submission = cmt.submission if not post else post
    # Since both comment and element will have property author and reply
    # We will refer them both as element
    element = cmt if cmt else submission
    print(f"replying to {element.id} under submission {submission.id}")

    if is_open(element):
        print("Submission open commenting...")
        return __try_commenting(element, reply_message)
    else:
        print(f"ERROR: Submission {submission.id} closed: Archived or Locked. Cannot comment ")


def is_open(post=None, comment=None):
    """Check if either a post or comment is open"""
    submission = cmt.submission if not post else post
    submission_closed = submission.locked or submission.archived
    return not submission_closed


def __try_commenting(element, reply_message):
    # If reddit time limits us  wait for 7 mins and try again
    TIME_LIMIT = 7 * 61  # seconds
    try:
        bot_reply = element.reply(reply_message)
        print(f"Replied {element.id} {element.author} {reply_message}")
        return bot_reply
    except RedditAPIException as e:
        print(f"LIMIT REACHED: {e} sleeping ")
        time.sleep(TIME_LIMIT)
        __try_commenting(element, reply_message)


def update_replied_ids(file_path, element_id):
    replied_ids = get_replied_ids(file_path)
    replied_ids.append(element_id)
    with file_path.open("w") as wf:
        json.dump(replied_ids, wf)


def get_replied_ids(file_path):
    with file_path.open("r") as rf:
        ids = json.load(rf)
    return ids
