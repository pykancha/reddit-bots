import datetime
import requests

url = "https://8xf7bb.deta.dev/"

def request_url(url):
    response = requests.get(url)
    return response.json()

def filter_data(data, filter):
    results = []
    for data_dict in data:
        name = data_dict['candidate-name']
        if name.split(' ')[0] in filter or name.strip() in filter:
           if name == 'Balendra Shah':
              data_dict['candidate-name'] = 'Balen Shah'
           if name == 'Khadak Raj Poudel':
              data_dict['candidate-name'] += ' (Ganess)'
           if name == 'Harka Raj Rai':
              data_dict['candidate-name'] += ' (Sampang)'
           results.append(data_dict)
           continue
    return results

def concat_party(partyname):
    concat_map = {
        "Rastriya Prajatantra Party" : "RPP",
        "Maoist Center" : "Maoist",
        "Nepali Congress" : "Congress",
        "CPN (Unified Socialist)":"CPN (US)",
        "Bibeksheel Sajha Party" : "BS Party",
        "Janata Samajwadi Party" : "JSP",
        }
    return concat_map.get(partyname, partyname)

def sum_total(data):
    total = 0
    for data_dict in data:
        vote_no = 0
        if data_dict.get('vote-numbers', False):
            try:
                vote_no = int(data_dict.get('vote-numbers', '0'))
            except Exception as e:            
                print("Voter total error", e, data_dict)
                pass
        total += vote_no
    return total

def get_ktm_votes():
    req_url = f'{url}kathmandu'
    data = request_url(req_url)
    mayors = ['Balendra', 'Keshav', 'Shirjana', 'Suman', 'Madan', 'Samiksha', "Ram"]
    deputy = []#['Sunita', 'Rameshwore', 'Binita']
    mayor_dict = filter_data(data, mayors)
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(mayor_dict)
    counted_votes += 0.2 * counted_votes
    total_votes = 1_91_186
    vote_percentage = round((counted_votes / total_votes) * 100, 2)
    return {
      'mayor': mayor_dict[:-1],
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
    }

def get_bharatpur_votes():
    req_url = f'{url}bharatpur'
    data = request_url(req_url)
    mayors = ['Renu', 'Vijay', 'Jaggannath', 'Prabin', 'Yog', "Purna", "Ganes", "Surya", "Vinod", "Yam", "Khem", "Surendra"]
    deputy = []
    mayor_dict = filter_data(data, mayors[:2])
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(filter_data(data, mayors))
    counted_votes += 0.16 * counted_votes
    total_votes = 1_27_000
    vote_percentage = round((counted_votes / total_votes) * 100, 2)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
    }

def get_dhangadi_votes():
    req_url = f'{url}dhangadi'
    data = request_url(req_url)
    mayors = ['Gopal', 'Nripa', 'Ran', "Kabindra", "Basanta"]
    deputy = []#['Shanti', 'Prabhakar', 'Kandakala']
    mayor_dict = filter_data(data, mayors[:2])
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(filter_data(data, mayors))
    counted_votes += 0.18 * counted_votes
    total_votes = 53_181
    counted_votes = total_votes
    vote_percentage = round((counted_votes / total_votes) * 100, 2)

    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
    }


def get_lalitpur_votes():
    req_url = f'{url}lalitpur'
    data = request_url(req_url)
    mayors = ['Chiri', 'Hari', 'Asta', "Ujjwal"]
    deputy = []
    mayor_dict = filter_data(data, mayors[:2])
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(filter_data(data, mayors))
    counted_votes += 0.15 * counted_votes
    total_votes = 83_540
    vote_percentage = round((counted_votes / total_votes) * 100, 2)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
    }

def get_pokhara_votes():
    req_url = f'{url}pokhara'
    data = request_url(req_url)
    mayors = ['Dhana', 'Krishna', 'Shankar', 'Khadak', 'Shusila']
    deputy = []
    mayor_dict = filter_data(data, mayors)
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(mayor_dict)
    counted_votes += 0.15 * counted_votes
    total_votes = 1_43_226
    vote_percentage = round((counted_votes / total_votes) * 100, 2)

    return {
      'mayor': mayor_dict[:2],
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
   }

def get_biratnagar_votes():
    req_url = f'{url}biratnagar'
    data = request_url(req_url)
    mayors = ['Nagesh', 'Sagar', 'Umesh', 'Prahlad']
    deputy = []
    mayor_dict = filter_data(data, mayors[:2])
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(filter_data(data, mayors))
    counted_votes += 0.15 * counted_votes
    total_votes = 89_678
    vote_percentage = round((counted_votes / total_votes) * 100, 2)

    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
   }

def get_damak_votes():
    req_url = f'{url}url?url=https://election.ekantipur.com/pradesh-1/district-jhapa/damak?lng=eng'
    data = request_url(req_url)
    mayors = ['Ram Kumar Thapa', 'Gita', "Dipesh Kumar Rai", "Pawan Bista"]
    deputy = []
    mayor_dict = filter_data(data, mayors[:2])
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(filter_data(data, mayors))
    counted_votes += 0.15 * counted_votes
    total_votes = 39_949
    counted_votes = total_votes
    vote_percentage = round((counted_votes / total_votes) * 100, 2)

    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
    }

def get_hetauda_votes():
    req_url = f'{url}url?url=https://election.ekantipur.com/pradesh-3/district-makwanpur/hetauda?lng=eng'
    data = request_url(req_url)
    mayors = ["Meena", 'Dipak', "Ananta", "Sanjiv Khanal"]
    deputy = []
    mayor_dict = filter_data(data, mayors[:2])
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(filter_data(data, mayors))
    counted_votes += 0.15 * counted_votes
    total_votes = 74_185
    vote_percentage = round((counted_votes / total_votes) * 100, 2)

    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
    }

def get_janakpur_votes():
    req_url = f'{url}url?url=https://election.ekantipur.com/pradesh-2/district-dhanusha/janakpurdham?lng=eng'
    data = request_url(req_url)
    mayors = ["Manoj Kumar Sah Sudi", "Shiva", "Balram", "Manoj Chaudhari", "Lal", "Janaki", "Kisa"]
    deputy = []
    mayor_dict = filter_data(data, mayors[:2])
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(filter_data(data, mayors))
    counted_votes += 0.21 * counted_votes
    total_votes = 59_970
    vote_percentage = round((counted_votes / total_votes) * 100, 2)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
    }

def get_dharan_votes():
    req_url = f'{url}url?url=https://election.ekantipur.com/pradesh-1/district-sunsari/dharan?lng=eng'
    data = request_url(req_url)
    mayors = ["Kishore Rai", "Harka Raj Rai"]
    deputy = []
    mayor_dict = filter_data(data[:2], mayors)
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(mayor_dict)
    counted_votes += 0.23 * counted_votes
    total_votes = 62_897
    counted_votes = total_votes
    vote_percentage = round((counted_votes / total_votes) * 100, 2)

    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
    }

def get_jitpur_votes():
    req_url = f'{url}url?url=https://election.ekantipur.com/pradesh-2/district-bara/jitpur-simara?lng=eng'
    data = request_url(req_url)
    mayors = ["Rajan Poudel", "Saraswati", "Sanjay", "Madhav"]
    deputy = []
    mayor_dict = filter_data(data, mayors[:2])
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(filter_data(data, mayors))
    counted_votes += 0.2 * counted_votes
    total_votes = 52_958
    vote_percentage = round((counted_votes / total_votes) * 100, 2)

    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
    }

def get_birgunj_votes():
    req_url = f'{url}birgunj'
    data = request_url(req_url)
    mayors = ['Rajesh Man Singh', 'Bijay Kumar Sarawagi', 'Girish Giri']
    deputy = []
    mayor_dict = filter_data(data, mayors[:2])
    deputy_dict = filter_data(data, deputy)
    counted_votes = sum_total(filter_data(data, mayors))
    counted_votes += 0.1 * counted_votes
    total_votes = 93_236
    vote_percentage = round((counted_votes / total_votes) * 100, 2)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
      'vote_counted': int(counted_votes),
      'percentage': vote_percentage,
      'total_votes': total_votes,
    }

def get_current_time(utc=False):
    utctime = datetime.datetime.utcnow()
    offset = datetime.timedelta(hours=5, minutes=45)
    nepaltime = utctime + offset
    if utc:
        nepaltime = utctime
    time_str = nepaltime.strftime("%d %b %I:%M %p")
    return time_str

if __name__ == '__main__':
    from pprint import pprint
    #pprint(get_janakpur_votes())
    pprint(get_dharan_votes())
