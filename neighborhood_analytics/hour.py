from collections import Counter

class Hour:
    @classmethod
    def group_trip_list_by_arrival_hour(self, Trip_list):
        """function groups trip lists by hour of day"""
        #print(len(filter_list_to_just_objects(Trip_list)[1]))
        hourly_trip_dict = {}
        trip_list_wo_dockless = self.drop_dockless_arrivals(Trip_list)
        
        for i in trip_list_wo_dockless:
            date = i.stoptime
            try:
                hour = date[date.find(' ')+len(' '):date.rfind(':')]
            except:
                #“dockless” trips are where a bike does not start or end at an official station, per healthyride documentation
                hour = 'dockless'

            if hour not in hourly_trip_dict.keys():
                hourly_trip_dict[hour] = [i.end_neighborhood]
            else:
                hourly_trip_dict[hour] += [i.end_neighborhood]
        
        return self.convert_hourly_trip_dict_to_counter(hourly_trip_dict)
    
    @classmethod
    def group_trip_list_by_departure_hour(self, Trip_list):
        """function groups trip lists by hour of day"""
        hourly_trip_dict = {}
        trip_list_wo_dockless = self.drop_dockless_departures(Trip_list)
        for i in trip_list_wo_dockless:
            date = i.starttime
            try:
                hour = date[date.find(' ')+len(' '):date.rfind(':')]
            except:
                #“dockless” trips are where a bike does not start or end at an official station, per healthyride documentation
                hour = 'dockless'
            
            if hour not in hourly_trip_dict.keys():
                hourly_trip_dict[hour] = [i.start_neighborhood]
            else:
                hourly_trip_dict[hour] += [i.start_neighborhood]
        return self.convert_hourly_trip_dict_to_counter(hourly_trip_dict)
    
    @classmethod
    def convert_hourly_trip_dict_to_counter(self, hourly_trip_dict):
        counted_hourly_neighborhoods = {}
        for key, val in hourly_trip_dict.items():
            counted_hourly_neighborhoods[key] = Counter(val)
        return counted_hourly_neighborhoods

    @classmethod
    def drop_dockless_departures(self, Trip_list):
        return [i for i in Trip_list if type(i.starttime) is not None]

    @classmethod
    def drop_dockless_arrivals(self, Trip_list):
        return [i for i in Trip_list if type(i.stoptime) is not None]