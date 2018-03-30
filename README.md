# Google Location History Heatmap
By Nicholas Knezek
September 2014


This code uses location history data from google.com/locationhistory .
In it’s current form, you must go to the website and download your kml location history for each 30 day period. 

1. visit google.com/locationhistory and download the .kml file.

2. copy and past the rows of location data from the kml files together. (all the ‘when’ and ‘gx:coord’ lines) into one .kml file.

3. Then, use KML2CSV to convert the KML data into a plain cdv files including the date, time, latitude and longitude data. 

4. run “makegheatmap.py” which uses functions written in “heatmap.py” to produce a javascript webpage. 

5. Open the html file that “makegheatmap.py” created in a web-browser with internet access. This webpage overlays a heat map of location points onto data from google maps and allows you to adjust parameters using the buttons across the top of the webpage window.

LocationHistory.py includes additional functions the play around with the data. 

## Examples

A large global overview of my location in 2014
![overview](https://github.com/nknezek/location_history_heatmap/blob/master/pictures/nation.png)

And a zoomed-in track history of a trip to Lake Tahoe
![tahoe](https://github.com/nknezek/location_history_heatmap/blob/master/pictures/tahoe.png)
