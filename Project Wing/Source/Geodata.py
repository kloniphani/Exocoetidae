"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       December 06, 2017
Copyrights:  2017 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""

from Source import API as api
import googlemaps
import time, json, io, sys

class Geodata(object):
	"""description of class"""

	def __init__(self, **kwargs):
		self.GMaps = googlemaps.Client(key = api.Google().JavaScript, timeout = 20)
		self.Counter = 1
		return super().__init__(**kwargs)

	def SearchPlaces(self, Places, Next = ''):
		return self.GMaps.places(query = Places, page_token = Next)

	def PopulateResults(self, Query = None, Location = "", Type = 'point_of_interest', Next = '', Results = False, Sleep = 5, FileName = None, OutputFile = False):
		Results = {}
		while True:
			try:
				PlaceResults = self.SearchPlaces(Query, Next = Next)
			except:
				print("! Error has occured - {0}".format(sys.exc_info()[0]))
				continue;
			else:	
				for Place in PlaceResults['results']:
					if (Place['formatted_address'].find("South Africa") or Place['formatted_address'] == 'South Africa'):
						if Type.lower() in Place['types']:
							if Location in Place['formatted_address']:
								print("---{0}".format(Place['formatted_address']))
								Results[str(Place['name'])] = Place
								if Results is True: print(Place);
								if OutputFile is True:
									self.WriteFile(FileName + ".txt", "{0:3} {1:70} {2:12f} {3:12f} \t{4}\n".format(self.Counter, Place['name'], Place['geometry']['location']['lat'], Place['geometry']['location']['lng'], Place['formatted_address']))
								self.Counter += 1; 				
			time.sleep(Sleep)

			if 'next_page_token' in PlaceResults.keys():
				Next = PlaceResults['next_page_token']
			else:
				break;

		return Results

	def SearchPlacesResults(self, Query = None, Type = '', Types = None, Places = None, Next = '', Results = False, Sleep = 1, FileName = None, OutputFile = False):
		SearchResults = {}
		if Types is not None and Places is not None:
			for Place in Places:
				for Type in Types:
					Query = Type + " in " + Place + ", South Africa"
					print(Query)
					FileName = "./Source/Data/Study/" + Place
					SearchResults.update(self.PopulateResults(Query = Query, Location = Place, FileName = FileName, Results = Results, OutputFile = True))
				
				if OutputFile is True:
					with open(FileName + ".json", 'w') as fp:
						json.dump(SearchResults, fp, indent = 4)
					fp.close()

				SearchResults.clear()
				self.Counter = 1;
		else:
			SearchResults.update(PopulateResults(Query = Query, Location = Place, FileName = FileName, Results = Results, OutputFile = True))
			if OutputFile is True:
				with open(FileName + ".json", 'w') as fp:
					json.dump(SearchResults, fp, indent = 4)
				fp.close()
		

		return SearchResults
	
	def WriteFile(self, FileName, Data):
		File = io.open(FileName, 'a+', encoding="utf-8")
		File.write(Data)
		File.close()

	def WriteGeodata(self, FileName, Query = None, Type = '', Next = '', Results = False):
		try:
			PlaceResults = self.SearchPlaces(Query, Next = Next)
		except ApiError as e:
			print(e)
		else:
			for Place in PlaceResults['results']:
				if Place['formatted_address'].find("South Africa") or Place['formatted_address'] == 'South Africa':
					if Type in Place['types']:
						self.WriteFile(FileName, "{0:3} {1:70} {2:12f} {3:12f}\n".format(self.Counter, Place['name'],
																		Place['geometry']['location']['lat'],
																		Place['geometry']['location']['lng']))
						self.Counter += 1; 
						if Results is True: print(Place);
		
		time.sleep(1)

		try:
			PlaceResults['next_page_token']
		except KeyError as e:
			self.Counter = 1; 
			print("Search Completed")
		else:
			self.WriteGeodata(FileName, Query = Query, Type = Type, Next = PlaceResults['next_page_token'])
		
if __name__ == '__main__':
	G = Geodata()
	#Type = ['Clinic','Health Centre', 'Hospital', 'Medical Centre', 'Health Care', 'Surgery', 'Police', 'SAPS', 'Court', 'Correction Services', 'Traffic Department', 'School', 'College', 'Academy', 'University', 'Store', 'Shop', 'Shopping Mall',	 'Church', 'Stadiums' 'Park', 'Mining', 'Farms']
	
	#Types = ['SAPS'], Places = ["Port Of Entry SAPS, Cape Town, Western Cape"]

	Type = ['School', 'College', 'Academy', 'University']
	#Place = ['Mopani District Municipality', 'Vhembe District Municipality', 'Waterberg District Municipality', 'Chris Hani District Municipality', 'Tzaneen', 'Lulekani', 'Zeerust', 'Duduza', 'Hlankomo', 'Mandileni', 'Gonono', 'Soweto', 'Khayelitsha, Cape Town']
	Place = ['Lulekani', 'Zeerust', 'Duduza', 'Hlankomo', 'Mandileni', 'Gonono', 'Soweto', 'Khayelitsha']
	#SearchQuery = "" + Type[0] + " in " + Place[4] + " , South Africa"
	#G.WriteGeodata(FileName = "./Source/Data/" + Type[0] + " - " + Place[4] + ".txt", 
	#				Query = SearchQuery,
	#				Type = Type[4].lower())
	#G.SearchPlacesResults(Query = SearchQuery, Type = Type.lower())
	G.SearchPlacesResults(Types = Type, Places = Place, OutputFile = True)