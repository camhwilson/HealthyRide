from dateutil import parser
from dataclasses import dataclass

station_dict = {
    'Downtown': ['1000', '49701', '1002', '1001', '49691', '49671', '1056', '1003', 
                                '49731', '1004', '1006', '49651', '1010'],
    
    'Strip District': ['1016', '1017', '49611', '1059', '1060'],

    'East Liberty' : ['1026', '1027', '1029', '1024', '49391', '49371', '1064'],

    'Lawrenceville' : ['1061', '49581', '1019', '1020', '49501', '49951', '49561', '1018'],

    'North Shore' : ['49941', '49921', '1012', '1013'],

    'Central Northside' : ['1014', '1015', '49881'],

    'Southside Flats' : ['1074', '1049', '1048', '1047', '1046', '1045', '1084'],

    'Oakland' : ['1038', '1044', '1039', '1091', '1093', '1041', '1095', '1036', '1037', '1099', 
                        '1040', '1097', '1035', '1094', '49271'] 

}




@dataclass
class Trip:
    """This is a dataclass that """
    tripid : str
    bikeid : str
    toname: str
    usertype : str
    stoptime : str
    fromname : str
    starttime : str
    toid : str
    tripduration : str
    _id : int
    fromid : str
    
    def __post_init__(self):
        '''
        Upon initialization, weekday parameter is created using datestr_to_dayint(). See 
        that function's documentation for an explanation of functionality.
        '''
        self.weekday = self.datestr_to_dayint(self.starttime)
    
    def weekday_arrivals_todict(list_of_trip_objects):
        '''
        This function takes in a list of trips and returns a dictionary where keys are days of week, and values
        are a list of times (hour of the day) people arrived at a station. Very similar to weekday departures
        to dict function (below), which is a function that does the same thing except maps departures.

            Parameters:
                list_of_trip_objects (list): List of Trip objects
            Returns:
                return weekday_dict (dict): Dictionary where keys are days of week, vals are list of arrival times.
                Keep in mind weekdays are integers, where monday is indexed as 0.
            ex. format:
            {
                0: [12:00, 1:32, 3:04, 4:21],
                1: [13:24, 1:10, 13:02, 21:02]
                ...
            }
        '''
        weekday_dict = {}
        for Trip in list_of_trip_objects:
            this_weekday = Trip.weekday
            if this_weekday not in list(weekday_dict.keys()):
                weekday_dict[this_weekday] = [Trip.starttime.split(" ")[1]]
            else:
                weekday_dict[this_weekday].append(Trip.starttime.split(" ")[1])
        return weekday_dict

    def weekday_departures_todict(list_of_trip_objects):
        weekday_dict = {}
        '''
        This function takes in a list of trips and returns a dictionary where keys are days of week, and values
        are a list of times (hour of the day) people departed from a station. Very similar to weekday arrivals
        to dict function (above), which is a function that does the same thing except maps arrivals.

            Parameters:
                list_of_trip_objects (list): List of Trip objects.
                var2 (type): desc.

            Returns:
                return weekday_dict (dict): Dictionary where keys are days of week, vals are list of departure times.
                                            Keep in mind weekdays are integers, where monday is indexed as 0. 

            ex. format:
            {
                0: [12:00, 1:32, 3:04, 4:21],
                1: [13:24, 1:10, 13:02, 21:02]
                ...
            }
        '''
        for trip in list_of_trip_objects:
            this_weekday = trip.weekday
            if this_weekday not in list(weekday_dict.keys()):
                weekday_dict[this_weekday] = [trip.stoptime.split(" ")[1]]
            else:
                weekday_dict[this_weekday].append(trip.stoptime.split(" ")[1])
        return weekday_dict

    def datestr_to_dayint(self, date):
        '''
        This function determines the day of week a date string occured on by converting to a datetime object
        and using the datetime.weekday function.

            Parameters:
                date (str): This parameter represents the date in dd/mm/yy T: 00:00:00 format

            Returns:
                'missing date' if trip data is missing date
                day of week (int): day of the week of an object if trip data is not missing date (0 = Monday ... 6 = Sunday)
        '''
        try:
            datetime_obj = parser.parse(date)
            return datetime_obj.weekday()
        except:
            return 'missing date'

@dataclass
class Weekday:
    """This is a dataclass that """
    weekday : int
    arrivals : list
    departures : list
        


def sort_by_stations(station_ids, Trip_list):
    '''
    Summary.

        Parameters:
            var1 (type): desc.
            var2 (type): desc.

        Returns:
            return var (type): desc.
    '''
    master_to = []
    master_from = []
    for station in station_ids:
        master_to += [i for i in Trip_list if i.toid == station]
        master_from += [i for i in Trip_list if i.fromid == station]
    return master_to, master_from



def group_weekdaydict_by_station(Trip_list):
    neighborhood_weekday_dict = {}
    for key, val in station_dict.items():
        neighborhood_weekday_dict[key] = triplist_to_weekdayobjectlist(val, Trip_list)
    return neighborhood_weekday_dict

def dayint_to_daystr(day_of_week):
    week_dict =  { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 
        3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday' }
    return week_dict[day_of_week]


def triplist_to_weekdayobjectlist(station_ids, Trip_list):

        station_trip_list = sort_by_stations(station_ids, Trip_list)
        
        to_dict = Trip.weekday_arrivals_todict(station_trip_list[0])
        from_dict = Trip.weekday_departures_todict(station_trip_list[1])

        to_dates = list(to_dict.keys())
        from_dates = list(from_dict.keys())

        unique_to_arrivals = [i for i in to_dates if i not in from_dates]

        shared_dates = [i for i in to_dates if i not in unique_to_arrivals]
        
        weekday_object_list = []
        
        for i in shared_dates:
            weekday_object_list.append(Weekday(i, to_dict[i], from_dict[i]))
        return weekday_object_list
