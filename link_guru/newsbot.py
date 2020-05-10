import json
import re
import time
from pathlib import Path

from bs4 import BeautifulSoup as BS

from news import get_full_news, get_news, get_summary
from custom_scrapers import custom_scrapers_map
from reddit_helper import (get_replied_ids, get_submissions, is_open, login,
                           reply, update_replied_ids, __cut_text)
from templates.footer import footer_string
from templates.news import NewsTemplate


SITES_FILE_PATH = Path("supported_sites.json")
REPLIED_FILE_PATH = Path("replied_to.json")


def main():
    USERNAME = "link_guru"
    reddit = login(USERNAME)

    replied_ids = get_replied_ids(REPLIED_FILE_PATH)
    manage_mentions(reddit, replied_ids)

    submissions = get_submissions_with_supported_link(reddit)
    unreplied_submissions = [sub for sub in submissions if sub.id not in replied_ids]
    print(f"Got {len(unreplied_submissions)} unreplied submissions")
    open_unreplied_submissions = {
        sub for sub in unreplied_submissions if is_open(post=sub)
    }
    print(f"Got {len(open_unreplied_submissions)} valid submissions")
    for submission in open_unreplied_submissions:
        news = get_news_with_translation(submission.url, submission.domain)
        if not news:
            continue
        reply_and_update_ids(reddit, news, submission)


def reply_and_update_ids(reddit, news, element):
    main_reply, child_reply = gen_reply_message(news)

    # TESTING ONLY IS PURPOSES. SOONER IF POSSIBLE REMOVE
    test_submission = reddit.submission(id='gezfqs')
    replied_cmt = reply(main_reply, test_submission)
    #replied_cmt = reply(main_reply, element)
    # ----------------------------

    if replied_cmt:
        update_replied_ids(REPLIED_FILE_PATH, element.id)
    if child_reply:
        reply(child_reply, replied_cmt)


def get_submissions_with_supported_link(reddit):
    """
    Get submission on certain categories. 
    Get the domain of that submission and matches against regular expressions
    of sites we have in supported_sites.json file
    """
    categories = ["hot", "new"]
    submissions = get_submissions(reddit, categories=categories, subreddit="nepal")
    matched_submissions = []
    for sub in submissions:
        flair = sub.link_flair_text
        if matched_link(sub.domain):
            matched_submissions.append(sub)
            continue
        elif 'News' in flair and not 'reddit' in sub.url:
            matched_submissions.append(sub)
             
    print(f"{[(sub.id, sub.domain, sub.author) for sub in matched_submissions]}")
    return matched_submissions


def get_news_with_translation(url, domain):
    url = url
    print(f"Got url {url}")
    scraper = map_to_scraper(domain)
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


def matched_link(url, make_pattern=None):
    with SITES_FILE_PATH.open("r") as rf:
        sites = json.load(rf)
    # Make site name regex safe
    sites = [site.replace(".", "\.") for site in sites]
    if not make_pattern:
        make_pattern = lambda site: r"(www\.)?{site}".format(site=site)
    patterns = [make_pattern(site) for site in sites]
    print(f"Generated patterns \n{patterns}")
    print(f"Matching regex {url}")

    match = None
    for pattern in patterns:
        match = re.search(pattern, url)
        if match and match.group():
            print(f"Matched {url}")
            break;

    return match


def gen_reply_message(news):
    main_reply = NewsTemplate.heading_string
    child_reply = None
    first_reply = news['summary']
    translated_summary = news["full_news_en"]
    if not translated_summary:
        translated_summary = news['summary_en']

    if translated_summary and translated_summary.strip():
        main_reply += NewsTemplate.translation_string
        child_reply = translated_summary.replace("** ", "**").replace(" **", "**")

    main_reply += f"{first_reply}{footer_string}"
    return main_reply, child_reply


def map_to_scraper(domain):
    if domain in custom_scrapers_map:
        return custom_scrapers_map[domain]
    else:
        return get_news


def scan_for_matched_links(element):
    html = element.body_html
    links_with_domain = extract_links_from_html(html)
    if links_with_domain:
        return links_with_domain

    parent = element.parent()
    if hasattr(parent, 'title'):
        new_html = parent.selftext_html + f' <a href="{parent.url}"></a>'
        print(f"submission detected \n{new_html}")
    else:
        new_html = parent.body_html
    links_with_domain = extract_links_from_html(new_html)

    return links_with_domain


def manage_mentions(reddit, replied_ids):
    mentions = reddit.inbox.mentions()
    unreplied_mentions = (
        mention for mention in mentions if mention.id not in replied_ids
    )
    for index, element in enumerate(unreplied_mentions):
        # If mentioned in post try translate without checking site support
        if hasattr('element', 'title') and not 'reddit' in element.url:
            news = get_news_with_translation(link, domain)
            if news:
                reply_and_update_ids(news, element)

        # If not check for selftext and comment links and only translate 
        # Supported sites.
        links_with_domain = scan_for_matched_links(element)
        print(f"scanning {index} mention. Got links \n{links_with_domain}")
        for link_domain in links_with_domain:
            link, domain = link_domain
            news = get_news_with_translation(link, domain)
            if not news:
                continue
<<<<<<< HEAD
            reply_and_update_ids(reddit, news, element)
=======
            reply_and_update_ids(news, element)
>>>>>>> c48cc9c... Adds mentioning capability


def extract_links_from_html(html):
    soup = BS(html, features='lxml')
    links = [a['href'] for a in soup.find_all('a')]
    print(f"Got links from html \n{links}")

    pattern_str = r"(http|https)?(://)?(www\.)?({site})/(.)*\b"
    pattern_maker = lambda site: pattern_str.format(site=site)
    links_with_domain = []

    for link in links:
        match = matched_link(link, make_pattern=pattern_maker)
        if match and match.group(4):
            links_with_domain.append( (link, match.group(4)) )

    print(f"Extracted from html \n{links_with_domain}")
    return links_with_domain


if __name__ == "__main__":
    main()
