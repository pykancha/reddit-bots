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
from templates.footer import footer_string


def main():
    USERNAME = "emuji-bot"
    reddit = login(USERNAME)
    REPLIED_FILE_PATH = Path("replied_to.json")

    replied_ids = get_replied_ids(REPLIED_FILE_PATH)
    submissions, comments = get_open_submissions_and_comments(reddit)
    unreplied_submissions = [sub for sub in submissions if sub.id not in replied_ids]
    unreplied_comments = [cmt for cmt in comments if cmt.id not in replied_ids]
    print(f"Got {len(unreplied_submissions)} valid submissions"
          f"Got {len(unreplied_comments)} valid comments")

    for comment in unreplied_comments:
        text = comment.body
        emotion = detect_emotion(text)
        if not emotion:
            continue
        
        reply_message = gen_reply_message(comment, emotion)

        # TESTING ONLY IS PURPOSES. SOONER IF POSSIBLE REMOVE
        test_comment = reddit.comment('fpuxbz9')
        replied_cmt = reply(reply_message, cmt=test_comment)
        # replied_cmt = reply(reply_message, cmt=comment)
        # ----------------------------

        if replied_cmt:
            update_replied_ids(REPLIED_FILE_PATH, comment.id)

    for submission in unreplied_submissions:
        text = submission.title + submission.selftext
        emotion = detect_emotion(text)
        if not emotion:
            continue

        reply_message = gen_reply_message(submission, emotion)

        # TESTING ONLY IS PURPOSES. SOONER IF POSSIBLE REMOVE
        test_submission = reddit.submission(id="gfpcqg")
        replied_cmt = reply(reply_message, post=test_submission)
        # replied_cmt = reply(reply_message, post=submission)
        # ----------------------------

        if replied_cmt:
            update_replied_ids(REPLIED_FILE_PATH, submission.id)


def get_open_submissions_and_comments(reddit):
    categories = ["hot", "new"]
    comments = []
    submissions = get_submissions(reddit, categories=categories, subreddit="nepal")
    [
        comments.extend(get_submission_comments(sub)) for sub in submissions
    ]
    open_submissions = {
        sub for sub in submissions if is_open(post=sub)
    }
    open_comments = {
        cmt for cmt in comments if is_open(comment=cmt)
    }
    print(f"Got {len(open_comments)} comments & {len(open_submissions)} posts")
    
    return open_submissions, open_comments


def detect_emotion(text):
    reply_message = ""
    emotions = replies_data.keys()
    for emotion in emotions:
        if detected(emotion, text):
            return emotion

    return None


def detected(emotion, text):
    emoticons = emoticons_data[emotion]
    for emoticon in emoticons:
        if emoticon in text:
            print(f"detected {emotion} {emoticon}")
            return True
    print(f"No {emotion} emotion Detected")
    return False


def gen_reply_message(element, emotion):
    replies = replies_data[emotion]
    random.shuffle(replies)
    core_reply = random.choice(replies)

    # TESTING PURPOSES ONLY
    text = element.body if hasattr(element, 'body') else (element.title +
                                                          element.selftext)
    author = f"{element.author}" if element.author else ""
    #author = f"u/{element.author}" if element.author else ""
    full_message = f">{author} \n\n > {text} \n\n"
    full_message += core_reply.format(author=author)
    #full_message = core_reply.format(author=author)
    # --------------------------------------

    full_message += f"\n\n {footer_string}"
    print(f"Generated reply message {full_message}")
    return full_message


if __name__ == "__main__":
    main()
