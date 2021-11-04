
import matplotlib.pyplot as plt
from weekday_analytics.weekday import dayint_to_daystr
import matplotlib.dates as mdates
from neighborhood_analytics.neighborhood import Neighborhood
from trip import Trip
import datetime
from collections import OrderedDict

class Neighborhood_Plot:

    def __init__(self, Trip_list):
        arrivals_by_neighborhood, departures_by_neighborhood = Neighborhood.sort_direction_neighborhood_weekday_hour(Trip_list)

        self.tuple_dict = self.combine_dicts(arrivals_by_neighborhood, departures_by_neighborhood)       


    #function that zips two dictionaries by identical key

    def combine_dicts(self, arrival_dict, departure_dict):
        #order matters, arrivals are first index of tuple, departures follow
        return_dict = {}
        for key in arrival_dict.keys():
            return_dict[key] = (arrival_dict[key], departure_dict[key])
        return return_dict


    def make_keys_int(self, d):
        return_dict = {}
        for key in d.keys():
            return_dict[int(key)] = d[key]
        return return_dict

    def order_nested_dict(self, nested_dict):
        return_dict = {}

        for key, val in OrderedDict(sorted(nested_dict.items())).items():
            nested_dict = self.make_keys_int(val)

            return_dict[key] = OrderedDict(sorted(nested_dict.items()))
        return return_dict



    def plot_hours_of_day(self, ax, day_of_wk, daily_dict):
        x = list(range(0, 24))

        x = [datetime.datetime.strptime(str(i),'%H') for i in x]

        for key, val in daily_dict.items():

            ax[day_of_wk].title.set_text((dayint_to_daystr(day_of_wk)))

            ax[day_of_wk].xaxis.set_major_locator(plt.MaxNLocator(6))
            ax[day_of_wk].xaxis.set_major_formatter(mdates.DateFormatter("%I"))

            ax[day_of_wk].plot(x, val)

            ax[day_of_wk].set_xlabel('Hour of Day')
            #ax.plot(x, val)

        ax[0].set_ylabel('4-year Arrival/Departure Volume')



    def return_arrival_daily_dict(self, ordered_arrivals, neighborhoods):
        arrival_daily_dict = {}
        for day, val in ordered_arrivals.items():
            neighborhood_dict = {}
            for key, val in val.items():       
                for i in neighborhoods:
                    if i not in neighborhood_dict.keys():
                        neighborhood_dict[i] = [val[i]]
                    else:
                        neighborhood_dict[i] += [val[i]]
            arrival_daily_dict[day] = neighborhood_dict
        return arrival_daily_dict

    def return_departure_daily_dict(self, ordered_departures, neighborhoods):    
        departure_daily_dict = {}
        for day, val in ordered_departures.items():
            neighborhood_dict = {}
            for key, val in val.items():       
                for i in neighborhoods:
                    if i not in neighborhood_dict.keys():
                        neighborhood_dict[i] = [val[i]]
                    else:
                        neighborhood_dict[i] += [val[i]]
            departure_daily_dict[day] = neighborhood_dict
        return departure_daily_dict

    def plot_daily_dict(self, direction_statement, neighborhood, daily_dict):
        fig, axs = plt.subplots(1, 7, figsize=(20,3), sharey = True)

        for key, val in daily_dict.items():
        #note that at some point here arrivals are flipped with departures

            self.plot_hours_of_day(axs, key, val)


        fig.suptitle(direction_statement + ' ' + neighborhood)
    ### changed from arrival_daily_dict[0]
        fig.legend(daily_dict[0].keys(), bbox_to_anchor=(1, 0.84))

        fig.subplots_adjust(top=0.8)

    def main_plot(self):
        neighborhoods = self.tuple_dict.keys()

        for key, val in self.tuple_dict.items():
            arrivals, departures = val

            ordered_arrivals = self.order_nested_dict(arrivals)
            ordered_departures = self.order_nested_dict(departures)

            arrival_daily_dict = self.return_arrival_daily_dict(ordered_arrivals, neighborhoods)
            departure_daily_dict = self.return_departure_daily_dict(ordered_departures, neighborhoods)

            self.plot_daily_dict('Arrivals to', key, arrival_daily_dict)
            self.plot_daily_dict('Departures from',  key, departure_daily_dict)