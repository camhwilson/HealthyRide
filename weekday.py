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
    
    def station_data_to_weekday_dict(station_dict):
        neighborhood_weekday_dict = {}
        for key, val in station_dict.items():
            neighborhood_weekday_dict[key] = Weekday.triplist_to_weekdayobjectlist(val)
        return neighborhood_weekday_dict