from dateutil import parser
from dataclasses import dataclass


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
