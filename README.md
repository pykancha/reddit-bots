Reddit Bots: Bots deployed on R/NEPAL sub
========================================

These bots are scripts written in [python](https://python.org) programming language.
They use [praw,](http://praw.readthedocs.io) a python library for accessing reddit [API](https://google.com/search?q=What+is+application+programming+interface).

Any kind of contribution: be it suggestions for improving replies, documentation, code imporovement, outlining issues etc are welcomed.
For code changes please file a issue for respective bot outlining what you intend to do.

Every components of code is freely licensed for you to modify and use it however you like.

# Reddit Election Bot 2079

Python bot written with Praw, to update an submission with latest election count results.
The scraping part is now decoupled and is written in Go. This is python client to communicate with reddit.
This bot fetches and filters the data from [API](https://github.com/hemanta212/nepal-election-api).

# [INACTIVE] News TLDR Bot: link_guru
What it does:

1. Scans the subreddit and finds any linked news articles.
2. Gets its summary and translation if its nepali.
3. From the english translation derive its summary using SMMRY API
4. This is then posted as reply to the respective submissions

The bot uses [custom fork](https://github.com/pykancha/newspaper3k_wrapper) of [newspaper/newspaper3k](https://github.com/codelucas/newspaper) python library for news extraction.

Similarly, it uses [googletrans](https://github.com/ssut/py-googletrans) python library for translation of news and [translate](https://github.com/terryyin/translate-python) python module as fallback translator.

The summary is powered by [SMMRY](https://smmry.com).

This bot runs every 15 minutes and scans the top 20 posts of 'hot', 'new' section of subreddit.

You can view [issues](https://github.com/pykancha/reddit-bots/issues?q=is%3Aopen+is%3Aissue+label%3A%22Link+Guru%22) starting with lable Link Guru for issues regarding this bot.

# [INACTIVE] Emoji Bot

The infamous bot that used to reply to any emoji comment from a reddit user with song lyrics

It had emoji dictionary from emoji database and pre written song lyrics for each emotions which it randomly sampled and commented.
