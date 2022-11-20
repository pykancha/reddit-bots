import os
import time
from functools import partial
from parser import (
    chitwan_two_votes,
    dadeldura_one_votes,
    get_current_time,
    get_data,
    kathmandu_one_votes,
    party_shortform,
)

import praw
import requests
from dotenv import load_dotenv

USERNAME = "election-bot-2079"
SUBMISSION_IDS = [
    "upmnp6",
]

# GRAPH_URL = "https://electionupdate.herokuapp.com"

load_dotenv()

FETCH_LIST = [
    "pradesh-7/district-dadeldhura",
    "pradesh-1/district-jhapa",
    "pradesh-3/district-kathmandu",
    "pradesh-3/district-lalitpur",
    "pradesh-3/district-bhaktapur",
    "pradesh-3/district-chitwan",
    "pradesh-3/district-chitwan",
]


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
    api_data = get_data(FETCH_LIST)
    election_area_map = {
        "Dadeldhura 1": partial(dadeldura_one_votes, api_data),
        "Kathmandu 1": partial(kathmandu_one_votes, api_data),
        "Chitwan 2": partial(chitwan_two_votes, api_data),
    }

    source = (
        "**Election Data Source**: https://election.ekantipur.com?lng=eng\n\n"
        # "**Data for every local ward/post**: [Official ECN website](https://result.election.gov.np/LocalElectionResult2079.aspx)\n\n"
        f"**Last updated**: {get_current_time()} (UTC: {get_current_time(utc=True)})"
    )
    news = (
        "# News of Interest\n"
        "- [A Look at Balen's Core team and their strategic planning for KTM mayoral election]"
        "(https://shilapatra.com/detail/85494)"
        "([Reddit discussion]"
        "(https://www.reddit.com/r/Nepal/comments/uqe55n))\n\n"
        "- [Harka Sampang, A Revolution. A look into Harka and his lone struggle to see better dharan]"
        "(https://www.setopati.com/election/localelection/272021)\n\n"
        "- [All dalit *independent* panel elected in a ward of a rural municipality in Jumla]"
        "(https://kathmandupost.com/karnali-province/2022/05/17/constantly-spurned-how-dalits-united-to-create-history-in-local-elections)"
        "([Reddit discussion]"
        "(https://www.reddit.com/r/Nepal/comments/uq3ko0))\n\n"
        "- [Setopati Analysis of Core kathmandu Votes: Game Over, Sthapit and Singh will fight for second spot]"
        "(https://en.setopati.com/political/158516)"
        "\n\n\n\n"
    )
    footer = (
        "*contribute*: "
        "[Bot code](https://github.com/pykancha/reddit-bots) |"
        "[API code](https://github.com/pykancha/election-api) |"
        "[API url for your personal automation](https://g7te1m.deta.dev/)"
    )
    text = ""
    print("Started fetching at: ", get_current_time())
    for city, data in election_area_map.items():
        try:
            text += gen_msg(city, data)
        except Exception as e:
            print("Failed generating text, Skipping this time", e, city)
            return
        time.sleep(1)
    print("Info fetched completed at: ", get_current_time())

    submission_body = f"{text}\n\n\n\n{footer}"
    cached_submission = ""
    try:
        with open("cache.json", "r") as rf:
            cached_submission = rf.read()
    except Exception as e:
        print("Error: Reading cache file failed", e)

    if cached_submission == submission_body:
        print("Cached matched: No new updates")
        return

    print("Cached unmatched: Updating")
    # IMP: Write to cache before inserting timestamp for next time comparision
    with open("cache.json", "w") as wf:
        wf.write(submission_body)

    submission_body = f"{source}\n\n{text}\n\n\n\n{footer}"

    reddit = login(USERNAME)
    submissions = [reddit.submission(i) for i in SUBMISSION_IDS]

    print(submissions)
    for submission in submissions:
        body = (
            submission.selftext if not hasattr(submission, "body") else submission.body
        )
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

    voter_stat = ""
    footer = ""

    if data.get("total_votes", 0) and data.get("percentage", 0):
        voter_stat = f"- **Vote counted**: {data['percentage']}% ({data['vote_counted']:,} of {data['total_votes']:,})"

    metadata = f"# {city}\n{voter_stat}\n\n"

    # Utils functions
    get_name = lambda x: x["name"] if not concat_name else x["name"].split(" ")[0]
    party = lambda x: party_shortform(x["party"])
    vote_percent = lambda x: round((int(x["votes"]) / data["vote_counted"]) * 100, 1)

    # Mayor format
    header = "Candidate|Party|Votes|Percentage|\n:--:|:--:|:--:|:--:|\n"
    candidates = []
    for index, d in enumerate(data["candidates"]):
        vote_diff = ""
        if index == 0:
            try:
                second_candidate_votes = int(data["candidates"][2]["votes"])
                vote_diff = f"  (+ {(int(d['votes']) - second_candidate_votes):,}) "
            except Exception as e:
                print("Vote diff calc error", e, d["name"])
        candidates.append(
            f"{get_name(d)} | {party(d)} | {int(d['votes']):,}{vote_diff} | {vote_percent(d)}%"
        )

    candidate_info = metadata + header + "\n".join(candidates)
    candidate_text = f"{candidate_info}\n{footer}" if footer else candidate_info

    body = f"{candidate_text}\n\n"
    return body


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)
