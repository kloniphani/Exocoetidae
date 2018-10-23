"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       December 06, 2017
Copyright:  2017 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""
#PACKAGES
#Object Oriented Classes
from Clustering.Distribution import *
from Clustering.Model import *
from Clustering.Display import *
from Object.Node import *
from Object.Provider import *
from Source.API import *

#Third Party Classes
from numpy import * 
from geopy import distance #Geo Location
import json, io, datetime, progressbar, csv
from xml.etree import ElementTree

class Nodes(object):
	"""description of class"""

	def __init__(self, **kwargs):
		self.__PROVIDER = None;
		self.__NODES = {}; self.__NETWORK = {}; self.__RECJECTED = []; self.CHAIN = {}; self.__UNUSSIGNED = []; self.__DATA = {};
		self.ClusterRadius = None; self.MaximumClusterHeads = None; 
		self.DroneCoverageRadius = [0.09043710000157064, 0.08983170000155323];
		self.Minimum_SNR = 0; self.Maximum_SNR = 0;
		self.ResidualEnergy_Median = 0;
		return super().__init__(**kwargs)

	def Network(self):
		NODES = {}; NETWORK = {}; UNUSSIGNED = []; DATA = {};
		if len(self.__NODES) > 0:
			for key, value in self.__NODES.items():
				NODES[key] = value
		
		if len(self.__NETWORK) > 0:
			for key, value in self.__NETWORK.items():
				NETWORK[key] = value

		if len(self.__UNUSSIGNED) > 0:
			for key in self.__UNUSSIGNED:
				UNUSSIGNED.append(key)

		if len(self.__NETWORK) > 0:
			for key, value in self.__DATA.items():
				DATA[key] = value

		return NODES, NETWORK, UNUSSIGNED, DATA;

	def CreateNodes(self, FileName, Place = None, ServiceProvider = None, Results = False, ClusterRadius = None):
		"""
		"""

		#Loading Json Geo Data from Google cloud
		with io.open(FileName, 'r', encoding="utf-8") as JsonData:
			JsonGeoData = json.load(JsonData)

			if ClusterRadius is not None: self.ClusterRadius = ClusterRadius;

			ResidualEnergies, SNRs = Distribution.Normal() #Loading Normal Distributed Random Values

			#Initialising the Provider
			if ServiceProvider is None:
				self._PROVIDER = Provider(Address = "" + Place + ", South Africa")

			#Creating Nodes from Google data
			if Results is True:	print("{0:3} {1:70} {2:27s} {3:3s}".format(
			'ID', 'NAME', 'RESIDUAL ENERGY', 'SNR'))
			for key, value in JsonGeoData.items():
				self.__NODES[key] = Node(Id = key, Name = value['name'], Position = [value['geometry']['location']['lng'], value['geometry']['location']['lat']], SNR = random.choice(SNRs), RE = random.choice(ResidualEnergies))
				if Results is True: 
					print("{0:4} {1:70} {2:15f} {3:15f}".format(self.__NODES[key].Id, self.__NODES[key].Name, self.__NODES[key].ResidualEnergy, self.__NODES[key].SNR))

			#Sorting the Nodes in Descending order based on their SNR
			TEMP = list(self.__NODES.values());
			TEMP.sort(key = lambda node: node.SNR, reverse = True) 

			self.__UNUSSIGNED = [node.Id for node in TEMP]

			self.Minimum_SNR = TEMP[-1].SNR
			self.Maximum_SNR = TEMP[0].SNR
			self.Deviation_SNR = std([node.SNR for node in TEMP])
			self.Average_SNR = average([node.SNR for node in TEMP])

			self.Median_ResidualEnergy = median([node.ResidualEnergy for node in TEMP])
			self.Average_ResidualEnergy = average([node.ResidualEnergy for node in TEMP])
			self.Maximum_ResidualEnergy = max([node.ResidualEnergy for node in TEMP])
			#self.MaximumClusterHeads = int(ceil(abs(len(self.__NODES)/sqrt(abs(self.Maximum_SNR - self.Minimum_SNR)))))
			self.MaximumClusterHeads = int(ceil(abs(len(self.__NODES) * (self.Minimum_SNR/self.Maximum_SNR))))

			print('Total: {0:3}\tMedian: {1:10f}\tMinimum: {2:10f}\tMaximum {3:10f}\tPossible Nodes: {4:10f}'.format(len(self.__NODES), float(median([node.SNR for node in TEMP])), self.Minimum_SNR, self.Maximum_SNR, self.MaximumClusterHeads))

if __name__ == '__main__':
	import time

	Place = 'Dummy'
	Heads = [] #To store computed number of Cluster Heads
	Unussigned = [] #To store number of nodes not connected
	
	print("#01: Creating Nodes!\n")
	ServiceProvider = Provider(Id = '00', Address = "" + Place + ", South Africa", Position = [-23.829150, 30.142595,10])
	Network = Nodes()
	Network.CreateNodes('./Source/Data/' + Place + '.json', Place, ClusterRadius = 0.5, ServiceProvider = ServiceProvider, Results = True)

	#MODELS
	print("\n#02: Running Models!\n")
	Technique = 'Greedy';	Distribution = 'Uniform'
	NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
	NODES, NETWORK, UNUSSIGNED, DATA = Model.Greedy(NODES, NETWORK, UNUSSIGNED, DATA)
	Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	#Display.MapNetwork(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	CHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
	Display.SaveToCSV(NODES, NETWORK, Technique); Display.SaveTopology(NODES, NETWORK, Technique, Links = True); Display.SaveRouting(NODES, NETWORK, Technique);
	NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();


	print('\n\n-----DONE-----')