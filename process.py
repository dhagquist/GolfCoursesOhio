import csv, urllib, json

"""
About:
This program performs address lookup using the business name and its lat/lon coordinates via the Google Places API.
(Lat/lon coordinates can be generated in QGIS using the MMQGIS geocoding plugin.)

Input:
Data file with the following row structure:
| X | Y | NAME | ...
where X and Y are longitude and latitude coordinates respectively.

Process:
-In order to get a full address, Google Places API requires a PID (place ID), therefore two API calls are needed:
 One to get the PID (based on the lat/lon) and another using the PID to get the full address

Notes:
-Check for duplicates (handle in spreadsheet)
-Split address field (handle in spreadsheet)

# Example call to Places API (nearby search):
# https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.1173337,-82.4035978&radius=500&&keyword=trout club&key=AIzaSyCo0LreTVp0UAW-eiYj9UWwkL5udHZ7ckQ

# Example call to Places API (details):
# https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJk_RFwMY8OIgRPc6Uf2HMoyA&key=AIzaSyCo0LreTVp0UAW-eiYj9UWwkL5udHZ7ckQ

github.com/dhaqguist

"""

f = open('data10.csv')
csv_f = csv.reader(f)

lat, lon, name, pid = "", "", "", ""
found, not_found = [], []

key = "AIzaSyCo0LreTVp0UAW-eiYj9UWwkL5udHZ7ckQ"

for row in csv_f:
  
  # Get lat, lon, name from CSV file
  lat = row[1]
  lon = row[0]
  name = row[2]

  try:
    
    # Get Place ID (PID)
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat + "," + lon + "&radius=500&&keyword=" + name + "&key=" + key
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    # Check if daily query limit has been reached
    if "OVER_QUERY_LIMIT" in data.values():
      print "Daily API query limit reached. Please try again later or with a different key."
      break
    pid = str(data["results"][0]["place_id"])
    

    # Get details based on PID
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + pid + "&key=" + key
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    # Check if daily query limit has been reached
    if "OVER_QUERY_LIMIT" in data.values():
      print "Daily API query limit reached. Please try again later or with a different key."
      break
    address = str(data["result"]["formatted_address"])

    print lat, lon, name, "...Success"
    
    # Append address to row and append row to found list
    row.append(address)
    found.append(row)

  except:
    
    print lat, lon, name, "...Failed"
    not_found.append(row)


# Write found list to new CSV file
with open('data_final10.csv', "wb") as csv_file:
  writer = csv.writer(csv_file, delimiter=',')
  for f in found:
    writer.writerow(f)

# Write not found list to CSV file
with open('data_not_found10.csv', "wb") as csv_file:
  writer = csv.writer(csv_file, delimiter=',')
  for nf in not_found:
    writer.writerow(nf)
