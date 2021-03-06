"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       April 10, 2018
Copyrights:  2018 ISAT, Department of Computer Science
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
			FileName = './Model/Computed Data/{0}-{1}.xlsx'.format(FileName,  datetime.datetime.now().strftime("%d-%m-%y--%H-%M"))
		else:
			FileName = './Model/Computed Data/Results.xlsx'

		if SheetName is None:
			SheetName = 'Results'

		Columns = ['Emulation', 'Minimum SNR', 'Maximum SNR', 'Median RE', 'Backhauling CH', 'Myopic CH', 'Odd CH', 'OddRange CH', 'K-Means CH', 'Backhauling I-CH', 'Myopic I-CH', 'Odd I-CH', 'OddRange I-CH', 'K-Means I-CH', 'Backhauling Unassigned', 'Myopic Unassigned', 'Odd Unassigned', 'OddRange Unassigned', 'K-Means Unassigned', 'Backhauling Empty', 'Myopic Empty', 'Odd Empty', 'OddRange Empty', 'K-Means Empty']
		
		DATA = {}
		DATA['Emulation'] = []
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
		DATA['Backhauling Unassigned'] = []
		DATA['Myopic Unassigned'] = []
		DATA['Odd Unassigned'] = []
		DATA['OddRange Unassigned'] = []
		DATA['Converse Unassigned'] = []
		DATA['K-Means Unassigned'] = []
		DATA['Backhauling Empty'] = []
		DATA['Myopic Empty'] = []
		DATA['Odd Empty'] = []
		DATA['OddRange Empty'] = []
		DATA['Converse Empty'] = []
		DATA['K-Means Empty'] = []

		for data in INPUTDATA:
			DATA['Emulation'].append(data[0])
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
			DATA['Backhauling Unassigned'].append(data[16])
			DATA['Myopic Unassigned'].append(data[17])
			DATA['Odd Unassigned'].append(data[18])
			DATA['OddRange Unassigned'].append(data[19])
			DATA['Converse Unassigned'].append(data[20])
			DATA['K-Means Unassigned'].append(data[21])
			DATA['Backhauling Empty'].append(data[22])
			DATA['Myopic Empty'].append(data[23])
			DATA['Odd Empty'].append(data[24])
			DATA['OddRange Empty'].append(data[25])
			DATA['Converse Empty'].append(data[26])
			DATA['K-Means Empty'].append(data[27])
		
		DataFrames = pd.DataFrame(data = DATA, columns = Columns)  #Create a Pandas dataframe from some data.
		Writer = pd.ExcelWriter(FileName, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
		DataFrames.to_excel(Writer, index=False, sheet_name=SheetName)
		Writer.save()

		if Results is True: print('DATA Saved to Excel File')


if __name__ is '__main__':
	import time

	Place = 'Mopani'
	Code = '0930';
	Distribution = 'ChiSquare'
	RESULTS = []	
	End = 50
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
			NODES, NETWORK, UNASSIGNED, DATA = Model.Odd(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNASSIGNED, DATA = Model.OddRange(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			NODES, NETWORK, UNASSIGNED, DATA = Model.Converse(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
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
