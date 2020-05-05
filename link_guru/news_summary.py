import datetime
import os
import time

import praw
from praw.exceptions import RedditAPIException

from googletrans import Translator
from vendored.news_extractor.newspaper import Article

# Reddit time limit for simultaneous comment is 7 minutes
TIME_LIMIT = (7 * 60) + 3


def login():
    print("Logging in...")
    reddit = praw.Reddit(
        client_id=os.getenv("LINK_GURUBOT_ID"),
        client_secret=os.getenv("LINK_GURUBOT_SECRET"),
        user_agent=os.getenv("LINK_GURUBOT_USERAGENT"),
        username="link_guru",
        password=os.getenv("LINK_GURUBOT_PASS"),
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
    ids = data["LINK_GURU_BOT"]
    ids.append(element_id)
    data["LINK_GURU_BOT"] = ids
    with open("replied_to.json", "w") as wf:
        json.dump(data, wf)


def get_news(url):
    article = Article(url, language="hi")
    article.download()
    article.parse()
    article.nlp()
    data = {
        "date": article.publish_date,
        "title": article.title,
        "keywords": article.keywords,
        "summary": article.summary,
        "text": article.text,
        "img_url": article.top_image,
        "video": article.movies,
        "url": url,
    }
    return data


def cut_text(text, length):
    cuts = []

    def rec_cut(text, length):
        text_length = len(text)
        if length >= text_length:
            cuts.append(text)
            return
        else:
            snippet = text[:length]
            last_purnabiram = snippet.rfind("।") + 1
            last_fullstop = snippet.rfind(".") + 1
            # rfind returns -1 on failure (-1 + 1) == 0
            if last_purnabiram == 0 and last_fullstop == 0:
                raise ValueError("No purnabiram or fullstop found in given length")
            punctuation = last_fullstop if last_fullstop else last_purnabiram
            valid_paragraph = snippet[:punctuation]
            cuts.append(valid_paragraph)
            rec_cut(text[last_purnabiram:], length)

    rec_cut(text, length)
    return cuts


def translate(cuts):
    translator = Translator()
    translation = ""
    for paragraph in cuts:
        translated = translator.translate(paragraph, src="ne")
        translation += translated.text
    return translation


def get_summary(news_text):
    summary = cut_text(news_text, 1000)[0]
    summary_en = translate([summary])
    return summary, summary_en


def get_submissions(reddit, subreddit="nepal"):
    rnepal = reddit.subreddit(subreddit)
    comments = []
    submissions = []

    for index, submission in enumerate(rnepal.hot(limit=20)):
        submissions.append(submission)

        print(f"Scanned {submission.id}. Got {len(single_comments)} comments.")

    return submissions


def inspect_submissions_and_reply(submissions):
    for submission in submissions:
        print(f"Inspecting submission {submission.id} for emoticons")
        text = submission.title + submission.selftext


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
    replied_ids = get_replied_data()["LINK_GURU_BOT"]

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
        try_commenting(element, reply_message)


if __name__ == "__main__":
    reddit = login()
    submissions = get_submissions(reddit, subreddit="nepal")
    print(f"Scanned {len(submissions)} submissions ")
    inspect_submissions_and_reply(submissions)
