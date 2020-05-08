Reddit Bots: Bots deployed on R/NEPAL sub
========================================

These bots are just scripts written in [python](https://python.org) programming language.
They use [praw,](http://praw.readthedocs.io) a python library for accessing reddit [API](https://google.com/search?q=What+is+application+programming+interface).

Any kind of contribution: be it suggestions for improving replies, documentation, code imporovement, outlining issues etc are welcomed. 
For code changes please file a issue for respective bot outlining what you intend to do.

Every components of code is freely licensed for you to modify and use it however you like. 

I manage the hosting/running of the bot separately and the database of replied posts/comments is maintained separately. If you need any kind of help in figuring this part I will be glad to assist you.

# Link Guru Bot:
What it does:

1. Scans the subreddit and finds any linked news articles.
2. Gets its summary and translation if its nepali.
3. This is then posted as reply to the respective submissions

The bot uses [custom fork](https://github.com/pykancha/newspaper3k_wrapper) of [newspaper/newspaper3k](https://github.com/codelucas/newspaper) python library for news extraction. 

Similarly, it uses [googletrans](https://github.com/ssut/py-googletrans) python library for translation of news and [translate](https://github.com/terryyin/translate-python) python module as fallback translator.

This bot runs every 15 minutes and scans the top 20 posts of 'hot', 'new' section of subreddit.

You can view [issues](https://github.com/pykancha/reddit-bots/issues?q=is%3Aopen+is%3Aissue+label%3A%22Link+Guru%22) starting with lable Link Guru for issues regarding this bot.
