import googlemaps
import time
import json
import pprint
import csv

locationToSearch='2.965670, 101.750908'
locationRadius=50000
def getApiKey():
    f = open("c:\\temp\\googleplacekey.txt","r")
    return f.read()

API_KEY = getApiKey()
_mapsvc = googlemaps.Client(API_KEY)
#my_fields = ['name','formatted_phone_number','website','rating','formatted_address']
#my_fields = ['rating', 'international_phone_number', 'geometry', 'permanently_closed', 'alt_id', 'review', 'formatted_address', 'formatted_phone_number', 'address_component', 'adr_address', 'website', 'type', 'scope', 'plus_code', 'icon', 'name', 'id', 'opening_hours', 'url', 'vicinity', 'utc_offset', 'place_id', 'price_level']
my_fields = None

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

def appendToCsv(p):
    #print(p)
    with open('c:\\temp\\place_file.csv', mode='a') as place_file:
        place_writer = csv.writer(place_file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        pprint.pprint(p.values())
        place_writer.writerow(p.values())
    place_file.close()

def processQuery(query):
    for place in query['results']:
      try:
          my_place_id = place['place_id']
          places_details  = _mapsvc.place(place_id= my_place_id, fields= my_fields)
          appendToCsv(places_details['result'])
      except Exception as e:
          pprint.pprint("ERROR " + e)
      time.sleep(2)

def process():
    result = _mapsvc.places_nearby(location=locationToSearch, radius=locationRadius)
    processQuery(result)

    if 'next_page_token' in result.keys():
      nextpagetoken = result['next_page_token']
      time.sleep(2)
    else:
      nextpagetoken = ''

    while nextpagetoken != '':
      try:
        result = _mapsvc.places_nearby(location=locationToSearch, radius=locationRadius, page_token=nextpagetoken)
        processQuery(result)
        if 'next_page_token' in result.keys():
          nextpagetoken = result['next_page_token']
        else:
          nextpagetoken = ''
          print('done')
      except Exception as e:
        print(e)
      time.sleep(2)

def main():
    process()

main()
