# Repository Overview

Almost every city has a bike ridesharing service. In New York it's Citibike, in Chicago it's Divvy, in Pittsburgh it's HealthyRide. One late night in <em> the 'Burgh </em> I was riding home after a night out with the fellas on one of these bikes and wondered "how many other people have made this journey at this hour?"

This question formed the premise of this project.

Which neighborhoods are people coming from, and where are they going to? Which hours of the days see spikes in arrivals? Which see spikes in departures? Which neighborhoods did people use these bikes the most? Which use them the least?

# <em> Key Files </em>

## 1. <strong> resource_consolidation.py </strong>
 
All of the data this project runs off of can be found on Pittsburgh's public data store. It's free. The data is stored in silos by economic quarter, these silos are reffered to as <em> resources</em> by the data service.This data can be easily accessed by identifying the resource id's that correspond to the various economic quarters, and using the resouce id's to form the endpoint you insert into the request header.

This is what class Resource in resource_consolidation.py does. Once instantiated, you run a function called "create_json" that creates a list of all resource id's found at the base url, and iterates through one by one extracting data from them. Once you have iterated through all of the resources listed on the page, function returns a list of json objects. This can be easily translated into a Json file which can live on your computer when you're developing.
 
 The data in this JSON format is as follows.

"

{<span style="color:salmon">'Trip id'</span>: '60100515',

<span style="color:salmon">'Bikeid'</span>: '70332',

<span style="color:salmon">'To station name'</span>: 'S 12th St & E Carson St', 

<span style="color:salmon">'Usertype'</span>: 'Customer', 

<span style="color:salmon">'Stoptime'</span>: '10/1/2018 0:17', 

<span style="color:salmon">'From station name'</span>: 'First Ave & Smithfield St', 

<span style="color:salmon">'Starttime'</span>: '10/1/2018 0:00', 

<span style="color:salmon">'To station id'</span>: '1049', 

<span style="color:salmon">'Tripduration'</span>: '1017', 

<span style="color:salmon">'_id'</span>: 1, 

<span style="color:salmon">'From station id'</span>: '1003'}

"

I created a custom data type based on this format that is hosted in trip.py, the next important file I'll walk you through.
</p>

## 2. <strong> trip.py </strong>
In order to preform the types of operations I wanted to on the data, I decided to create a custom data type (class), a "Trip". This data type is based on the json format the api stores the data in, but adds a few attributes onto the end. Here are a list of the addributes, as they would appear for the trip shown above.

<em>Attributes assigned at time on initialization: </em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">tripid</span> = '60100515' <em> --> A unique identifying string of the trip </em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">bikeid</span> = '70332' <em> -->  A unique identifying ID of the bike</em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">toname</span> = 'S 12th St & E Carson St' <em> --> The name of the station the bike left from</em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">usertype</span> = 'Customer' <em> --> The type of customer (Customer vs. User) </em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">stoptime</span> = '10/1/2018 0:17' <em> --> The time, in datetime format, the trip ended </em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">fromname</span> = 'First Ave & Smithfield St' <em> --> The name of the station the bike ended its trip at  </em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">starttime</span> = '10/1/2018 0:00' <em> --> The time, in datetime format, the trip began </em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">toid</span> = '1049' <em> --> The unique identifying ID of the station the trip ended at </em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">tripduration</span> = '1017' <em> --> The duration of the trip, in seconds </em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">_id</span> = 1 <em> -->  The nth trip</em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">fromid</span> = '1003' <em> --> The unique identifying ID of the station the trip began at </em>

<em>Attributes assigned post-initialization:</em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">weekday</span> = 0 <em> -->  Calculated using the start time of the trip, this attribute returns the day of week in integer form. 0 = Monday.</em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">start_neighborhood</span> = 'Downtown' <em> -->  The neighborhood the trip began in, calculated using the station dictionary defined on the same file. This dictionary clumps station ID's by neighborhoods I defined</em>

<span style="color:indianred">Trip.</span><span style="color:lightsalmon">end_neighborhood</span> = 'Southside Flats' <em> -->  The neighborhood the trip ended in, calculated using the station dictionary defined on the same file. This dictionary clumps station ID's by neighborhoods I defined</em>

As you can see, this datatype was built to expand. When I go to build on the project by analyzing it in a different way, I usually beign the project by adding a post-initialization attribute that I use to expand the project. I've found it is much easier to measure attributes as far up-stream as possible, and everything begins here.

If you want to contribute to this project and begin with exploratory analysis, the best way to do so is to creat a list of these trip objects. You can then sort and filter these lists using list comprehension and begin to draw conclusions.


## 3. <strong> analytics.ipynb </strong>

analytics.ipynb is where I feature all of the visualizations that support my project. So far, they are as follows.

1) Weekday Analytics - plots that display patterns of arrivals and departures by neighborhood
![Downtown Arrivals and Departures](/supporting_figures/downtown.png)
2) Neighborhood Analytics - similar to Weekday Analytics but more complicated - plots that display patterns of arrivals and departures from and to neighborhoods
![Downtown Arrivals by Neighborhood](/supporting_figures/arrivals_to_downtown.png)
![Downtown Departures by Neighborhood](/supporting_figures/departures_from_downtown.png)
You may notice that these visualizations correspond to folders in this repository. This is the way I have chosen to structure the repository. Folders within the main repository contain logic that is specific to a visualization. Files that exist outside these folders are there for a reason-  they apply across visualizations.

# <em> If you want to contribute </em>
Want to contribute? This is how I invision it will work.

1) Read the above (lol). You will need a really good working understanding of how to create a copy of the data on your computer, and how I've structured "the trip" datatype.
2) After you clone the project, you'll want to create your own branch.
3) Configure filepaths inside "sys.insert()" arguments. I want this eventually to configure automatically, this is an area for improvement in the repo. Maybe I will revisit it someday.
4) After the filepaths have been configured, everything on the repository should be in working order. Run <em>api_data_to_json.ipynb</em> to create a copy of the data locally on your computer. You will see this file pop up in your directory as "<em>data.json</em>".
5) Once you have a working copy of the data on your computer, you are set to begin exploratory analysis. You should preform this in <em>exploratory_analysis.py</em>, which is already set to read the <em>data.json</em> file you just created.
6) When you have an idea of a point you want to prove through visualization, create a folder. I've done the majority of my development in jupyter notebooks and translated those files into regular python files, but you may have a different workflow.
7) Push the branch! I'll review changes and feature your visualiation in analytics.ipynb