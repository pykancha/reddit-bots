import datetime

import requests

url = "http://localhost:8090"


def get_data(places_list):
    bulk_list_arg = ",".join(places_list)
    bulk_url = f"{url}/bulk?list={bulk_list_arg}"
    print("Requesting at ", bulk_url)
    data = request_url(bulk_url)
    return data


def request_url(url):
    response = requests.get(url)
    return response.json()


def dadeldura_one_votes(data):
    all_candidate_data = data["dadeldhura"]["constituency : 1"]
    candidates_filter = ["Sher", "Sagar", "Karna Bahadur Malla"]
    filtered_candiate_data = filter_data(all_candidate_data, candidates_filter)
    counted_votes = sum_total(all_candidate_data)
    # Add up invalid votes through percentage guess
    corrected_counted_votes = int(counted_votes + 0.2 * counted_votes) + 1
    # Lookup newspaper to get this number estimate by ECN
    # total_votes = 0
    # vote_percentage = round((counted_votes / total_votes) * 100, 2)
    return {
        "candidates": filtered_candiate_data,
        "vote_counted": corrected_counted_votes,
        # "percentage": vote_percentage,
        # "total_votes": total_votes,
    }


def kathmandu_one_votes(data):
    all_candidate_data = data["kathmandu"]["constituency : 1"]
    candidates_filter = [
        "Rabindra Mishra",
        "Kiran Puoudel",
        "Prakashman Singh",
        "Pukar Bam",
    ]
    filtered_candiate_data = filter_data(all_candidate_data, candidates_filter)
    counted_votes = sum_total(all_candidate_data)
    # Add up invalid votes through percentage guess
    corrected_counted_votes = int(counted_votes + 0.2 * counted_votes) + 1
    # Lookup newspaper to get this number estimate by ECN
    # total_votes = 0
    # vote_percentage = round((counted_votes / total_votes) * 100, 2)
    return {
        "candidates": filtered_candiate_data,
        "vote_counted": corrected_counted_votes,
        # "percentage": vote_percentage,
        # "total_votes": total_votes,
    }


def chitwan_two_votes(data):
    all_candidate_data = data["chitwan"]["constituency : 2"]
    candidates_filter = [
        "Rabi Lamichhane",
        "Umesh Shrestha",
        "Krishna Bhakta Pokhrel",
    ]
    filtered_candiate_data = filter_data(all_candidate_data, candidates_filter)
    counted_votes = sum_total(all_candidate_data)
    # Add up invalid votes through percentage guess
    corrected_counted_votes = int(counted_votes + 0.2 * counted_votes) + 1
    # Lookup newspaper to get this number estimate by ECN
    # total_votes = 0
    # vote_percentage = round((counted_votes / total_votes) * 100, 2)
    return {
        "candidates": filtered_candiate_data,
        "vote_counted": corrected_counted_votes,
        # "percentage": vote_percentage,
        # "total_votes": total_votes,
    }


def filter_data(data, filter):
    results = []
    for data_dict in data:
        name = data_dict["name"]
        if name.split(" ")[0] in filter or name.strip() in filter:
            results.append(data_dict)
            continue
    return results


def party_shortform(partyname):
    fullform_map = {
        "Rastriya Prajatantra Party": "RPP",
        "Maoist Center": "Maoist",
        "Nepali Congress": "Congress",
        "CPN (Unified Socialist)": "CPN (US)",
        "Bibeksheel Sajha Party": "BS Party",
        "Janata Samajwadi Party": "JSP",
    }
    return fullform_map.get(partyname, partyname)


def sum_total(data):
    total = 0
    for data_dict in data:
        vote_no = 0
        if data_dict.get("votes", False):
            try:
                vote_no = int(data_dict.get("votes", "0"))
            except Exception as e:
                print("Voter total error", e, data_dict)
                pass
        total += vote_no
    return total


def get_current_time(utc=False):
    utctime = datetime.datetime.utcnow()
    offset = datetime.timedelta(hours=5, minutes=45)
    nepaltime = utctime + offset
    if utc:
        nepaltime = utctime
    time_str = nepaltime.strftime("%d %b %I:%M %p")
    return time_str


if __name__ == "__main__":
    from pprint import pprint

    data = get_data(
        [
            "pradesh-7/district-dadeldhura",
            "pradesh-1/district-jhapa",
            "pradesh-3/district-kathmandu",
            "pradesh-3/district-lalitpur",
            "pradesh-3/district-bhaktapur",
            "pradesh-3/district-chitwan",
            "pradesh-3/district-chitwan",
        ]
    )
    pprint(dadeldura_one_votes(data))
