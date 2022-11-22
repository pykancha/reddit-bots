import datetime
import time

import requests

url = "http://localhost:8090"


def get_data(places_list):
    all_places = []
    if len(places_list) >= 12:
        all_places.extend(
            [
                places_list[:3],
                places_list[3:6],
                places_list[6:9],
                places_list[9:11],
                places_list[11:],
            ]
        )
    elif len(places_list) >= 5:
        all_places.extend([places_list[:3], places_list[3:]])
    else:
        all_places.append(places_list)

    all_data = {}
    for places_list in all_places:
        bulk_list_arg = ",".join(places_list)
        bulk_url = f"{url}/bulk?list={bulk_list_arg}"
        print("Requesting at ", bulk_url)
        data = request_url(bulk_url)
        all_data.update(data)
        time.sleep(1)
    return all_data


def get_summary_data():
    summary_url = f"{url}/summary"
    print("Requesting at ", summary_url)
    data = request_url(summary_url)
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


def dhading_one_votes(data):
    all_candidate_data = data["dhading"]["constituency : 1"]
    candidates_filter = [
        "Rajendra Prasad Pandey",
        "Bhumi Prasad Tripathi",
        "Himesh Panta",
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


def morang_six_votes(data):
    all_candidate_data = data["morang"]["constituency : 6"]
    candidates_filter = [
        "Dr. Shekhar Koirala",
        "Lal Babu Pandit",
        "Yadav Kumar Pradhan",
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


def mahottari_three_votes(data):
    all_candidate_data = data["mahottari"]["constituency : 3"]
    candidates_filter = [
        "Ram Aadhar Kapar",
        "Mahantha Thakur",
        "Hari Narayan Yadav",
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


def rupandehi_two_votes(data):
    all_candidate_data = data["rupandehi"]["constituency : 2"]
    candidates_filter = [
        "Ganesh Paudel",
        "Bishnu Prasad Paudel",
        "Keshav Bahadur Thapa Magar",
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


def lalitpur_three_votes(data):
    all_candidate_data = data["lalitpur"]["constituency : 3"]
    candidates_filter = [
        "Amrit Khadka",
        "Toshima Karki",
        "Kiran Shahi",
        "Pampha Bhushal",
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


def jhapa_two_votes(data):
    all_candidate_data = data["jhapa"]["constituency : 2"]
    candidates_filter = [
        "Dev Raj Ghimire",
        "Bhadra Prasad Nepal",
        "Hari Kumar Rana Magar",
        "Rudra Prasad Giri",
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


def jhapa_four_votes(data):
    all_candidate_data = data["jhapa"]["constituency : 4"]
    candidates_filter = [
        "Shambhu Prasad Dhakal",
        "Lal Prasad Sawa Limbu",
        "Deu Kumar Thebe",
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


def kathmandu_two_votes(data):
    all_candidate_data = data["kathmandu"]["constituency : 2"]
    candidates_filter = [
        "Sobita Gautam",
        "Onsari Gharti",
        "Maniram Phuyal",
        "Kanti Devi Pokharel",
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


def kathmandu_six_votes(data):
    all_candidate_data = data["kathmandu"]["constituency : 6"]
    candidates_filter = [
        "Shishir Khanal",
        "Shabendra Khanal",
        "Bhemsen Das Pradhan",
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


def kathmandu_five_votes(data):
    all_candidate_data = data["kathmandu"]["constituency : 5"]
    candidates_filter = [
        "Pradip Poudel",
        "Ishwor Pokhrel",
        "Dr.Pranaya",
        "Shree Ram Gurung",
        "Sailesh Dandol",
        "Sushant Shrestha",
        "Ranju Neupane",
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


def kathmandu_eight_votes(data):
    all_candidate_data = data["kathmandu"]["constituency : 8"]
    candidates_filter = [
        "Suman Sayami",
        "Biraj Bhakta Shrestha",
        "Shiv Sundar Rajabhaidha",
        "Jeewan Ram Shrestha",
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


def rauthat_one_votes(data):
    all_candidate_data = data["rauthat"]["constituency : 1"]
    candidates_filter = [
        "Madhav Kumar Nepal",
        "Ajay Kumar Gupta",
        "Rajendra Prasad Shah",
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


def rauthat_two_votes(data):
    all_candidate_data = data["rauthat"]["constituency : 2"]
    candidates_filter = [
        "Kiran Kumar Shah",
        "Mo. Firdos Alam",
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


def westnawalparasi_one_votes(data):
    all_candidate_data = data["nawalparasiwest"]["constituency : 1"]
    candidates_filter = [
        "Binod Kumar Chaudhary",
        "Hridayesh Tripathi",
        "Mahendra Sen (Thakuri)",
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


def lalitpur_two_votes(data):
    all_candidate_data = data["lalitpur"]["constituency : 2"]
    candidates_filter = [
        "Prem Bahadur Maharjan",
        "Sudin Shakya",
        "Raghuwar Raj Thapa",
        "Buddha Ratna Maharjan",
        "Krishna Lal Maharjan",
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


def jhapa_three_votes(data):
    all_candidate_data = data["jhapa"]["constituency : 3"]
    candidates_filter = [
        "Rajendra Prasad Lingden",
        "Krishna Prasad Sitaula",
        "Prakash Pathak",
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


def kathmandu_seven_votes(data):
    all_candidate_data = data["kathmandu"]["constituency : 7"]
    candidates_filter = [
        "Ashmita Singh (Manusi) Yami Bhattarai",
        "Ganesh Parajuli",
        "Shyam Kumar Ghimire",
        "Prabendra",
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


def kathmandu_four_votes(data):
    all_candidate_data = data["kathmandu"]["constituency : 4"]
    candidates_filter = [
        "Gagan Kumar Thapa",
        "Rajan Bhattarai",
        "Dr. Thakur Mohan Shrestha",
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


def bhaktapur_two_votes(data):
    all_candidate_data = data["bhaktapur"]["constituency : 2"]
    candidates_filter = [
        "Durlav Thapa Chhetri",
        "Mahesh Basnet",
        "Sajan BK",
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


def saptari_two_votes(data):
    all_candidate_data = data["saptari"]["constituency : 2"]
    candidates_filter = [
        "Chandra Kanta Raut",
        "Jay Prakash Thakur",
        "Upendra Yadav",
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
            if name == "Ashmita Singh (Manusi) Yami Bhattarai":
                data_dict["name"] = "Manusi Yami Bhattarai"
            elif name == "Chandra Kanta Raut":
                data_dict["name"] = "Chandra Kanta (C.K) Raut"
            elif name == "Ranju Neupane":
                data_dict["name"] = "Ranju Darsana"
            elif name == "Dr.Pranaya Shemser Rana":
                data_dict["name"] = "Pranaya Shumsher"
            elif name == "Bhadra Prasad Nepal":
                data_dict["name"] = "Swagat Nepal"
            elif name == "Bishnu Prasad Paudel":
                data_dict["name"] = "Bisnu Paudel"
            elif name == "Keshav Bahadur Thapa Magar":
                data_dict["name"] = "Keshav Magar"
            elif name == "Krishna Bhakta Pokhrel":
                data_dict["name"] = "Krishna Pokhrel"
            elif name == "Hari Kumar Rana Magar":
                data_dict["name"] = "Hari Magar"
            elif name == "Binod Kumar Chaudhary":
                data_dict["name"] = "Binod Chaudhary"
            elif name == "Mahendra Sen (Thakuri)":
                data_dict["name"] = "Mahendra Sen"
            results.append(data_dict)
            continue
    return results


def party_shortform(partyname):
    fullform_map = {
        "Rastriya Prajatantra Party": "RaPraPa",
        "Maoist Center": "Maoist",
        "Nepali Congress": "Congress",
        "CPN (Unified Socialist)": "CPN (US)",
        "Bibeksheel Sajha Party": "BS Party",
        "Janata Samajwadi Party": "JaSaPa",
        "Loktantrik Samajwadi Party": "LoSaPa",
        "Hamro Nepali Party": "Hamro Nepali Party (Lauro)",
        "Nepal Workers and Peasants Party": "NeMaKiPa",
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
            "pradesh-3/district-dhading",
            "pradesh-1/district-morang",
            "pradesh-2/district-mahottari",
            "pradesh-2/district-rauthat",
            "pradesh-5/district-rupandehi",
            "pradesh-5/district-dang",
        ]
    )
    pprint(dadeldura_one_votes(data))
    pprint(dhading_one_votes(data))
    pprint(morang_six_votes(data))
    pprint(mahottari_three_votes(data))
    pprint(rupandehi_two_votes(data))
    pprint(rauthat_two_votes(data))
    pprint(jhapa_three_votes(data))
    pprint(jhapa_four_votes(data))
    pprint(get_summary_data())
