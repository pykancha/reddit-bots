import os
import time

import praw
from dotenv import load_dotenv

from news import get_ktm_votes, get_lalitpur_votes, get_bharatpur_votes
from keep_alive import keep_alive

USERNAME = "election-bot-2079"
load_dotenv()

def login(username):
    # rnepal-bot -> RNEPALBOT | link_guru -> LINK_GURU
    BOT_NAME = username.replace("-", "").upper()
    reddit = praw.Reddit(
        client_id=os.getenv(f"{BOT_NAME}_ID"),
        client_secret=os.getenv(f"{BOT_NAME}_SECRET"),
        user_agent=os.getenv(f"{BOT_NAME}_USERAGENT"),
        username=username,
        password=os.getenv(f"{BOT_NAME}_PASS"),
    )
    return reddit


def main():
    reddit = login(USERNAME)
    submissions = [reddit.comment('i8lotdy'), reddit.submission('upxo3j')]
    try:
        city_data_map = dict(
            Kathmandu=get_ktm_votes(),
            Bharatpur=get_bharatpur_votes(),
            Lalitpur=get_lalitpur_votes(),
        )
    except Exception as e:
        print("Scraper error", e)
        time.sleep(10)
        return

    header = "source: https://election.ekantipur.com\n"
    news = "\n\n# News\n\n- [एमालेको विरोधपछि रोकियो भरतपुर महानगरको मतगणना](https://www.setopati.com/election/localelection/270907) [Restarted after 25 mins]"
    footer = """^^contribute:  [Bot code](https://github.com/pykancha/reddit-bots) |  [Api code](https://github.com/pykancha/election-api) | [Api url for your personal automation](https://g7te1m.deta.dev/)"""
    text = ''
    for city, data in city_data_map.items():
        text += gen_msg(city, data) if city!='Kathmandu' else gen_msg(city, data, concat_name=True)

    submission_body = f"{header}\n{text}\n{news}\n\n{footer}"

    for submission in submissions:
        body = submission.selftext if not hasattr(submission, 'body') else submission.body
        if body.strip() == submission_body.strip():
            print("Yes")
        else:
            print(submission.author)
            submission.edit(body=submission_body)


def gen_msg(city, data, concat_name=False):
    mayor = f"# {city}\n\n## Mayor\n\n"
    get_name = lambda x: x['candidate-name'] if not concat_name else x['candidate-name'].split(' ')[0]
    candidates = [f"- {get_name(i)} = {i['vote-numbers']}" for i in data['mayor']]
    mayor += "\n\n".join(candidates)
    deputy = "\n\n## Deputy Mayor\n\n"
    candidates = [f"- {i['candidate-name'].split(' ')[0]} = {i['vote-numbers']}" for i in data['deputy']]
    deputy = deputy + "\n".join(candidates) if candidates else ""
    body = f'{mayor}\n\n{deputy}\n\n' if deputy else f'{mayor}\n\n'
    return body

if __name__ == "__main__":
    keep_alive()
    while True:
        main()
        time.sleep(120)
