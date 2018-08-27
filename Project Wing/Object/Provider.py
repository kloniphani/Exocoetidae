"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       September 29, 2017
Copyright:  2017 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""

#PACKAGES
import googlemaps
from numpy import *
from geopy import Nominatim, distance
from Source import API as api

class Provider(object):
	"""description of class"""

	#INITIALISERS
	def __init__(self, Id = None, Address = None, RE = None, Position = None):
		#SERVICE PROVIDER IDENTITY
		self.Id = Id; self.Name = "NULL";
		self.MEMBERS = []

		#NETWORK INFORMATION
		self.Gt = 200 #dBi
		self.Gr = 120 #dBi
		self.Pt = 180 #dBm
		self.Frequency = 5e5
		self.Channel = 1

		#TELEMETRY		
		self.ResidualEnergy = random.choice(random.normal(124000, 0.1, 100000))
		if RE is not None:
			self.ResidualEnergy = RE

		#COMPUTING THE NODE'S LOCATION
		self.gmaps = googlemaps.Client(key = api.Google().Geocoding)
		self.Height = 15000

		if Address is None:
			self.Geocode = self.gmaps.reverse_geocode((Position[0], Position[1]))[0] 
			self.Address = self.Geocode['formatted_address']
			print("Address: {}\tPosition{}".format(self.Address, Position))
		else:
			self.Address = Address;			

		if Position is None:		
			self.Geocode = self.gmaps.geocode(Address)[0] 
			self.Position = [self.Geocode['geometry']['location']['lat'], self.Geocode['geometry']['location']['lng'], self.Height]
		else:
			self.Position = Position