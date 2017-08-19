# GolfCoursesOhio
An interactive web-map of golf courses in Ohio.

I used QGIS' MMQGIS plugin to geocode a data set of Ohio golf courses (containing just the course name, city, and state). I coded process.py in order to obtain the PID (place ID) and the address details via Google's Places API.

From there I imported the refined data set back into QGIS and used the QGIS2Web plugin to create a web map. The map utilizes Leaflet for functionality and OpenStreetMaps for the basemap. 

![Screenshot](https://raw.githubusercontent.com/dhagquist/GolfCoursesOhio/master/screenshot.png)

You can find the raw data in CSV format in the data folder.
