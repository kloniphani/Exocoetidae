"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       December 06, 2017
Copyright:  2017 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""
#PACKAGES
#Object Oriented Classes
from Clustering.Distribution import *
from xml.etree import ElementTree
from Clustering.Model import *
from Object.Node import *
from Object.Provider import *
from Source.API import *

#Third Party Classes
from numpy import * 
from geopy import distance #Geo Location
import json, io, datetime, progressbar, csv

#These packages are for ploting the graph
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

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

			ResidualEnergies, SNRs = Distribution.ChiSquare() #Loading Normal Distributed Random Values

			#Initialising the Provider
			if ServiceProvider is None:
				self._PROVIDER = Provider(Address = "" + Place + ", South Africa")

			#Creating Nodes from Google data
			if Results is True:	print("{0:3} {1:70} {2:27s} {3:3s}".format(
			'ID', 'NAME', 'RESIDUAL ENERGY', 'SNR'))
			for key, value in JsonGeoData.items():
				self.__NODES[key] = Node(Id = key, Name = value['name'], Position = [value['geometry']['location']['lat'], value['geometry']['location']['lng']], SNR = random.choice(SNRs), RE = random.choice(ResidualEnergies))
				if Results is True: 
					print("{0:4} {1:70} {2:15f} {3:15f}".format(self.__NODES[key].Id, self.__NODES[key].Name, self.__NODES[key].ResidualEnergy, self.__NODES[key].SNR))

			#Sorting the Nodes in Descending order based on their SNR
			TEMP = list(self.__NODES.values());
			TEMP.sort(key = lambda node: node.SNR, reverse = True) 

			self.__UNUSSIGNED = [node.Id for node in TEMP]

			self.Best_SNR = 2e-07
			self.Minimum_SNR = TEMP[-1].SNR
			self.Maximum_SNR = TEMP[0].SNR

			self.ResidualEnergy_Median = median([node.ResidualEnergy for node in TEMP])
			#self.MaximumClusterHeads = int(ceil(abs(len(self.__NODES)/sqrt(abs(self.Maximum_SNR - self.Minimum_SNR)))))
			self.MaximumClusterHeads = int(ceil(abs(len(self.__NODES) * (self.Minimum_SNR/self.Maximum_SNR))))

			print('Total: {0:3}\tMedian: {1:10f}\tMinimum: {2:10f}\tMaximum {3:10f}\tPossible Nodes: {4:10f}'.format(len(self.__NODES), float(median([node.SNR for node in TEMP])), self.Minimum_SNR, self.Maximum_SNR, self.MaximumClusterHeads))

class Display(object):
	"""description of class"""

	def PrintList(List):
		"""Helper function to print an item from a list one by one"""
		for item in List:
			print(item)

	def SaveToCSV(Nodes, Network, Name = None):
		if Name is not None:
			FileName = str(Name)

		with open('./Source/Topology/' + FileName + 'Nodes.csv', 'w', newline='') as fp:
			FieldNames = ['Id', 'Name', 'SNR', 'Energy', 'Position', 'Type']
			Writer = csv.DictWriter(fp, fieldnames=FieldNames)
			Writer.writeheader()
			for key, value in Nodes.items():
				Writer.writerow({'Id' : value.Id,
					'Name': value.Name,
					'SNR': value.SNR,
					'Energy': value.ResidualEnergy,
					'Position': value.Position,
					'Type': value.Type})
		fp.close()

		with open('./Source/Topology/' + FileName + 'Network.csv', 'w', newline ='') as fp:
			Writer = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)			
			for key, value in Network.items():
				Temp = [value.Id]
				Temp += [node.Id for node in value.MEMBERS]
				Writer.writerow(Temp)
		fp.close()
				
	def SaveTopology(Nodes, Network, Name = None, Links = False):
		FileName = ''
		if Name is not None:
			FileName = str(Name)
		
		with open('./Source/Topology/' + FileName + 'Topology.json', 'w') as fp:
			Data = {}; N = {}; L = [];
			N["P1"] = {} #Service Provider
			for key, value in Nodes.items():
				N["N" + key] = {
					"x": 6367.445 * cos(value.Position[1]) * cos(value.Position[0]),
					"y": 6367.445 * cos(value.Position[1]) * sin(value.Position[0]),
					"RE" : value.ResidualEnergy
					} 

			Data["nodes"] = N

			if Links is True:
				for key, value in Network.items():
					L.append({"from": "N" + value.Id, "to" : "P1", "SNR": value.SNR})
					for node in value.MEMBERS:
						L.append({"from": "N" + node.Id, "to" : "N" + value.Id, "SNR": node.SNR})

				Data["links"] = L

			json.dump(Data, fp, indent = 4)
		fp.close()


	def SaveRouting(Nodes, Network, Name = None):
		from lxml import etree

		FileName = ''
		if Name is not None:
			FileName = str(Name)

	
		Data = {}; N = {}; L = [];
		AccessPoint = 192 #Service Provider
		ClusterHead = 1;
		ClusterMember = 1;

			

		page = etree.Element('config')
		doc = etree.ElementTree(page)

		AccesPointAdreess = '192.0.0.0'

		etree.SubElement(page, 'interface', host='P1', address=AccesPointAdreess, netmask='255.x.x.x', addDefaultRoutes = 'false', addStaticRoutes ='false', addSubnetRoutes='false') 

		for key, value in Network.items():	
			ClusterHeadAddress = '' + str(AccessPoint) + '.' + str(ClusterHead) + '.0.0'

			for node in value.MEMBERS:
				etree.SubElement(page, 'interface', host='N' + node.Id, address=''+str(AccessPoint) + '.' + str(ClusterHead) + '.' + str(ClusterMember)+ '.x', netmask='255.255.255.0', addDefaultRoutes = 'false', addStaticRoutes ='false', addSubnetRoutes='false')
				etree.SubElement(page, 'route', host='N' + node.Id, destination=ClusterHeadAddress, netmask='255.255.255.0', gateway=ClusterHeadAddress)
				ClusterMember += 1;

			etree.SubElement(page, 'interface', host='N' + value.Id, address=ClusterHeadAddress, netmask='255.255.0.0', addDefaultRoutes = 'false', addStaticRoutes ='false', addSubnetRoutes='false')
			etree.SubElement(page, 'route', host='N' + value.Id, destination=AccesPointAdreess, netmask='255.255.0.0', gateway = AccesPointAdreess)
			ClusterHead += 1

		doc.write('./Source/Topology/' + FileName + 'Routing.xml', xml_declaration = True, pretty_print=True, encoding='utf-16')


	def SaveNetwork(Nodes, Network, Radius, Name = None):
		"""
		"""
		FileName = ''
		if Name is not None:
			FileName += str(Name)
		FileName += str('---' + datetime.datetime.now().strftime("%d-%m-%y--%H-%M"))
		plt.savefig('./Source/Results/' + FileName + "-R" + str(Radius) + '.png')

		with open('./GUI/Network/Network/static/data/Network.json', 'w') as fp:
			Temp = {}; 
			for key, value in Network.items():
				L = [node.Id for node in value.MEMBERS]
				Temp[key] = {'Id' : value.Id,
					'Name': value.Name,
					'SNR': value.SNR,
					'Energy': value.ResidualEnergy,
					'Position': value.Position,
					'MEMBERS': L,
					'Type': value.Type} 
			json.dump(Temp, fp, indent = 4)
		fp.close()

		with open('./GUI/Network/Network/static/data/Nodes.json', 'w') as fp:
			Temp = {}
			for key, value in Nodes.items():
				Temp[key] = {'Id' : value.Id,
					'Name': value.Name,
					'SNR': value.SNR,
					'Energy': value.ResidualEnergy,
					'Position': value.Position,
					'Type': value.Type} 
			json.dump(Temp, fp, indent = 4)
		fp.close()

	def SaveToExcel(Heads, Unussigned, ResidualEnergy_Median, Minimum_SNR, Maximum_SNR, FileName = None, SheetName = None, Counter = 0, Results = False):
		if FileName is None:
			FileName = './Model/Computed Data/Results.xlsx'

		if SheetName is None:
			SheetName = 'Results'

		Columns = ['', 'Minimum SNR', 'Maximum SNR', 'Median RE', 'Backhauling CH', 'Myopic CH', 'K-Means CH', 'Backhauling Unussigned', 'Myopic Unussigned', 'K-Means Unussigned']
		
		DATA = {}
		DATA[''] = Counter
		DATA['Minimum SNR'] = [Minimum_SNR]
		DATA['Maximum SNR'] = [Maximum_SNR]
		DATA['Median RE'] = [ResidualEnergy_Median]
		DATA['Backhauling CH'] = [Heads[0]]
		DATA['Myopic CH'] = [Heads[1]]
		DATA['K-Means CH'] = [Heads[2]]
		DATA['Backhauling Unussigned'] = [Unussigned[0]]
		DATA['Myopic Unussigned'] = [Unussigned[1]]
		DATA['K-Means Unussigned'] = [Unussigned[2]]
		
		DataFrames = pd.DataFrame(data = DATA, columns = Columns)  #Create a Pandas dataframe from some data.
		Writer = pd.ExcelWriter(FileName, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
		DataFrames.to_excel(Writer, startrow = len(DataFrames)+1, header = False, index=False, sheet_name=SheetName)
		Writer.save()

		if Results is True: print('RE: {0}\tMIN: {1}\tMAX: {2}\tHEADS: {3}\tUNUSSIGNED: {4}'.format(ResidualEnergy_Median, Minimum_SNR, Maximum_SNR, Heads, Unussigned))

	def DrawPoints(nodes = None, network = None, Name = None, Radius = '', Show = False, Save = False):
		"""Helper function that returns a figure with point attributes in an array for every cluster network"""
		
		fig = plt.figure()
		if Name is not None:
			fig.canvas.set_window_title(Name)
		figure = fig.add_subplot(111, projection = '3d')

		from itertools import cycle
		points = []; colors = cycle('rgbmcy')
	
		if network is not None and nodes is not None:
			with progressbar.ProgressBar(max_value = len(network)) as bar:
				count = 0
				for head in list(network.values()):
					figure.scatter(head.Position[0], head.Position[1], head.Position[2], c = 'k', marker = 'o', s = 50)
			
					color = next(colors)
		
					figure.scatter(head.Position[0], head.Position[1], head.Position[2], c = color, marker = 'o')
					figure.text(head.Position[0], head.Position[1], head.Position[2], head.Id)

					points.append(head.Id)					
					for leaf in head.MEMBERS:
						figure.scatter(leaf.Position[0], leaf.Position[1], leaf.Position[2], c = color, marker = 'o')
						figure.text(leaf.Position[0], leaf.Position[1], leaf.Position[2], leaf.Id)
			
						#Drawing a line in 3d
						spacing = 100
						xs = linspace(head.Position[0], leaf.Position[0], spacing)
						ys = linspace(head.Position[1], leaf.Position[1], spacing)
						zs = linspace(head.Position[2], leaf.Position[2], spacing)
						figure.plot(xs, ys, zs, c = color)

						points.append(leaf.Id)

					count += 1
					bar.update(count)
		
				color = 'k'
				for node in list(nodes.values()):
					if node.Id not in points:
						figure.scatter(node.Position[0], node.Position[1], node.Position[2], c = color, marker = 'o')
						figure.text(node.Position[0], node.Position[1], node.Position[2], node.Id)

		figure.set_xlabel('Latitude')
		figure.set_ylabel('Lonitude')
		figure.set_zlabel('Altitude in (km)')

		if Show is True:
			plt.show()

		if Save is True:
			Display.SaveNetwork(nodes, network, Radius, Name)

		plt.close()

	def MapNetwork(Nodes = None, Network = None, Name = None, Radius = '', Show = False, Save = False):
		"""Helper function that Draw a Network on top of Geographical Map"""
		import subprocess, os, webbrowser, time, sys, random;
		Display.SaveNetwork(Nodes, Network, Radius, Name)
		PORT = random.randint(5555, 10555)
		sys.argv.append(str(PORT))
		try:
			subprocess.Popen([sys.executable, '' + os.getcwd() + '/GUI/Network/runserver.py '] + sys.argv[1:], shell = True)
			time.sleep(1)
			webbrowser.open_new('http://localhost:{0}'.format(PORT))
		except:
			print('!Failed to open the page.\n\t{0}'.format(sys.exc_info()))

		

	def ConnectNodes(NODES, NETWORK, UNUSSIGNED):
		"""
		"""
		N = len(NETWORK)
		for node in list(NETWORK.values()):
			N += len(node.MEMBERS)
		
		CH = 0;
		for head in NETWORK.values():
			if (head.Type == -1 or head.Type == 3):
				CH += 1

		ICH = 0;
		for head in NETWORK.values():
			if (head.Type == 3 or head.Type == 2):
				ICH += 1

		print("Connected Nodes: {0:3}\tCH: {1:3}\tICH: {2:3}\tTotal Network: {3:3}\tTotal Nodes: {4:3}\tUnussigned Nodes: {5:3}\n\n".format(N, CH, ICH, len(NETWORK), len(NODES), len(UNUSSIGNED)))

		return CH, ICH

if __name__ == '__main__':
	import time

	Place = 'Mopani'
	Heads = [] #To store computed number of Cluster Heads
	Unussigned = [] #To store number of nodes not connected
	
	print("#01: Creating Nodes!\n")
	ServiceProvider = Provider(Id = '00', Address = "" + Place + ", South Africa", Position = [-23.829150, 30.142595,10])
	Network = Nodes()
	Network.CreateNodes('./Source/Data/' + Place + '.json', Place, ClusterRadius = 1000, ServiceProvider = ServiceProvider, Results = True)

	#MODELS
	print("\n#02: Running Models!\n")
	NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
	NODES, NETWORK, UNUSSIGNED, DATA = Model.Backhauling(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
	#Display.DrawPoints(NODES, NETWORK, Place +'-Bachauling-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	#Display.MapNetwork(NODES, NETWORK, Place + '-Myopic-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	CHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
	Display.SaveToCSV(NODES, NETWORK, "Backhauiling"); Display.SaveTopology(NODES, NETWORK, "Backhauiling"); Display.SaveRouting(NODES, NETWORK, "Backhauiling");
	NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();

	"""NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
	NODES, NETWORK, UNUSSIGNED, DATA = Model.Myopic(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
	NODES, NETWORK, UNUSSIGNED, DATA = Model.Balancing(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
	NODES, NETWORK, UNUSSIGNED, DATA = Model.Redistribute(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
	NODES, NETWORK, UNUSSIGNED, DATA = Model.Hoop(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius, ServiceProvider = ServiceProvider)	
	NODES, NETWORK, UNUSSIGNED, DATA = Model.Chaining(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
	#Display.DrawPoints(NODES, NETWORK, Place + '-Myopic-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	#Display.MapNetwork(NODES, NETWORK, Place + '-Myopic-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
	NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();

	NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
	NODES, NETWORK, UNUSSIGNED, DATA = Model.Odd(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
	#Display.DrawPoints(NODES, NETWORK, Place +'-Bachauling-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	#Display.MapNetwork(NODES, NETWORK, Place + '-Myopic-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	CHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
	NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();

	NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
	NODES, NETWORK, UNUSSIGNED, DATA = Model.Converse(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
	#Display.DrawPoints(NODES, NETWORK, Place +'-Bachauling-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	#Display.MapNetwork(NODES, NETWORK, Place + '-Myopic-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	CHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
	NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();

	NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
	NODES, NETWORK, UNUSSIGNED, DATA = Model.Converse(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
	#Display.DrawPoints(NODES, NETWORK, Place +'-Bachauling-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	#Display.MapNetwork(NODES, NETWORK, Place + '-Myopic-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	CHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
	NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
	
	NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
	NODES, NETWORK, UNUSSIGNED, DATA = Model.KMeans(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
	#Display.DrawPoints(NODES, NETWORK, Place + '-KMeans-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	Display.MapNetwork(NODES, NETWORK, Place + '-Myopic-Uniform-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius)
	Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
	NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();"""

	print('\n\n-----DONE-----')