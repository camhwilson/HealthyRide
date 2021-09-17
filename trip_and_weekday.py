from dateutil import parser

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
    
    def weekday_arrivals_todict(list_of_trip_objects):
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
        for trip in list_of_trip_objects:
            this_weekday = trip.weekday
            if this_weekday not in list(weekday_dict.keys()):
                weekday_dict[this_weekday] = [trip.stoptime.split(" ")[1]]
            else:
                weekday_dict[this_weekday].append(trip.stoptime.split(" ")[1])
        return weekday_dict

    def datestr_to_dayint(self, date):
        try:
            datetime_obj = parser.parse(date)
            return datetime_obj.weekday()
        except:
            return 'missing date'

class Weekday:
    def __init__(self, weekday, arrivals = [], departures = []):
        self.weekday = weekday
        self.arrivals = arrivals
        self.departures = departures


def sort_by_stations(station_ids, Trip_list):
    master_to = []
    master_from = []
    for station in station_ids:
        master_to += [i for i in Trip_list if i.toid == station]
        master_from += [i for i in Trip_list if i.fromid == station]
    return master_to, master_from



def station_data_to_weekday_dict(station_dict, Trip_list):
    neighborhood_weekday_dict = {}
    for key, val in station_dict.items():
        neighborhood_weekday_dict[key] = triplist_to_weekdayobjectlist(val, Trip_list)
    return neighborhood_weekday_dict

def dayint_to_daystr(day_of_week):
    week_dict =  { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 
        3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday' }
    return week_dict[day_of_week]


def triplist_to_weekdayobjectlist(station_ids, Trip_list):
        print('trip list exists in tltwol ' + str(len(Trip_list)))

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