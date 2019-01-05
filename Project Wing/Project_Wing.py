"""         
Authors:     Kloni Maluleke (Msc), kloniphani@gmail.com
Date:        December 06, 2017
Copyrights:  2017 ISAT, Department of Computer Science
             University of the Western Cape, Bellville, ZA
"""
#PACKAGES
#Object Oriented Classes
from Clustering.Distribution import *
from Clustering.Model import *
from Clustering.Display import *
from Clustering.Backbone import *
from Clustering.Multisink import *
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
		self.Median_ResidualEnergy = 0;
		return super().__init__(**kwargs)

	def Network(self):
		NODES = {}; NETWORK = {}; UNASSIGNED = []; DATA = {};
		if len(self.__NODES) > 0:
			for key, value in self.__NODES.items():
				NODES[key] = value
		
		if len(self.__NETWORK) > 0:
			for key, value in self.__NETWORK.items():
				NETWORK[key] = value

		if len(self.__UNUSSIGNED) > 0:
			for key in self.__UNUSSIGNED:
				UNASSIGNED.append(key)

		if len(self.__NETWORK) > 0:
			for key, value in self.__DATA.items():
				DATA[key] = value

		return NODES, NETWORK, UNASSIGNED, DATA;

	def CreateNodes(self, FileName, Place = None, Code = None, ServiceProvider = None, Results = False, ClusterRadius = None):
		"""
		"""

		#Loading Json Geo Data from Google cloud
		with io.open(FileName, 'r', encoding="utf-8") as JsonData:
			JsonGeoData = json.load(JsonData)

			if ClusterRadius is not None: self.ClusterRadius = ClusterRadius;

			ResidualEnergies, SNRs = Distribution.Distribution.Normal() #Loading Normal Distributed Random Values

			#Initialising the Provider
			if ServiceProvider is None:
				self._PROVIDER = Provider(Address = "" + Place + ", South Africa")

			#Creating Nodes from Google data
			if Results is True:	print("{0:3} {1:70} {2:27s} {3:3s}".format(
			'ID', 'NAME', 'RESIDUAL ENERGY', 'SNR'))
			Counter = 1
			for k, value in JsonGeoData.items():
				key = str(Counter);
				if Code != None and Code not in value['formatted_address']:
					continue;
				if 'links' in value.keys():
					self.__NODES[key] = Node(Id = key, Name = k, Position = [value['geometry']['location']['lng'], value['geometry']['location']['lat']], SNR = random.choice(SNRs), RE = random.choice(ResidualEnergies), MeshNetwork = value['links'])
				else:
					self.__NODES[key] = Node(Id = key, Name = value['name'], Position = [value['geometry']['location']['lng'], value['geometry']['location']['lat']], SNR = random.choice(SNRs), RE = random.choice(ResidualEnergies))
				if Results is True: 
					print("{0:4} {1:70} {2:15f} {3:15f}".format(self.__NODES[key].Id, self.__NODES[key].Name, self.__NODES[key].ResidualEnergy, self.__NODES[key].SNR))
				Counter += 1

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

	Place = 'SAPS'
	Code = '';

	Heads = [] #To store computed number of Cluster Heads
	Unassigned = [] #To store number of nodes not connected
	
	print("#01: Creating Nodes!\n")
	ServiceProvider = Provider(Id = '00', Address = "" + Place + ", South Africa", Position = [-23.829150, 30.142595,10])
	Network = Nodes()
	Network.CreateNodes('./Source/Data/' + Place + '.json', Place, Code = Code, ClusterRadius = 0.5, ServiceProvider = ServiceProvider, Results = True)

	#MODELS
	print("\n#02: Running Models!\n")
	Technique = 'Greedy';	Distribution = 'Normal'
	NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
	#NODES, NETWORK, UNASSIGNED, DATA = Model.Successive(NODES, NETWORK, UNASSIGNED, DATA)
	#NODES, NETWORK, UNASSIGNED, DATA = Backbone.GraphColouringWithHeightControl(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'UAV')
	NODES, NETWORK, UNASSIGNED, DATA = Multisink.GreedySinkNodeSelectionWithSinksTree(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'LAP')
	#Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius, Type = '2D')
	Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius, Type = 'TREE')

	NODES, NETWORK, UNASSIGNED, DATA = Multisink.BalanceTree(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'Hop')
	#Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius, Type = '2D')
	Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius, Type = 'TREE')
	
	#Display.MapNetwork(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	CH, ICH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
	#Display.DrawTreeGraph(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	#Display.SaveToCSV(NODES, NETWORK, Technique); Display.SaveTopology(NODES, NETWORK, Technique, Links = True); Display.SaveRouting(NODES, NETWORK, Technique);
	#NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();   

	print('\n\n-----DONE-----')