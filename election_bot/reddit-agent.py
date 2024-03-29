import os
import random
import time
from functools import partial
from parser import (
    bhaktapur_two_votes,
    chitwan_two_votes,
    dadeldura_one_votes,
    dhading_one_votes,
    eastnawalparasi_one_votes,
    get_current_time,
    get_data,
    get_summary_data,
    sum_total,
    get_pr_data,
    jhapa_four_votes,
    jhapa_three_votes,
    jhapa_two_votes,
    gulmi_two_votes,
    kathmandu_eight_votes,
    kathmandu_five_votes,
    kathmandu_four_votes,
    kathmandu_one_votes,
    kathmandu_seven_votes,
    kathmandu_six_votes,
    kathmandu_two_votes,
    kavre_two_votes,
    lalitpur_three_votes,
    lalitpur_two_votes,
    mahottari_three_votes,
    morang_six_votes,
    party_shortform,
    rauthat_one_votes,
    sunsari_one_votes,
    rauthat_two_votes,
    rupandehi_two_votes,
    westnawalparasi_one_votes,
)

import praw
from dotenv import load_dotenv

USERNAME = "election-bot-2079"
# SUBMISSION_IDS = ["upmnp6"]
SUBMISSION_IDS = ["z0opw6"]

load_dotenv()

FETCH_LIST = [
    "pradesh-7/district-dadeldhura",
    "pradesh-3/district-kathmandu",
    "pradesh-3/district-bhaktapur",
    "pradesh-3/district-lalitpur",
    "pradesh-3/district-chitwan",
    "pradesh-2/district-rauthat",
    "pradesh-1/district-jhapa",
    "pradesh-5/district-nawalparasiwest",
    "pradesh-4/district-nawalparasieast",
    "pradesh-3/district-dhading",
    "pradesh-1/district-morang",
    "pradesh-2/district-mahottari",
    "pradesh-5/district-rupandehi",
    "pradesh-5/district-gulmi",
    "pradesh-3/district-kavrepalanchowk",
    "pradesh-1/district-sunsari",
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
    reddit.validate_on_submit = True
    return reddit


def main():
    main_body_text = ""

    print("Started fetching at: ", get_current_time())
    try:
        summary_data = get_summary_data()
    except Exception as e:
        print("Failed getting summary", e)

    try:
        main_body_text += gen_summary_msg(summary_data)
    except Exception as e:
        print("Failed generating summary, Skipping this time", e)
    else:
        print("Generated Summary message")

    try:
        pr_data = get_pr_data()
    except Exception as e:
        print("Failed getting pr votes", e)

    try:
        main_body_text += gen_pr_msg(pr_data)
    except Exception as e:
        print("Failed generating pr votes table, Skipping this time", e)
    else:
        print("Generated Pr message")


    api_data = get_data(FETCH_LIST)

    election_area_map = {
        "Sunsari 1": partial(sunsari_one_votes, api_data),
        "Mahottari 3": partial(mahottari_three_votes, api_data),
        "Rupandehi 2": partial(rupandehi_two_votes, api_data),
        "Dadeldhura 1": partial(dadeldura_one_votes, api_data),
        "Chitwan 2": partial(chitwan_two_votes, api_data),
        "Kathmandu 1": partial(kathmandu_one_votes, api_data),
        "Kathmandu 2": partial(kathmandu_two_votes, api_data),
        "Kathmandu 4": partial(kathmandu_four_votes, api_data),
        "Kathmandu 5": partial(kathmandu_five_votes, api_data),
        "Kathmandu 6": partial(kathmandu_six_votes, api_data),
        "Kathmandu 7": partial(kathmandu_seven_votes, api_data),
        "Kathmandu 8": partial(kathmandu_eight_votes, api_data),
        "Lalitpur 3": partial(lalitpur_three_votes, api_data),
        "Lalitpur 2": partial(lalitpur_two_votes, api_data),
        "Bhaktapur 2": partial(bhaktapur_two_votes, api_data),
        "West Nawalparasi 1": partial(westnawalparasi_one_votes, api_data),
        "Gulmi 2": partial(gulmi_two_votes, api_data),
        "Kavre 2": partial(kavre_two_votes, api_data),
        "Rauthat 2": partial(rauthat_two_votes, api_data),
        "Jhapa 2": partial(jhapa_two_votes, api_data),
        "East Nawalparasi 1": partial(eastnawalparasi_one_votes, api_data),
        "Dhading 1": partial(dhading_one_votes, api_data),
        "Rauthat 1": partial(rauthat_one_votes, api_data),
        "Morang 6": partial(morang_six_votes, api_data),
        "Jhapa 3": partial(jhapa_three_votes, api_data),
    }

    source = (
        "**Election Data Source**: https://election.ekantipur.com?lng=eng\n\n"
        "**All Party/Candidates PowerBi Visualization by u/authorsuraj**: [PowerBi Link](https://app.powerbi.com/view?r=eyJrIjoiNTU4NDY2YTYtMDU0MS00M2I5LWJjMTAtZGY5MGE5M2IyNGE3IiwidCI6ImNiNzIwMDNkLWYwMjctNDgwMC1hMWZkLTYwYzVmYjRmYmU0OCJ9&pageName=ReportSection)\n\n"
        "**Official And Detailed Election Data**: [Official ECN website](https://result.election.gov.np/ElectionResultCentral2079.aspx)\n\n"
        "**Proportional Vote counts**: [ECN proportional count](https://result.election.gov.np/PRVoteChartResult.aspx)\n\n"
        f"**Last updated**: {get_current_time()} (UTC: {get_current_time(utc=True)})\n\n"
    )
    news = (
        "# News of Interest\n"
        "- [Setopati Analysis of Core kathmandu Votes: Game Over, Sthapit and Singh will fight for second spot]"
        "(https://en.setopati.com/political/158516)"
        "\n\n\n\n"
    )
    footer = (
        "*contribute*: "
        "[Bot code](https://github.com/pykancha/reddit-bots) |"
        "[API code](https://github.com/pykancha/election-api) |"
    )

    for city, data in election_area_map.items():
        try:
            main_body_text += gen_msg(city, data)
        except Exception as e:
            print("Failed generating text, Skipping this time", e, city)
            return

    print("Info fetched completed at: ", get_current_time())

    submission_body = f"{main_body_text}\n\n\n\n{footer}"
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

    submission_body = f"{source}\n\n{main_body_text}\n\n\n\n{footer}"

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
            print(":: Posting...")
            try:
                submission.edit(body=submission_body)
                print(":: Posted as", submission.author)
            except Exception as e:
                print("", e)


def gen_summary_msg(data):
    # Summary Format
    title = "# Federal Seats Summary\n"
    header = "Party|Leads|Wins|\n:--:|:--:|:--:|\n"
    parties = []
    for index, party_info in enumerate(data["federal"]):
        parties.append(
            f"{party_info['name']} | {party_info['leads']} | {party_info['wins']}"
        )
    summary_info = title + header + "\n".join(parties)
    return f"{summary_info}\n\n"


def gen_pr_msg(data):
    # Pr votes Format
    title = "# Proportional Votes\n"
    header = "Party|Votes|%(counted)|%(total)|\n:--:|:--:|:--:|:--:|\n"
    counted_votes = sum_total(data)
    total_voters = 11_000_000
    counted_percent = round((counted_votes / total_voters) * 100, 1)
    metadata = f"**Votes counted**: {counted_votes:,} ~({counted_percent})%\n\n**Remaining Votes**: {(total_voters-counted_votes):,}\n\n"
    parties = []

    party = lambda x: "Hamro Nepali Party (Lauro)" if x == "Hamro Nepali Party" else x
    make_int = lambda x: int("".join(x.split(",")))
    vote_percent = lambda x: round((make_int(x["votes"]) / counted_votes) * 100, 1)
    vote_percent_total = lambda x: round((make_int(x["votes"]) / total_voters) * 100, 1)

    for index, party_info in enumerate(data[:12]):
        parties.append(
            f"{party(party_info['name'])} | {party_info['votes']} | {vote_percent(party_info)}% | {vote_percent_total(party_info)}%"
        )
    pr_info = title + metadata + header + "\n".join(parties)
    return f"{pr_info}\n\n"


def gen_msg(city, data, concat_name=False):
    try:
        data = data()
    except Exception as e:
        print("Scraper error", e)
        data = data()

    voter_stat = ""
    footer = ""
    winner = ""
    try:
        winner_declared = data.get("candidates")[0]["winner_declared"]
        if winner_declared:
            winner = data["candidates"][0]["name"]
    except Exception as e:
        print("Cannot find winner declared text", e)

    if data.get("total_votes", 0) and data.get("percentage", 0):
        voter_stat = f"- **Vote counted**: {data['percentage']}% ({data['vote_counted']:,} of {data['total_votes']:,})"
    elif data.get("vote_counted", 0) <= 1:
        return ""
        # voter_stat += f"- **Vote counting not started yet.**"
    if city == "Kathmandu 1":
        voter_stat += f"- **Prakashman Singh wins by 125 votes margin.**"
    elif city == "Kathmandu 4":
        voter_stat += f"- **Gagan Kumar Thapa wins by a comfortable margin.**"
    elif winner:
        voter_stat += f"- **{winner} wins.**"

    metadata = f"# {city}\n{voter_stat}\n\n"

    # Utils functions
    make_int = lambda x: int("".join(x.split(",")))
    get_name = lambda x: x["name"] if not concat_name else x["name"].split(" ")[0]
    party = lambda x: party_shortform(x["party"])
    vote_percent = lambda x: round((make_int(x["votes"]) / data["vote_counted"]) * 100, 1)


    # Candidate format
    header = "Candidate|Party|Votes|Percentage|\n:--:|:--:|:--:|:--:|\n"
    candidates = []
    for index, d in enumerate(data["candidates"]):
        vote_diff = ""
        if index == 0:
            try:
                second_candidate_votes = make_int(data["candidates"][1]["votes"])
                vote_diff = f"  (+ {(make_int(d['votes']) - second_candidate_votes):,}) "
            except Exception as e:
                print("Vote diff calc error", e, d["name"])
        candidates.append(
            f"{get_name(d)} | {party(d)} | {d['votes']}{vote_diff} | {vote_percent(d)}%"
        )

    candidate_info = metadata + header + "\n".join(candidates)
    candidate_text = f"{candidate_info}\n{footer}" if footer else candidate_info

    body = f"{candidate_text}\n\n"
    return body


if __name__ == "__main__":
    while True:
        main()
        time.sleep(random.randint(160, 240))
