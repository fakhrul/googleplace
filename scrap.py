import googlemaps
import time
import json
import pprint
import csv

API_KEY = 'AIzaSyAazCdclJEMO5XrsBPz2Ryfrj4c_BJmyts'
_mapsvc = googlemaps.Client(API_KEY)
my_fields = ['name','formatted_phone_number','website','rating']


def appendToCsv(p):
    print(p)
    with open('d:\place_file.csv', mode='a') as place_file:
        place_writer = csv.writer(place_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        place_writer.writerow(p.values())
    place_write.close()

def processQuery(query):
    for place in query['results']:
      try:
          my_place_id = place['place_id']
          places_details  = _mapsvc.place(place_id= my_place_id, fields= my_fields)
          pprint.pprint(places_details['result'])
          appendToCsv(places_details['result'])
      except:
          pprint.pprint("ERROR")

def process():
    result = _mapsvc.places_nearby(location='2.965670, 101.750908', radius=4000, type='cafe')
    processQuery(result)

    if 'next_page_token' in result.keys():
      nextpagetoken = result['next_page_token']
      time.sleep(2)
    else:
      nextpagetoken = ''

    while nextpagetoken != '':
      query = self._mapsvc.places_nearby(location='2.965670, 101.750908', radius=4000, type='cafe', page_token=nextpagetoken)
      result = query['results']
      for place in query['results']:
          try:
              my_place_id = place['place_id']
              #my_fields = ['name','formatted_phone_number','website']
              places_details  = _mapsvc.place(place_id= my_place_id )
              pprint.pprint(places_details['result'])
          except:
              pprint.pprint("ERROR")

      if 'next_page_token' in query.keys():
        nextpagetoken = query['next_page_token']
        time.sleep(2)
      else:
        nextpagetoken = ''

def main():
    process()

main()
