"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       October 28, 2019
Copyrights:  2019 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""

#PACKAGES
#Object Oriented Classes
from Project_Wing import *
import progressbar

class Emulation(object):
	def SaveToExcel(INPUTDATA, FileName = None, SheetName = None, Results = False):
		import pandas as pd
		import datetime

		if FileName is not None:
			FileName = './Model/Clustering/{0}-{1}.xlsx'.format(FileName,  datetime.datetime.now().strftime("%d-%m-%y--%H-%M"))
		else:
			FileName = './Model/Clustering/Results.xlsx'

		if SheetName is None:
			SheetName = 'Results'

		Columns = ['Emulation', 'Minimum SNR', 'Maximum SNR', 'Median RE', 
			 'Traditional Backhauling CH', 'Distance Balanced Backhauling CH', 'Density Balanced Backhauling CH', 
			 'Traditional Backhauling I-CH', 'Distance Balanced BackhaulingI-CH', 'Density Balanced Backhauling I-CH',
			 'Traditional Backhauling Unassigned', 'Distance Balanced BackhaulingK Unassigned', 'Density Balanced Backhauling Unassigned',  
			 'Traditional Backhauling Empty', 'Distance Balanced Backhauling Empty', 'Density Balanced Backhauling Empty']
		
		DATA = {}
		DATA['Emulation'] = []
		DATA['Minimum SNR'] = []
		DATA['Maximum SNR'] = []
		DATA['Median RE'] = []
		DATA['Traditional Backhauling CH'] = []
		DATA['Distance Balanced Backhauling CH'] = []
		DATA['Density Balanced Backhauling CH'] = []
		DATA['Traditional Backhauling I-CH'] = []
		DATA['Distance Balanced Backhauling I-CH'] = []
		DATA['Density Balanced Backhauling I-CH'] = []
		DATA['Traditional Backhauling Unassigned'] = []
		DATA['Distance Balanced Backhauling Unassigned'] = []
		DATA['Density Balanced Backhauling Unassigned'] = []
		DATA['Traditional Backhauling Empty'] = []
		DATA['Distance Balanced Backhauling Empty'] = []
		DATA['Density Balanced Backhauling Empty'] = []


		for data in INPUTDATA:
			DATA['Emulation'].append(data[0])
			DATA['Minimum SNR'].append(data[1])
			DATA['Maximum SNR'].append(data[2])
			DATA['Median RE'].append(data[3])
			DATA['Traditional Backhauling CH'].append(data[4])
			DATA['Distance Balanced Backhauling CH'].append(data[5])
			DATA['Density Balanced Backhauling CH'].append(data[6])
			DATA['Traditional Backhauling I-CH'].append(data[7])
			DATA['Distance Balanced Backhauling I-CH'].append(data[8])
			DATA['Density Balanced Backhauling I-CH'].append(data[9])
			DATA['Traditional Backhauling Unassigned'].append(data[10])
			DATA['Distance Balanced Backhauling Unassigned'].append(data[11])
			DATA['Density Balanced Backhauling Unassigned'].append(data[12])
			DATA['Traditional Backhauling Empty'].append(data[13])
			DATA['Distance Balanced Backhauling Empty'].append(data[14])
			DATA['Density Balanced Backhauling Empty'].append(data[15])
		
		
		DataFrames = pd.DataFrame(data = DATA, columns = Columns)  #Create a Pandas dataframe from some data.
		Writer = pd.ExcelWriter(FileName, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
		DataFrames.to_excel(Writer, index=False, sheet_name=SheetName)
		Writer.save()

		if Results is True: print('DATA Saved to Excel File')


if __name__ is '__main__':
	import time

	Place = 'Mopani'
	Code = '0930';
	Distribution = 'Normal'
	RESULTS = []	
	End = 10
	FileName = "{0}-{1}".format(Place, Distribution)

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
			Network.CreateNodes('./Source/Data/' + Place + '.json', Place, ClusterRadius = 1000, ServiceProvider = ServiceProvider, Results = False)

			#MODELS
			print('\n#{0:5}: Running Models!'.format(i))
			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNASSIGNED, DATA = Model.Backhauling(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;


			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNASSIGNED, DATA = Model.Backhauling(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.DistanceBalancing(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNASSIGNED, DATA = Model.Backhauling(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.DensityBalancing(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;


			bar.update(i)
			RESULTS.append([i, Network.Minimum_SNR, Network.Maximum_SNR, Network.Median_ResidualEnergy] + Heads + Interclusters + Unassigned + Empty)
			del Network;
			time.sleep(5)

	Emulation.SaveToExcel(RESULTS, FileName = FileName)

	print('\n\n-----DONE-----')


