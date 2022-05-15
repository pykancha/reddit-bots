import requests

url = "https://8xf7bb.deta.dev/"

def request_url(url):
    response = requests.get(url)
    return response.json()

def filter_data(data, filter):
    results = []
    for data_dict in data:
        name = data_dict['candidate-name']
        if name.split(' ')[0] in filter:
           if name == 'Balendra Shah':
              data_dict['candidate-name'] = 'Balen Shah'
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

def get_ktm_votes():
    req_url = f'{url}kathmandu'
    data = request_url(req_url)
    mayors = ['Balendra', 'Keshav', 'Shirjana', 'Suman', 'Madan', 'Samiksha']
    deputy = ['Sunita', 'Rameshwore', 'Binita']
    mayor_dict = filter_data(data, mayors)
    deputy_dict = filter_data(data, deputy)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
    }

def get_bharatpur_votes():
    req_url = f'{url}bharatpur'
    data = request_url(req_url)
    mayors = ['Renu', 'Vijay', 'Jaggannath']
    deputy = []
    mayor_dict = filter_data(data, mayors)
    deputy_dict = filter_data(data, deputy)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
    }

def get_dhangadi_votes():
    req_url = f'{url}dhangadi'
    data = request_url(req_url)
    mayors = ['Gopal', 'Nripa', 'Ran']
    deputy = ['Shanti', 'Prabhakar', 'Kandakala']
    mayor_dict = filter_data(data, mayors)
    deputy_dict = filter_data(data, deputy)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
    }


def get_lalitpur_votes():
    req_url = f'{url}lalitpur'
    data = request_url(req_url)
    mayors = ['Chiri', 'Hari']
    deputy = []
    mayor_dict = filter_data(data, mayors)
    deputy_dict = filter_data(data, deputy)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
    }

def get_pokhara_votes():
    req_url = f'{url}pokhara'
    data = request_url(req_url)
    mayors = ['Dhana', 'Krishna', 'Shankar', 'Khadak', 'Shushila']
    deputy = []
    mayor_dict = filter_data(data, mayors)
    deputy_dict = filter_data(data, deputy)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
    }

def get_biratnagar_votes():
    req_url = f'{url}biratnagar'
    data = request_url(req_url)
    mayors = ['Nagesh', 'Sagar', 'Umesh', 'Prahlad']
    deputy = []
    mayor_dict = filter_data(data, mayors)
    deputy_dict = filter_data(data, deputy)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
    }

def get_birgunj_votes():
    req_url = f'{url}birgunj'
    data = request_url(req_url)
    mayors = ['Rajesh', 'Bijay', 'Girish']
    deputy = []
    mayor_dict = filter_data(data, mayors)
    deputy_dict = filter_data(data, deputy)
    return {
      'mayor': mayor_dict,
      'deputy': deputy_dict,
    }



if __name__ == '__main__':
    from pprint import pprint
    pprint(get_ktm_votes())
