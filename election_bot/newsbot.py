import os
import time

import praw
from dotenv import load_dotenv

from news import (
    get_ktm_votes, get_lalitpur_votes, get_bharatpur_votes, get_dhangadi_votes,
    get_pokhara_votes, get_biratnagar_votes, get_birgunj_votes, concat_party,
    get_damak_votes,get_hetauda_votes, get_janakpur_votes
)
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
    submissions = [reddit.submission('upxo3j')]#, reddit.comment('i8lotdy')]
    try:
        city_data_map = dict(
            Kathmandu=get_ktm_votes(),
            Bharatpur=get_bharatpur_votes(),
            Hetauda=get_hetauda_votes(),
            Damak=get_damak_votes(),
            Janakpur=get_janakpur_votes(),
            Dhangadi=get_dhangadi_votes(),
            Pokhara=get_pokhara_votes(),
            Biratnagar=get_biratnagar_votes(),
            Lalitpur=get_lalitpur_votes(),
        )
    except Exception as e:
        print("Scraper error", e)
        time.sleep(10)
        return

    header = "source: https://election.ekantipur.com\n"
    news = ""
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
    mayor = f"# {city}\n\n## Mayor\n"
    get_name = lambda x: x['candidate-name'] if not concat_name else x['candidate-name'].split(' ')[0]
    party = lambda x: concat_party(x['candidate-party-name'])
    vote_percent = lambda x: int(round( (int(x['vote-numbers']) / data['vote_counted']) * 100, 0))
    header = "Candidate|Party|Votes|Percentage|\n:--:|:--:|:--:|:--:|\n"
    candidates = [f"{get_name(i)} | {party(i)} | {i['vote-numbers']} | {vote_percent(i)}%" for i in data['mayor']]
    mayor += header + "\n".join(candidates)
    deputy = "\n\n## Deputy Mayor\n"
    header = "Candidate|Party|Votes|\n:--:|:--:|:--:|\n"
    candidates = [f"{i['candidate-name'].split(' ')[0]}|{party(i)}|{i['vote-numbers']}" for i in data['deputy']]
    deputy = deputy + header + "\n".join(candidates) if candidates else ""
    if city == 'Kathmandu':
        extra = f"**Some Stats**\n\nTotal eligible Voters: 300,242 (64% = {data['total_votes']:,})\n\nVote Counted: {data['percentage']}% ({data['vote_counted']:,})"
        body = f'{mayor}\n\n{extra}\n\n{deputy}\n\n'
    else:
        body = f'{mayor}\n\n{deputy}\n\n' if deputy else f'{mayor}\n\n'
    return body

if __name__ == "__main__":
    keep_alive()
    while True:
        main()
        time.sleep(60)
