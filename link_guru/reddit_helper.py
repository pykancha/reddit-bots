"""
A wrapper module on top of praw. This module is same for all projects and copied from root folder and only modified there.
"""

import itertools
import json
import os

import praw
from praw.exceptions import RedditAPIException

from logger_file import Logger


logger = Logger().get_logger()


def login(username):
    # rnepal-bot -> RNEPALBOT | link_guru -> LINK_GURU
    BOT_NAME = username.replace("-", "").upper()
    logger.info("Logging in ...")
    reddit = praw.Reddit(
        client_id=os.getenv(f"{BOT_NAME}_ID"),
        client_secret=os.getenv(f"{BOT_NAME}_SECRET"),
        user_agent=os.getenv(f"{BOT_NAME}_USERAGENT"),
        username=username,
        password=os.getenv(f"{BOT_NAME}_PASS"),
    )
    logger.debug(f"Logged in as {username}. read_only: {reddit.read_only}")
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


def reply(reply_message, element):
    post = element.submission if hasattr(element, "submission") else element
    logger.info(f"replying to {element.id} under submission {post.id}")
    if is_open(post=post):
        return __try_commenting(element, reply_message)
    else:
        logger.error(f"ERROR: Submission {post.id} closed: Archived or Locked.")


def is_open(post=None, comment=None):
    """Check if either a post or comment is open"""
    submission = cmt.submission if not post else post
    submission_closed = submission.locked or submission.archived
    return not submission_closed


def __try_commenting(element, reply_message):
    """ Returns replied Comment object if comment success else None """
    try:
        bot_reply = element.reply(reply_message)
        logger.debug(f"Replied {element.id} {element.author} {reply_message}")
        return bot_reply
    except RedditAPIException:
        logger.exception("LIMIT REACHED: sleeping ")
        return None


def update_replied_ids(file_path, element_id):
    replied_ids = get_replied_ids(file_path)
    replied_ids.append(element_id)
    with file_path.open("w") as wf:
        json.dump(replied_ids, wf)


def get_replied_ids(file_path):
    with file_path.open("r") as rf:
        ids = json.load(rf)
    return ids
