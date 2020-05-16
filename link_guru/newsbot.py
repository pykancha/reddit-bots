import time
import json
import re
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup as BS

from news import get_full_news, get_news, get_summary, translate, summarize_to_tldr
from custom_scrapers import custom_scrapers_map
from reddit_helper import (
    get_replied_ids,
    get_submissions,
    is_open,
    login,
    reply,
    update_replied_ids,
)
from templates.news import NewsTemplate


USERNAME = "news-tldr"
SITES_FILE_PATH = Path("supported_sites.json")
REPLIED_FILE_PATH = Path("replied_to.json")


def main():
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
        if news:
            reply_and_update_ids(news, submission)


def reply_and_update_ids(news, element):
    main_reply, child_reply = gen_reply_message(news)
    replied_cmt = reply(main_reply, element)

    if replied_cmt:
        update_replied_ids(REPLIED_FILE_PATH, element.id)
        if child_reply:
            time.sleep(10)
            reply(child_reply, replied_cmt)

    return replied_cmt


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
        elif flair and "News" in flair and __is_valid_link(sub.url):
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
    title_en = ""
    text = data["text"]
    short_text = data["summary"]
    if not text or len(text) < len(short_text):
        text = data["summary"]

    if title:
        title_en = translate(title)

    full_translation = None
    if text and len(text) > 400:
        full_news, full_news_en = get_full_news(text)
        # Since we avoid mymemory translation on full_news, it might be empty or wrong
        if full_news_en.strip() and len(full_news_en) > len(full_news) / 2:
            full_translation = full_news_en
        summary, summary_en = get_summary(full_news, full_news_en=full_translation)
    else:
        print(f"Warning: Discarding data text {title} \n{text}")
        return None

    tldr = ""
    if summary_en.strip() or full_news_en.strip():
        tldr = (
            summarize_to_tldr(full_news_en)
            if full_news_en
            else summarize_to_tldr(summary_en)
        )
    else:
        print("Error: Nothing got translated. Exiting")
        return

    if not tldr or len(tldr) < 300:
        print(f"Warning: Discarding data: tldr \n{tldr}")
        tldr = ""
    
    news = {
        "title_en": title_en,
        "tldr": tldr,
        "image": data["img_url"],
        "summary_en": summary_en,
        "url": url,
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
            break

    return match


def gen_reply_message(news):
    NT = NewsTemplate
    title_en = (
        NT.title.format(title=news["title_en"].strip()) if news["title_en"] else ""
    )
    text_en = news["summary_en"]
    image = NT.image.format(image=news["image"]) if news["image"] else ""

    tldr = news["tldr"]
    tldr_message = ""
    if tldr.strip():
        tldr_message = NT.tldr.format(
            tldr=tldr, title=title_en, image=image, footer=NT.footer, link=news["url"]
        )
    print(f"Got tldr message, \n{tldr_message}")

    more_news = NT.summary.format(
        news=text_en, title=title_en, image=image, footer=NT.footer, link=news["url"]
    )
    print(f"Got more_news \n{more_news}")

    if tldr_message:
        replies = (tldr_message, more_news)
    else:
        replies = (more_news, None)

    return replies


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
    if hasattr(parent, "title"):
        selftext = parent.selftext_html if parent.selftext_html else ""
        new_html = selftext + f' <a href="{parent.url}"></a>'
        print(f"submission detected \n{new_html}")
    else:
        new_html = parent.body_html
    links_with_domain = extract_links_from_html(new_html)

    return links_with_domain


def manage_mentions(reddit, replied_ids):
    mentions = reddit.inbox.mentions(limit=100)
    unreplied_mentions = (
        mention for mention in mentions if mention.id not in replied_ids
    )
    for index, element in enumerate(unreplied_mentions):
        # check for selftext and comment links and only translate
        # Supported sites.
        update_replied_ids(REPLIED_FILE_PATH, element.id)
        links_with_domain = scan_for_matched_links(element)
        print(f"scanning {index} mention. Got links \n{links_with_domain}")
        replied = []
        for link_domain in links_with_domain:
            link, domain = link_domain
            news = get_news_with_translation(link, domain)
            if news:
                result = reply_and_update_ids(news, element)
                replied.append(True) if result else False

        if True in replied:
            continue

        # We were unable to detect and reply the mention. We assume good faith
        # If mentioned in post try translate without checking site support
        link = element.url if hasattr(element, "url") else None
        if not (link and __is_valid_link(link)):
            continue

        print(f"Trying to extract unrecognized {link} in {element.id}")
        try:
            news = get_news_with_translation(link, link)
            if news:
                reply_and_update_ids(news, element)
        except Exception as e:
            print(f"News extraction exception {e}")


def extract_links_from_html(html):
    soup = BS(html, features="lxml")
    links = [a["href"] for a in soup.find_all("a")]
    print(f"Got links from html \n{links}")

    pattern_str = r"(http|https)?(://)?(www\.)?({site})/(.)*\b"
    pattern_maker = lambda site: pattern_str.format(site=site)
    links_with_domain = []

    for link in links:
        match = matched_link(link, make_pattern=pattern_maker)
        if match and match.group(4):
            links_with_domain.append((link, match.group(4)))

    print(f"Extracted from html \n{links_with_domain}")
    return links_with_domain


def __is_valid_link(url):
    """
    Gets a link and checks it parts to determine if it is an image,
    or other invalid urls
    """
    is_valid_link = True
    img_exts = [".png", ".jpeg", ".gif", ".jpg"]
    keywords = [
        "imgur.com",
        "redd.it",
        "reddit.com",
        "youtu.be",
        "youtube.com",
        "v.reddi.it",
        "gfycat.com",
    ]
    checks = img_exts + keywords

    has_keyword = [True for i in checks if i in url]
    if True in has_keyword:
        is_valid_link = False
    print(f"Is valid link for {url} : {is_valid_link}")

    return is_valid_link


if __name__ == "__main__":
    main()
