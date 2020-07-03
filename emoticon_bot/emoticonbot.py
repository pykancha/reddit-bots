import datetime
import random
import json
import time
from pathlib import Path

from emoticons import emoticons_data
from replies import replies_data
from reddit_helper import (
    get_replied_ids,
    get_submissions,
    is_open,
    login,
    reply,
    update_replied_ids,
    get_submission_comments,
)
from logger_file import Logger, prettify


USERNAME = "emuji-bot"
REPLIED_FILE_PATH = Path("replied_to.json")
logger = Logger(name="emoticonbot").get_logger()


def main():
    reddit = login(USERNAME)
    submissions, comments = get_unreplied_open_submissions_and_comments(reddit)
    for comment in comments:
        text = comment.body
        logger.debug(f"Got comment text:{prettify(text)}")
        emotion = detect_emotion(text)
        anti = detect_anti(comment)
        if not emotion and not anti:
            continue

        reply_message = gen_reply_message(comment, emotion, anti=anti)
        replied_cmt = reply(reply_message, comment)
        if replied_cmt:
            update_replied_ids(REPLIED_FILE_PATH, comment.id)

    for submission in submissions:
        text = submission.title + submission.selftext
        logger.debug(f"Got submission text:{prettify(text)}")
        emotion = detect_emotion(text)
        if not emotion:
            continue

        reply_message = gen_reply_message(submission, emotion)
        replied_cmt = reply(reply_message, submission)
        if replied_cmt:
            update_replied_ids(REPLIED_FILE_PATH, submission.id)


def get_unreplied_open_submissions_and_comments(reddit):
    categories = ["hot", "new"]
    comments = []
    replied_ids = get_replied_ids(REPLIED_FILE_PATH)
    submissions = get_submissions(reddit, categories=categories, subreddit="nepal")
    [comments.extend(get_submission_comments(sub)) for sub in submissions]

    open_submissions = {sub for sub in submissions if is_open(post=sub)}
    open_comments = {cmt for cmt in comments if is_open(comment=cmt)}
    unreplied_submissions = (sub for sub in open_submissions if sub.id not in replied_ids)
    unreplied_comments = (cmt for cmt in open_comments if cmt.id not in replied_ids)

    return unreplied_submissions, unreplied_comments


def detect_anti(comment):
    if not comment.author in ['anti_emuji-bot', 'anti-emuji-bot']:
        return False

    replied_to_me = comment.parent() and comment.parent().author == 'emuji-bot'
    if replied_to_me and not comment.parent().body in replies_data['anti']:
        return True

    return False


def detect_emotion(text):
    reply_message = ""
    emotions = emoticons_data.keys()
    for emotion in emotions:
        if detected(emotion, text):
            return emotion

    return None


def detected(emotion, text):
    emoticons = emoticons_data[emotion]
    for emoticon in emoticons:
        if emoticon in text:
            logger.info(f"detected {emotion} {emoticon}")
            return True
    logger.info(f"No {emotion} emotion Detected")
    return False


def gen_reply_message(element, emotion, anti=False):
    replies = replies_data[emotion]
    if anti:
        replies = replies_data["anti"]
    random.shuffle(replies)
    core_reply = random.choice(replies)

    author = f"u/{element.author}" if element.author else ""
    full_message = core_reply.format(author=author)
    logger.debug(f"Generated reply message: {prettify(full_message)}")
    return full_message


if __name__ == "__main__":
    main()
