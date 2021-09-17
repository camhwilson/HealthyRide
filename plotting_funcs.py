import matplotlib.pylab as plt
from collections import Counter


import datetime
import matplotlib.dates as mdates

from trip_and_weekday import dayint_to_daystr

def hourly_volume(li):
    hourly_list = sorted([int(i.split(':')[0]) for i in li])
    counted_vals = Counter(hourly_list)
    new_dict = {}
    for key, val in counted_vals.items():
        new_key = datetime.datetime.strptime(str(key),'%H')
        new_dict[new_key] = val
    return new_dict

def individual_plot(da, dd, ax, i):
    plt.locator_params(axis='x', nbins=6)
    
    listsa = sorted(da.items()) # sorted by key, return a list of tuples
    listsd = sorted(dd.items()) # sorted by key, return a list of tuples
    
    xa, ya = zip(*listsa) # unpack a list of pairs into two tuples
    xd, yd = zip(*listsd)

    
    ax[i].plot(xa, ya, "g-", label = 'Arrivals')
    ax[i].plot(xd, yd, 'r-', label = 'Departures')

    ax[i].set_xlabel('Hour of Day')

    ax[i].xaxis.set_major_locator(plt.MaxNLocator(6))

    ax[i].title.set_text((dayint_to_daystr(i)))


    if i == 0:
        ax[i].set_ylabel('4-year Arrival/Departure Volume')

    ax[i].xaxis.set_major_formatter(mdates.DateFormatter("%I"))
    

def plot_days_of_wk(weekday_object_list, neighborhood_str):
    
    weekday_object_list.sort(key=lambda x: x.weekday, reverse=True)
    
    fig, axs = plt.subplots(1, 7, figsize=(15,2.5), sharey = True)
    fig.suptitle(neighborhood_str)

    for i, val in enumerate(weekday_object_list):
        
        arrivals_volume = hourly_volume(weekday_object_list[val.weekday].arrivals)
        departures_volume = hourly_volume(weekday_object_list[val.weekday].departures)
        individual_plot(arrivals_volume, departures_volume, axs, i)
    
    fig.legend(["Arrivals", "Departures"], bbox_to_anchor=(0.2, 1.1))
    fig.subplots_adjust(top=0.7)
    
    plt.show()

def plot_all(neighborhood_weekday_dict):
    for key, val in neighborhood_weekday_dict.items():
        plot_days_of_wk(val, key)