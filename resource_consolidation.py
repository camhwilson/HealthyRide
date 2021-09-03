from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.request import urlopen
import requests
from dateutil import parser



class Resources:
    def __init__(self, url, resource_extension, resource_calling_string):
        self.url = url
        self.resource_extension = resource_extension
        self.resource_calling_string = resource_calling_string
 
    def create_json(self):
        #uses functions defined in "Resources" scrape web page for links, filter resource links
        #use resource links to call api, and dumps resource data into singular json
        list_of_links = self.list_of_links(self.url)
        overall = self.extract_unique_path(list_of_links, self.resource_extension, self.resource_calling_string)
        json_list = self.combine_json(overall)
        return json_list

    def request_to_list(self, link, limit):
    #calls api for data from resource, returns a list of dictionaries
    #(json format) containing the data. Returned data is limited to "limit" as specified
        limit_string = '&limit='+str(limit)
        json_dict = requests.get(link+limit_string).json()
        print('of length: ' + str(len(json_dict['result']['records'])))
        if len(json_dict['result']['records']) > 20:
            print('correct length')
            return json_dict['result']['records']
        else:
            print('too short to add')
            return []

    def combine_json(self, links):
    #iterates through resource id's, calls API to retrive data, 
    #and combines all resources into one large JSON        
        li = []
        for link in links:
            print('working on: ' + link)
            quarterly_data = self.request_to_list(link, 10000000)
            for i in quarterly_data:
                li.append(i)
        return li
    
    def list_of_links(self, url):
    #returns list of links from scraping a given URL
        req = Request(url)
        html_page = urlopen(req)
        soup = BeautifulSoup(html_page, "lxml")
        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))
        return links

    def extract_unique_path(self, links, strip_string, replace_string):
    #returns list of all links that begin substring "strip_string" stripped of 
    #the "stripstring" output is a list of unique resource id links
        li = []
        for link in links:
            if strip_string in link:
                li.append(link.replace(strip_string, replace_string))
        return list(set(li))


class Trip:
    def __init__(self, tripid, bikeid, toname, usertype, stoptime, 
        fromname, starttime, toid, tripduration, _id, fromid):
        self.tripid = tripid
        self.bikeid = bikeid
        self.toname = toname
        self.usertype = usertype
        self.stoptime = stoptime
        self.fromname = fromname
        self.starttime = starttime
        self.toid = toid
        self.tripduration = tripduration
        self._id = _id
        self.fromid = fromid
        self.weekday = self.datestr_to_dayint(starttime)
    
    def datestr_to_dayint(self, date):
        try:
            datetime_obj = parser.parse(date)
            return datetime_obj.weekday()
        except:
            return 'missing date'
    
def dayint_to_daystr(day_of_week):
    week_dict =  { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 
        3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday' }
    return week_dict[day_of_week]






