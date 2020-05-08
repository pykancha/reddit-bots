import json
import re
import time
from pathlib import Path

from news import get_full_news, get_news, get_summary
from custom_scrapers import custom_scrapers_map
from reddit_helper import (get_replied_ids, get_submissions, is_open, login,
                           reply, update_replied_ids)
from templates.footer import footer_string
from templates.news import NewsTemplate


def main():
    USERNAME = "link_guru"
    reddit = login(USERNAME)
    REPLIED_FILE_PATH = Path("test_replied_to.json")

    replied_ids = get_replied_ids(REPLIED_FILE_PATH)
    submissions = get_submissions_with_supported_link(reddit)
    unreplied_submissions = [sub for sub in submissions if sub.id not in replied_ids]
    print(f"Got {len(unreplied_submissions)} unreplied submissions")
    open_unreplied_submissions = {
        sub for sub in unreplied_submissions if is_open(post=sub)
    }
    print(f"Got {len(open_unreplied_submissions)} valid submissions")
    for submission in open_unreplied_submissions:
        news = get_news_with_translation(submission)
        if not news:
            continue

        main_reply, child_reply = gen_reply_message(news)
        replied_cmt = reply(main_reply, post=submission)

        if replied_cmt:
            update_replied_ids(REPLIED_FILE_PATH, submission.id)
        if child_reply:
            time.sleep(5)
            reply(child_reply, cmt=replied_cmt)


def get_submissions_with_supported_link(reddit):
    """
    Get submission on certain categories. 
    Get the domain of that submission and matches against regular expressions
    of sites we have in supported_sites.json file
    """

    SITES_FILE_PATH = Path("supported_sites.json")

    categories = ["hot", "new"]
    submissions = get_submissions(reddit, categories=categories, subreddit="nepal")

    with SITES_FILE_PATH.open("r") as rf:
        sites = json.load(rf)

    # Make site name regex safe
    sites = [site.replace(".", "\.") for site in sites]
    make_pattern = lambda site: r"(www\.)?{site}".format(site=site)
    patterns = [make_pattern(site) for site in sites]
    print(f"Generated patterns \n{patterns}")

    matched_submissions = [
        sub for sub in submissions if matched_link(sub.domain, patterns)
    ]
    print(f"{[(sub.id, sub.domain, sub.author) for sub in matched_submissions]}")
    return matched_submissions


def get_news_with_translation(submission):
    url = submission.url
    print(f"Got url {url}")
    scraper = map_to_scraper(submission.domain)
    data = scraper(url)
    if not data:
        return None

    title = data["title"].strip()
    text = data["text"]
    short_text = data["summary"]
    if not text or len(text) < len(short_text):
        text = data["summary"]

    full_translation = None
    if title and (text and len(text) > 400):
        full_news, full_news_en = get_full_news(title, text)
        # Since we avoid mymemory translation on full_news it might be empty or wrong
        if full_news_en.strip() and len(full_news_en) > len(full_news) / 2:
            full_translation = full_news_en
        summary, summary_en = get_summary(full_news, full_news_en=full_translation)
    else:
        print(f"Warning: Discarding data {title} \n{text}")
        return None

    news = {
        "summary": summary,
        "summary_en": summary_en,
        "full_news": full_news,
        "full_news_en": full_news_en,
    }
    return news


def matched_link(url, patterns):
    matched = False
    print(f"Matching regex {url}")

    for pattern in patterns:
        match = re.search(pattern, url)
        if match and match.group() == url:
            matched = True
            print(f"Matched {url}")
            break

    return matched


def gen_reply_message(news):
    main_reply = NewsTemplate.heading_string
    child_reply = None
    summary = news["summary"]
    translated_summary = news["summary_en"]
    if translated_summary and translated_summary.strip():
        main_reply += NewsTemplate.translation_string
        child_reply = translated_summary.replace("** ", "**").replace(" **", "**")

    main_reply += f"{summary}{footer_string}"
    return main_reply, child_reply


def map_to_scraper(domain):
    if domain in custom_scrapers_map:
        return custom_scrapers_map[domain]
    else:
        return get_news


if __name__ == "__main__":
    main()
