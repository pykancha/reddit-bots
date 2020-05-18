import datetime
import json
import os
import random
import time

import praw
from praw.exceptions import RedditAPIException

# Reddit time limit for simultaneous comment is 7 minutes
TIME_LIMIT = (7 * 60) + 3


def login():
    print("Logging in...")
    username = "rnepal-bot"
    reddit = praw.Reddit(
        client_id=os.getenv("RNEPALBOT_ID"),
        client_secret=os.getenv("RNEPALBOT_SECRET"),
        user_agent=os.getenv("RNEPALBOT_USERAGENT"),
        username=username,
        password=os.getenv("RNEPALBOT_PASS"),
    )
    print(f"Logged in as {username}. read_only: {reddit.read_only}")
    print(reddit.auth.limits)
    return reddit


def get_past_data():
    with open("past_links.json", "r") as rf:
        data = json.load(rf)
    return data


def update_past_data(milestone, info):
    data = get_past_data()
    key = milestone + "k"
    data[key] = info
    with open("past_links.json", "w") as wf:
        json.dump(data, wf)


def get_milestone():
    prev_data = get_past_data()
    past_milestones = prev_data.keys()
    # changes 21k 20k to 21 and 20 and find max of it
    recent_milestone = max([int(i.replace("k", "")) for i in past_milestones])
    # changes 21 to 22 and makes it 22000
    next_milestone = str((recent_milestone + 1)) + "k"  # * 1000
    return past_milestones, recent_milestone, next_milestone


def get_date(stamp):
    date = datetime.datetime.fromtimestamp(stamp)
    return date.strftime("%d %B, %Y")


def get_timestamp(date):
    date = datetime.to(stamp)
    return date.strftime("%d %B, %Y")


def fill_milestone_data(submission):
    new_dict = {}
    new_dict["title"] = submission.title
    new_dict["author"] = "deleted" if not submission.author else submission.author.name
    new_dict["date"] = get_date(submission.created)
    new_dict["stamp"] = submission.created
    new_dict["link"] = submission.url
    return new_dict


def post(post_message, rnepal):
    # Since both comment and element will have property author and reply
    # We will refer them both as element
    element = cmt if cmt else submission
    print(f"replying to {element.id} under submission {submission.id}")
    replied_ids = get_replied_data()["RNEPAL_BOT"]

    if not submission_closed and element.id not in replied_ids:
        print("Submission open commenting...")
        try_commenting(element, reply_message)
    else:
        print(f"Submission {submission.id} closed: Archived or Locked. Cannot comment ")


def try_posting(element, reply_message):
    try:
        element.reply(reply_message)
        print(f"Replied {element.author} {reply_message}")
        update_replied_data(element.id)
    except RedditAPIException as e:
        print(f"LIMIT REACHED: {e} sleeping ")
        time.sleep(TIME_LIMIT)
        try_commenting(reply_message)


def gen_reply_message(element, emotion):
    pass


def detected(emotion, text):
    emoticons = emoticons_data[emotion]
    for emoticon in emoticons:
        if emoticon in text:
            print(f"detected {emotion} {emoticon}")
            return True
    print(f"No {emotion} emotion Detected")
    return False


if __name__ == "__main__":
    reddit = login()
    comments, submissions = get_comments_and_submissions(reddit, subreddit="nepal")
    print(f"Scanned {len(submissions)} submissions and {len(comments)} comments")
    inspect_comments_and_reply(comments)
    inspect_submissions_and_reply(submissions)
