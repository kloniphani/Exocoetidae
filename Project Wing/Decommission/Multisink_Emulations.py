"""         
Authors:     Kloni Maluleke (Msc), kloniphani@gmail.com
Date:        April 10, 2018
Copyrights:  2018 ISAT, Department of Computer Science
             University of the Western Cape, Bellville, ZA
"""

#PACKAGES
#Object Oriented Classes
from Project_Wing import *
import progressbar

class Emulation(object):
	def SaveToExcel(INPUTDATA, FileName = None, SheetName = None, Distribution = None, Results = False):
		import pandas as pd
		from time import gmtime, strftime

		if SheetName is None: SheetName = 'Results';
		if FileName is None:
			FileName = './Model/Computed Data/Results.xlsx'
		else:
			if Distribution is None: Distribution = '';
			Stamp = str(strftime("%Y %b %d %H-%M", gmtime()))
			FileName = './Model/Backbone/{0}-[{1}]-{2}.xlsx'.format(FileName, Stamp, Distribution)


		Columns = ['Emulation', 'Minimum SNR', 'Maximum SNR', 'Median RE', 
			 'Backhauling CH', 'Myopic CH', 'MSGBACK CH', 'MSLBACK CH', 'K-Means CH',
			 'Backhauling I-CH', 'Myopic I-CH', 'MSGBACK I-CH', 'MSLBACK I-CH', 'K-Means I-CH',
			 'Backhauling Unassigned', 'Myopic Unassigned', 'MSGBACK Unassigned', 'MSLBACK Unassigned', 'K-Means Unassigned',]
		
		DATA = {}
		DATA['Emulation'] = []
		DATA['Minimum SNR'] = []
		DATA['Maximum SNR'] = []
		DATA['Median RE'] = []
		DATA['Backhauling CH'] = []
		DATA['Myopic CH'] = []
		DATA['MSGBACK CH'] = []
		DATA['MSLBACK CH'] = []
		DATA['K-Means CH'] = []
		DATA['Backhauling I-CH'] = []
		DATA['Myopic I-CH'] = []
		DATA['MSGBACK I-CH'] = []
		DATA['MSLBACK I-CH'] = []
		DATA['K-Means I-CH'] = []
		DATA['Backhauling Unassigned'] = []
		DATA['Myopic Unassigned'] = []
		DATA['MSGBACK Unassigned'] = []
		DATA['MSLBACK Unassigned'] = []
		DATA['K-Means Unassigned'] = []

		for data in INPUTDATA:
			DATA['Emulation'].append(data[0])
			DATA['Minimum SNR'].append(data[1])
			DATA['Maximum SNR'].append(data[2])
			DATA['Median RE'].append(data[3])
			DATA['Backhauling CH'].append(data[4])
			DATA['Myopic CH'].append(data[5])
			DATA['MSGBACK CH'].append(data[6])
			DATA['MSLBACK CH'].append(data[7])
			DATA['K-Means CH'].append(data[8])
			DATA['Backhauling I-CH'].append(data[9])
			DATA['Myopic I-CH'].append(data[10])
			DATA['MSGBACK I-CH'].append(data[11])
			DATA['MSLBACK I-CH'].append(data[12])
			DATA['K-Means I-CH'].append(data[13])
			DATA['Backhauling Unassigned'].append(data[14])
			DATA['Myopic Unassigned'].append(data[15])
			DATA['MSGBACK Unassigned'].append(data[16])
			DATA['MSLBACK Unassigned'].append(data[17])
			DATA['K-Means Unassigned'].append(data[18])
		
		DataFrames = pd.DataFrame(data = DATA, columns = Columns)  #Create a Pandas dataframe from some data.
		Writer = pd.ExcelWriter(FileName, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
		DataFrames.to_excel(Writer, index=False, sheet_name=SheetName)
		Writer.save()

		if Results is True: print('DATA Saved to Excel File')


if __name__ is '__main__':
	import time

	Place = 'Khayelitsha'
	Code = '7784';
	Distribution = 'Normal'

	RESULTS = []	
	End = 10

	Network = None; NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

	with progressbar.ProgressBar(max_value = End) as bar:
		for i in range(1, End + 1):
			Heads = [] #To store computed number of Cluster Heads
			Unassigned = [] #To store number of nodes not connected
			Interclusters = []
			Empty = []

			print('\n#{0:5}: Creating Nodes!'.format(i))
			ServiceProvider = Provider(Id = '00', Address = "" + Place + ", South Africa", Position = [-23.829150, 30.142595,10])
			Network = Nodes()
			Network.CreateNodes('./Source/Data/' + Place + '.json', Place, ClusterRadius = 100, ServiceProvider = ServiceProvider, Results = True)

			#MODELS
			print('\n#{0:5}: Running Models!'.format(i))
			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Backhauling';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Backhauling(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Myopic';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Myopic(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Balancing(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'MSGBACK';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Greedy(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'MSLBACK';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Successive(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNASSIGNED, DATA = Model.KMeans(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			bar.update(i)
			RESULTS.append([i, Network.Minimum_SNR, Network.Maximum_SNR, Network.Median_ResidualEnergy] + Heads + Interclusters + Unassigned + Empty)
			del Network;

	Emulation.SaveToExcel(RESULTS, FileName = Place, SheetName = Distribution, Distribution=Distribution)

	print('\n\n-----DONE-----')

