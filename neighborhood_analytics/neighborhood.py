import sys

sys.path.insert(0, '/Users/cwilson/desktop/programming/jupyter_tings/healthyride/healthyride/neighborhood_analytics')

from hour import Hour
from weekday import Weekday

class Neighborhood:
    
    @classmethod
    def group_by_arrival_neighborhood(self, Trip_list):
        return_dict = {}
        for i in Trip_list:
            if i.start_neighborhood not in return_dict.keys():
                return_dict[i.start_neighborhood] = [i]
            else:
                return_dict[i.start_neighborhood].append(i)
        return return_dict
    
    @classmethod
    def group_by_departure_neighborhood(self, Trip_list):
        return_dict = {}
        for i in Trip_list:
            if i.end_neighborhood not in return_dict.keys():
                return_dict[i.end_neighborhood] = [i]
            else:
                return_dict[i.end_neighborhood].append(i)
        return return_dict

    @classmethod
    #apply group_by_arrival_neighborhood and group_by_departure_neighborhood first, then create hourly dict grouped by weeks
    
    def sort_direction_neighborhood_weekday_hour(self, Trip_list):
        neighborhood_by_arrivals = self.group_by_arrival_neighborhood(Trip_list)

        neighborhood_by_departures = self.group_by_departure_neighborhood(Trip_list)

#these are created correctly, something occurs below
        return_sorted_arrivals = {}

        for key, val in neighborhood_by_arrivals.items():
            return_sorted_arrivals[key] = Weekday.create_hourly_dict_grouped_by_weeks(val, Hour.group_trip_list_by_arrival_hour)

        return_sorted_departures = {}

        for key, val in neighborhood_by_departures.items():
            return_sorted_departures[key] = Weekday.create_hourly_dict_grouped_by_weeks(val, Hour.group_trip_list_by_departure_hour)

        
        return return_sorted_departures, return_sorted_arrivals

