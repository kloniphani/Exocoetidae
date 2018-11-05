"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       October 16, 2018
Copyright:  2017 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""

from numpy import * 
import json, io, datetime, progressbar, csv
from xml.etree import ElementTree

#These packages are for ploting the graph
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

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

		AccesPointAdreess = '192.0.0.x'

		etree.SubElement(page, 'interface', hosts='P1', names='wlan0', address=AccesPointAdreess, netmask='255.x.x.x') 

		for key, value in Network.items():	
			ClusterHeadAddress = '' + str(AccessPoint) + '.' + str(ClusterHead) + '.0.0'

			for node in value.MEMBERS:
				etree.SubElement(page, 'interface', hosts='N' + node.Id, names='wlan0', address=''+str(AccessPoint) + '.' + str(ClusterHead) + '.' + str(ClusterMember)+ '.x', netmask='255.255.255.0')
				etree.SubElement(page, 'route', hosts='N' + node.Id, destination=ClusterHeadAddress, netmask='255.255.255.0', gateway=ClusterHeadAddress)
				ClusterMember += 1;

			etree.SubElement(page, 'interface', hosts='N' + value.Id, names='wlan0', address=ClusterHeadAddress, netmask='255.255.0.0')
			etree.SubElement(page, 'route', hosts='N' + value.Id, destination=AccesPointAdreess, netmask='255.255.0.0', gateway = AccesPointAdreess)
			ClusterHead += 1

		doc.write('./Source/Topology/' + FileName + 'Routing.xml', xml_declaration = True, pretty_print=True, encoding='utf-16')


	def SaveNetwork(Nodes, Network, Radius, Name = None):
		"""
		"""
		FileName = ''
		if Name is not None:
			FileName += str(Name)
		FileName += str('---' + datetime.datetime.now().strftime("%d-%m-%y--%H-%M"))

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

	def DrawPoints(nodes = None, network = None, Name = None, Radius = '', Show = False, Save = False, Type = '2D'):
		"""Helper function that returns a figure with point attributes in an array for every cluster network"""
		
		fig = plt.figure()
		if Name is not None: fig.canvas.set_window_title(Name)
		if Type is '3D': figure = fig.add_subplot(111, projection = '3d')
		else: figure = fig.add_subplot(111)

		from itertools import cycle
		points = []; colors = cycle('rgbmcy')
	
		if network is not None and nodes is not None:
			with progressbar.ProgressBar(max_value = len(network)) as bar:
				count = 0
				if Type is '3D':
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
				
				if Type is '2D':					
					for head in list(network.values()):
						figure.scatter(head.Position[0], head.Position[1], zorder = 3, c = 'k', marker = 'o', s = 80)
			
						color = next(colors)
		
						figure.scatter(head.Position[0], head.Position[1], zorder = 4, c = color, marker = 'o', s = 10)
						figure.text(head.Position[0], head.Position[1], head.Id)
				
						for leaf in head.MEMBERS:
							#Drawing a line in 3d
							spacing = 100
							xs = linspace(head.Position[0], leaf.Position[0], spacing)
							ys = linspace(head.Position[1], leaf.Position[1], spacing)

							figure.plot(xs, ys, zorder = 1, c = color)
							figure.scatter(leaf.Position[0], leaf.Position[1], zorder = 2, c = color, marker = 'o', s = 30)
							figure.text(leaf.Position[0], leaf.Position[1], leaf.Id)

						count += 1
						bar.update(count)

					for node in nodes.values():
						draw = True
						if node.Id not in [n.Id for n in list(network.values())]: 							
							for head in list(network.values()):
								if node.Id in [leaf.Id for leaf in head.MEMBERS]:
									draw = False
									break
		
							if draw is True:
								if node.Type == -2:
									figure.scatter(node.Position[0], node.Position[1], zorder = 6, c = 'black', marker = 'o', s = 120)
									figure.text(node.Position[0], node.Position[1], node.Id)
								else:
									figure.scatter(node.Position[0], node.Position[1], zorder = 5, c = 'gray', marker = 'o', s = 30)
									figure.text(node.Position[0], node.Position[1], node.Id)

		figure.set_ylabel('Latitude')
		figure.set_xlabel('Longitude')
		if Type is '3D': figure.set_zlabel('Altitude in (km)')

		if Show is True:
			plt.show(block=True)

		if Save is True:
			Display.SaveNetwork(nodes, network, Radius, Name)
			FileName = ''
			if Name is not None:
				FileName += str(Name)
			FileName += str('---' + datetime.datetime.now().strftime("%d-%m-%y--%H-%M"))
			fig.savefig('./Source/Results/' + FileName + "-R" + str(Radius) + '.png')
		
		from time import sleep;
		sleep(1);
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
