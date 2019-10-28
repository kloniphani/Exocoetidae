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

		Columns = ['Emulation', 'Minimum SNR', 'Maximum SNR', 'Median RE', 'Backhauling CH', 'MSLBACK CH', 'MSGBACK CH', 'K-Means CH', 'Backhauling I-CH', 'MSLBACK I-CH', 'MSGBACK I-CH', 'K-Means I-CH', 
			 'Backhauling Unassigned', 'MSLBACK Unassigned', 'MSGBACK Unassigned', 'K-Means Unassigned', 'Backhauling Empty', 'MSLBACK Empty', 'MSGBACK Empty', 'K-Means Empty']
		
		DATA = {}
		DATA['Emulation'] = []
		DATA['Minimum SNR'] = []
		DATA['Maximum SNR'] = []
		DATA['Median RE'] = []
		DATA['Backhauling CH'] = []
		DATA['MSLBACK CH'] = []
		DATA['MSGBACK CH'] = []
		DATA['K-Means CH'] = []
		DATA['Backhauling I-CH'] = []
		DATA['MSLBACK I-CH'] = []
		DATA['MSGBACK I-CH'] = []
		DATA['K-Means I-CH'] = []
		DATA['Backhauling Unassigned'] = []
		DATA['MSLBACK Unassigned'] = []
		DATA['MSGBACK Unassigned'] = []
		DATA['K-Means Unassigned'] = []
		DATA['Backhauling Empty'] = []
		DATA['MSLBACK Empty'] = []
		DATA['MSGBACK Empty'] = []
		DATA['K-Means Empty'] = []

		for data in INPUTDATA:
			DATA['Emulation'].append(data[0])
			DATA['Minimum SNR'].append(data[1])
			DATA['Maximum SNR'].append(data[2])
			DATA['Median RE'].append(data[3])
			DATA['Backhauling CH'].append(data[4])
			DATA['MSLBACK CH'].append(data[5])
			DATA['MSGBACK CH'].append(data[6])
			DATA['K-Means CH'].append(data[7])
			DATA['Backhauling I-CH'].append(data[8])
			DATA['MSLBACK I-CH'].append(data[9])
			DATA['MSGBACK I-CH'].append(data[10])
			DATA['K-Means I-CH'].append(data[11])
			DATA['Backhauling Unassigned'].append(data[12])
			DATA['MSLBACK Unassigned'].append(data[13])
			DATA['MSGBACK Unassigned'].append(data[14])
			DATA['K-Means Unassigned'].append(data[15])
			DATA['Backhauling Empty'].append(data[16])
			DATA['MSLBACK Empty'].append(data[17])
			DATA['MSGBACK Empty'].append(data[18])
			DATA['K-Means Empty'].append(data[19])
		
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
	End = 20
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
			NODES, NETWORK, UNASSIGNED, DATA = Model.Myopic(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Balancing(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNASSIGNED, DATA = Model.Myopic(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Balancing(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Chaining(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Hoop(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius, ServiceProvider = ServiceProvider)
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
			time.sleep(5)

	Emulation.SaveToExcel(RESULTS, FileName = FileName)

	print('\n\n-----DONE-----')

