"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       April 10, 2018
Copyright:  2018 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""

#PACKAGES
#Object Oriented Classes
from Project_Wing import *
import progressbar

class Emulation(object):
	def SaveToExcel(INPUTDATA, FileName = None, SheetName = None, Results = False):
		import pandas as pd
		import time

		if FileName is not None:
			FileName = './Model/Computed Data/{0}-{1}.xlsx'.format(FileName, time.ctime())
		else:
			FileName = './Model/Computed Data/Results.xlsx'

		if SheetName is None:
			SheetName = 'Results'

		Columns = ['', 'Minimum SNR', 'Maximum SNR', 'Median RE', 'Backhauling CH', 'Myopic CH', 'Odd CH', 'OddRange CH', 'K-Means CH', 'Backhauling I-CH', 'Myopic I-CH', 'Odd I-CH', 'OddRange I-CH', 'K-Means I-CH', 'Backhauling Unussigned', 'Myopic Unussigned', 'Odd Unussigned', 'OddRange Unussigned', 'K-Means Unussigned']
		
		DATA = {}
		DATA['Run'] = []
		DATA['Minimum SNR'] = []
		DATA['Maximum SNR'] = []
		DATA['Median RE'] = []
		DATA['Backhauling CH'] = []
		DATA['Myopic CH'] = []
		DATA['Odd CH'] = []
		DATA['OddRange CH'] = []
		DATA['Converse CH'] = []
		DATA['K-Means CH'] = []
		DATA['Backhauling I-CH'] = []
		DATA['Myopic I-CH'] = []
		DATA['Odd I-CH'] = []
		DATA['OddRange I-CH'] = []
		DATA['Converse I-CH'] = []
		DATA['K-Means I-CH'] = []
		DATA['Backhauling Unussigned'] = []
		DATA['Myopic Unussigned'] = []
		DATA['Odd Unussigned'] = []
		DATA['OddRange Unussigned'] = []
		DATA['Converse Unussigned'] = []
		DATA['K-Means Unussigned'] = []

		for data in INPUTDATA:
			DATA['Run'].append(data[0])
			DATA['Minimum SNR'].append(data[1])
			DATA['Maximum SNR'].append(data[2])
			DATA['Median RE'].append(data[3])
			DATA['Backhauling CH'].append(data[4])
			DATA['Myopic CH'].append(data[5])
			DATA['Odd CH'].append(data[6])
			DATA['OddRange CH'].append(data[7])
			DATA['Converse CH'].append(data[8])
			DATA['K-Means CH'].append(data[9])
			DATA['Backhauling I-CH'].append(data[10])
			DATA['Myopic I-CH'].append(data[11])
			DATA['Odd I-CH'].append(data[12])
			DATA['OddRange I-CH'].append(data[13])
			DATA['Converse I-CH'].append(data[14])
			DATA['K-Means I-CH'].append(data[15])
			DATA['Backhauling Unussigned'].append(data[16])
			DATA['Myopic Unussigned'].append(data[17])
			DATA['Odd Unussigned'].append(data[18])
			DATA['OddRange Unussigned'].append(data[19])
			DATA['Converse Unussigned'].append(data[20])
			DATA['K-Means Unussigned'].append(data[21])
		
		DataFrames = pd.DataFrame(data = DATA, columns = Columns)  #Create a Pandas dataframe from some data.
		Writer = pd.ExcelWriter(FileName, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
		DataFrames.to_excel(Writer, index=False, sheet_name=SheetName)
		Writer.save()

		if Results is True: print('DATA Saved to Excel File')


if __name__ is '__main__':
	import time

	Place = 'Mopani'
	RESULTS = []	
	End = 20

	Network = None; NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

	with progressbar.ProgressBar(max_value = End) as bar:
		for i in range(1, End + 1):
			Heads = [] #To store computed number of Cluster Heads
			Unussigned = [] #To store number of nodes not connected
			Interclusters = []

			print('\n#{0:5}: Creating Nodes!'.format(i))
			ServiceProvider = Provider(Id = '00', Address = "" + Place + ", South Africa", Position = [-23.829150, 30.142595,10])
			Network = Nodes()
			Network.CreateNodes('./Source/Data/' + Place + '.json', Place, ClusterRadius = 1000, ServiceProvider = ServiceProvider, Results = False)

			#MODELS
			print('\n#{0:5}: Running Models!'.format(i))
			NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNUSSIGNED, DATA = Model.Backhauling(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
			Heads.append(CHs); Unussigned.append(len(UNUSSIGNED)); Interclusters.append(ICHs);
			NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
			NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

			NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNUSSIGNED, DATA = Model.Myopic(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNUSSIGNED, DATA = Model.Balancing(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
			Heads.append(CHs); Unussigned.append(len(UNUSSIGNED)); Interclusters.append(ICHs);
			NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
			NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

			NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNUSSIGNED, DATA = Model.Odd(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
			Heads.append(CHs); Unussigned.append(len(UNUSSIGNED)); Interclusters.append(ICHs);
			NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
			NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

			NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNUSSIGNED, DATA = Model.OddRange(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
			Heads.append(CHs); Unussigned.append(len(UNUSSIGNED)); Interclusters.append(ICHs);
			NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
			NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

			NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNUSSIGNED, DATA = Model.Converse(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
			Heads.append(CHs); Unussigned.append(len(UNUSSIGNED)); Interclusters.append(ICHs);
			NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
			NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;
	
			NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNUSSIGNED, DATA = Model.KMeans(NODES, NETWORK, UNUSSIGNED, DATA, Network.ResidualEnergy_Median, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
			Heads.append(CHs); Unussigned.append(len(UNUSSIGNED)); Interclusters.append(ICHs);
			NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
			NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

			bar.update(i)
			RESULTS.append([i, Network.Minimum_SNR, Network.Maximum_SNR, Network.ResidualEnergy_Median] + Heads + Interclusters + Unussigned)
			del Network;
			time.sleep(5)

	Emulation.SaveToExcel(RESULTS)

	print('\n\n-----DONE-----')