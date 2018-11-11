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
			FileName = './Model/Computed Data/{0}-[{1}]-{2}.xlsx'.format(FileName, Stamp, Distribution)


		Columns = ['Emulation', 'Minimum SNR', 'Maximum SNR', 'Median RE', 'Backhauling CH', 'Myopic CH', 'GSMB - UAV CH', 'GSMB - LAP CH', 'Backhauling I-CH', 'Myopic I-CH', 'GSMB - UAV I-CH', 'GSMB - LAP I-CH', 'Backhauling Unassigned', 'Myopic Unassigned', 'GSMB - UAV Unassigned', 'GSMB - LAP Unassigned']
		
		DATA = {}
		DATA['Emulation'] = []
		DATA['Minimum SNR'] = []
		DATA['Maximum SNR'] = []
		DATA['Median RE'] = []
		DATA['Backhauling CH'] = []
		DATA['Myopic CH'] = []
		DATA['GSMB - UAV CH'] = []
		DATA['GSMB - LAP CH'] = []
		DATA['Backhauling I-CH'] = []
		DATA['Myopic I-CH'] = []
		DATA['GSMB - UAV I-CH'] = []
		DATA['GSMB - LAP I-CH'] = []
		DATA['Backhauling Unassigned'] = []
		DATA['Myopic Unassigned'] = []
		DATA['GSMB - UAV Unassigned'] = []
		DATA['GSMB - LAP Unassigned'] = []

		for data in INPUTDATA:
			DATA['Emulation'].append(data[0])
			DATA['Minimum SNR'].append(data[1])
			DATA['Maximum SNR'].append(data[2])
			DATA['Median RE'].append(data[3])
			DATA['Backhauling CH'].append(data[4])
			DATA['Myopic CH'].append(data[5])
			DATA['GSMB - UAV CH'].append(data[6])
			DATA['GSMB - LAP CH'].append(data[7])
			DATA['Backhauling I-CH'].append(data[8])
			DATA['Myopic I-CH'].append(data[9])
			DATA['GSMB - UAV I-CH'].append(data[10])
			DATA['GSMB - LAP I-CH'].append(data[11])
			DATA['Backhauling Unassigned'].append(data[12])
			DATA['Myopic Unassigned'].append(data[13])
			DATA['GSMB - UAV Unassigned'].append(data[14])
			DATA['GSMB - LAP Unassigned'].append(data[15])
		
		DataFrames = pd.DataFrame(data = DATA, columns = Columns)  #Create a Pandas dataframe from some data.
		Writer = pd.ExcelWriter(FileName, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
		DataFrames.to_excel(Writer, index=False, sheet_name=SheetName)
		Writer.save()

		if Results is True: print('DATA Saved to Excel File')


if __name__ is '__main__':
	import time

	Place = 'Khayelitsha'
	Code = '7784';
	Distribution = 'LogNormal'

	RESULTS = []	
	End = 50

	Network = None; NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

	with progressbar.ProgressBar(max_value = End) as bar:
		for i in range(1, End + 1):
			Heads = [] #To store computed number of Cluster Heads
			Unassigned = [] #To store number of nodes not connected
			Interclusters = []

			print('\n#{0:5}: Creating Nodes!'.format(i))
			ServiceProvider = Provider(Id = '00', Address = "" + Place + ", South Africa", Position = [-23.829150, 30.142595,10])
			Network = Nodes()
			Network.CreateNodes('./Source/Data/' + Place + '.json', Place, Code = Code, ClusterRadius = 5, ServiceProvider = ServiceProvider, Results = True)

			#MODELS
			print('\n#{0:5}: Running Models!'.format(i))
			NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
			Technique = 'Backhauling';
			NODES, NETWORK, UNUSSIGNED, DATA = Model.Backhauling(NODES, NETWORK, UNUSSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = False, Save = True, Radius = Network.ClusterRadius)
			CHs, ICHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNUSSIGNED)); Interclusters.append(ICHs);
			NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
			NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

			NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
			Technique = 'Myopic';
			NODES, NETWORK, UNUSSIGNED, DATA = Model.Myopic(NODES, NETWORK, UNUSSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNUSSIGNED, DATA = Model.Balancing(NODES, NETWORK, UNUSSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = False, Save = True, Radius = Network.ClusterRadius)
			CHs, ICHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNUSSIGNED)); Interclusters.append(ICHs);
			NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
			NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

			NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
			Technique = 'GSMB - UAV';
			NODES, NETWORK, UNUSSIGNED, DATA = Model.Greedy(NODES, NETWORK, UNUSSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = False, Save = True, Radius = Network.ClusterRadius)
			CHs, ICHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNUSSIGNED)); Interclusters.append(ICHs);
			NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
			NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

			NODES, NETWORK, UNUSSIGNED, DATA = Network.Network()
			Technique = 'GSMB - LAP';
			NODES, NETWORK, UNUSSIGNED, DATA = Model.Successive(NODES, NETWORK, UNUSSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = False, Save = True, Radius = Network.ClusterRadius)
			CHs, ICHs = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNUSSIGNED = UNUSSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNUSSIGNED)); Interclusters.append(ICHs);
			NODES.clear(); NETWORK.clear(); UNUSSIGNED.clear();
			NODES = None; NETWORK = None; UNUSSIGNED = None; DATA = None;

			bar.update(i)
			RESULTS.append([i, Network.Minimum_SNR, Network.Maximum_SNR, Network.Median_ResidualEnergy] + Heads + Interclusters + Unassigned)
			del Network;

	Emulation.SaveToExcel(RESULTS, FileName = Place, SheetName = Distribution, Distribution=Distribution)

	print('\n\n-----DONE-----')
