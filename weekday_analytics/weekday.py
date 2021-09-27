from dataclasses import dataclass

import sys
  
sys.path.insert(0, '/Users/cwilson/desktop/programming/jupyter_tings/healthyride/healthyride')

from trip import Trip

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
                        '1040', '1097', '1035', '1094', '49271'],
    
    'Squirrel Hill' : ['49251', '49261', '1068', '1069', '1070'],
    
    'Shadyside': ['1034', '1033', '1032', '1031']
}


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
