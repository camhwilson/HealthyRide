
class Weekday:
    #split into lists which group by day, then by hour
    @classmethod
    def group_trip_list_by_weekday(self, Trip_list):
        """function groups trip lists by weekday"""
        weekday_trip_dict = {}
        for i in Trip_list:
            if i.weekday not in weekday_trip_dict.keys():
                weekday_trip_dict[i.weekday] = [i]
            else:
                weekday_trip_dict[i.weekday] += [i]
        return weekday_trip_dict
    
    @classmethod
    def create_hourly_dict_grouped_by_weeks(self, Trip_list, func):
        """function takes master trip list and passes it through create weekday dict, 
        then creates nested dict with hourly volumes"""
        return_hourly_values = {}

        weekday_trip_dict = self.group_trip_list_by_weekday(Trip_list)  
        
        for key, val in weekday_trip_dict.items():
            return_hourly_values[key] = func(val)
        
        return return_hourly_values
