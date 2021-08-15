

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

from urllib.request import urlopen
import requests
import pandas as pd
from json import dumps


class ResourceOperations:

    #calls api for data from resource, returns a list of dictionaries (json format) containing the data
    @staticmethod
    def request_to_list(link):
        limit = '&limit=1000000'
        json_dict = requests.get(link+limit).json()
        print('working on: ' + link +' of length: '+ str(len(json_dict['result']['records'])))
        if len(json_dict['result']['records']) > 30:
            return json_dict['result']['records']
        else:
            return []

    #iterates through resource id's, calls API to retrive data, and combines all resources
    #into one large JSON
    @staticmethod
    def combine_json(links):
        li = []
        for link in links:
            quarterly_data = ResourceOperations.request_to_list(link)
            for i in quarterly_data:
                li.append(i)
        return li

    #returns list of links from URL
    @staticmethod
    def list_of_links(url):
        req = Request(url)
        html_page = urlopen(req)
        soup = BeautifulSoup(html_page, "lxml")
        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))
        return links

    #returns list of all links that begin substring "strip_string" stripped of the "stripstring"
    #output is a list of unique resource id links
    @staticmethod
    def extract_unique_path(links, strip_string):
        li = []
        for link in links:
            if strip_string in link:
                li.append(link.replace(strip_string, 'https://data.wprdc.org/api/3/action/datastore_search?resource_id='))
        return list(set(li))




url = 'https://data.wprdc.org/dataset/healthyride-trip-data'
resource_extension = '/dataset/healthyride-trip-data/resource/'


list_of_links = ResourceOperations.list_of_links(url)
overall = ResourceOperations.extract_unique_path(list_of_links, resource_extension)
json_list = ResourceOperations.combine_json(overall)

jsonStr = dumps(json_list)
df = pd.read_json(jsonStr)
