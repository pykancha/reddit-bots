import os
import time

import praw
import requests
from dotenv import load_dotenv

from news import (
    get_ktm_votes, get_lalitpur_votes, get_bharatpur_votes, get_dhangadi_votes,
    get_pokhara_votes, get_biratnagar_votes, get_birgunj_votes, concat_party,
    get_damak_votes,get_hetauda_votes, get_janakpur_votes, get_dharan_votes, get_jitpur_votes,
    get_current_time,
)

from keep_alive import keep_alive

USERNAME = "election-bot-2079"
GRAPH_URL = "https://electionupdate.herokuapp.com"
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
    city_data_map = dict(
        Kathmandu=get_ktm_votes,
        Bharatpur=get_bharatpur_votes,
        Dharan=get_dharan_votes,
        Damak=get_damak_votes,
        Hetauda=get_hetauda_votes,
        Janakpur=get_janakpur_votes,
        Dhangadi=get_dhangadi_votes,
        Pokhara=get_pokhara_votes,
        Biratnagar=get_biratnagar_votes,
        Lalitpur=get_lalitpur_votes,
    )

    source = f"**Election Data Source**: https://election.ekantipur.com?lng=eng\n\n**Last updated**: {get_current_time()}"
    news = ("# News of Interest\n"
           "- [A Look at Balen's Core team and their strategic planning for KTM mayoral election]"
                "(https://shilapatra.com/detail/85494)"
              "([Reddit discussion]"
                "(https://www.reddit.com/r/Nepal/comments/uqe55n))\n\n"

           "- [All dalit *independent* panel elected in a ward of a rural municipality in Jumla]"
              "(https://kathmandupost.com/karnali-province/2022/05/17/constantly-spurned-how-dalits-united-to-create-history-in-local-elections)"
              "([Reddit discussion]"
                "(https://www.reddit.com/r/Nepal/comments/uq3ko0))\n\n"

           "- [Setopati Analysis of Core kathmandu Votes: Game Over, Sthapit and Singh will fight for second spot]"
           "(https://en.setopati.com/political/158516)"

           "\n\n\n\n"
    )
    footer = ("*contribute*: "
             "[Bot code](https://github.com/pykancha/reddit-bots) |"
             "[API code](https://github.com/pykancha/election-api) |"
             "[API url for your personal automation](https://g7te1m.deta.dev/)"
    )
    text = ''
    print("Started fetching at: ", get_current_time())
    for city, data in city_data_map.items():
        try:
            text += gen_msg(city, data) if city!='Kathmandu' else gen_msg(city, data, concat_name=True)
        except Exception as e:
            print("Failed generating text, Skipping this time", e, city)
            return
        time.sleep(1)
    print("Info fetched completed at: ", get_current_time())

    submission_body = f"{text}\n\n{news}\n\n\n\n{footer}"
    cached_submission = ''
    try:
        with open('cache.json', 'r') as rf:
            cached_submission = rf.read()
    except Exception as e:
        print("Error: Reading cache file failed", e)

    if cached_submission == submission_body:
        print("Cached matched: No new updates")
        #return

    print("Cached unmatched: Updating")
    # IMP: Write to cache before inserting timestamp for next time comparision
    with open('cache.json', 'w') as wf:
        wf.write(submission_body)

    submission_body = f"{source}\n\n{text}\n\n{news}\n\n\n\n{footer}"

    reddit = login(USERNAME)
    submissions = [reddit.comment('i8lotdy')]
    submissions = [reddit.submission('upxo3j')]

    for submission in submissions:
        body = submission.selftext if not hasattr(submission, 'body') else submission.body
        body_list = body.strip().split("\n")
        text_list = submission_body.strip().split("\n")
        body_list.remove(body_list[2])
        text_list.remove(text_list[2])
        if body_list == text_list:
            print("No new updates")
        else:
            try:
                requests.get(GRAPH_URL)
            except Exception as e:
                print("Graph url cannot accessed skipping", e)
            print(submission.author)
            try:
                submission.edit(body=submission_body)
            except Exception as e:
                print("Praw submit error Skipping this time..", e)


def gen_msg(city, data, concat_name=False):
    try:
        data = data()
    except Exception as e:
        print("Scraper error", e)
        time.sleep(5)
        data = data()

    voter_stat = ''
    footer = ''
    if city == 'Kathmandu':
        voter_stat = (
                f"- **Total eligible voters**: 300,242 (64% = {data['total_votes']:,})\n"
                f"- **Vote counted**: {data['percentage']}% ({data['vote_counted']:,})\n"
        )
        footer = (
                f"- [Lead Gap Visualization By u/time_chemist_8566]({GRAPH_URL})\n"
                f"- [CSV/Excel data dump of KTM mayor election updates](https://g7te1m.deta.dev/data/)"
        )
    elif data.get('total_votes', 0) and data.get('percentage', 0):
        voter_stat = f"- **Vote counted**: {data['percentage']}% ({data['vote_counted']:,} of {data['total_votes']:,})"
    metadata = f"# {city}\n{voter_stat}\n\n"

    # Utils functions
    get_name = lambda x: x['candidate-name'] if not concat_name else x['candidate-name'].split(' ')[0]
    party = lambda x: concat_party(x['candidate-party-name'])
    vote_percent = lambda x: round( (int(x['vote-numbers']) / data['vote_counted']) * 100, 1)

    # Mayor format
    header = "Candidate|Party|Votes|Percentage|\n:--:|:--:|:--:|:--:|\n"
    candidates = []
    for index, d in enumerate(data['mayor']):
        vote_diff = ''
        if index == 0:
            try:
                second_candidate_votes = int(data['mayor'][1]['vote-numbers'])
                vote_diff = f"  (+ {(int(d['vote-numbers']) - second_candidate_votes):,}) "
            except Exception as e:
                print("Vote diff calc error", e, d['candidate-name'])
        candidates.append(f"{get_name(d)} | {party(d)} | {int(d['vote-numbers']):,}{vote_diff} | {vote_percent(d)}%")

    mayor = metadata + header + "\n".join(candidates)
    mayor = f"{mayor}\n{footer}" if footer else mayor

    # Deputy Format
    deputy = "\n\n## Deputy Mayor\n"
    header = "Candidate|Party|Votes|\n:--:|:--:|:--:|\n"
    candidates = [f"{i['candidate-name'].split(' ')[0]}|{party(i)}|{int(i['vote-numbers']):,}" for i in data['deputy']]
    deputy = deputy + header + "\n".join(candidates) if candidates else ""

    body = f'{mayor}\n\n{deputy}\n\n' if deputy else f'{mayor}\n\n'
    return body

if __name__ == "__main__":
    keep_alive()
    while True:
        main()
        time.sleep(60)
