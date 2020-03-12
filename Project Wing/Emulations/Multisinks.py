"""         
Authors:     Kloni Maluleke (Msc), kloniphani@gmail.com
Date:        November 21, 2019
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
			FileName = './Source/Results/Network/Multisink/Results.xlsx'
		else:
			if Distribution is None: Distribution = '';
			Stamp = str(strftime("%Y %b %d %H-%M", gmtime()))
			FileName = './Source/Results/Network/Multisink/{0}-[{1}]-{2}.xlsx'.format(FileName, Stamp, Distribution)

		Columns = ['Emulation', 'Minimum SNR', 'Maximum SNR', 'Median RE', 
			 'Tree Balancing CH', 'Path Balancing CH',
			 'Tree Balancing I-CH', 'Path Balancing I-CH',
			 'Tree Balancing Unassigned', 'Path Balancing Unassigned']
		
		DATA = {}
		DATA['Emulation'] = []
		DATA['Minimum SNR'] = []
		DATA['Maximum SNR'] = []
		DATA['Median RE'] = []

		DATA['Tree Balancing CH'] = []
		DATA['Path Balancing CH'] = []		 		

		DATA['Tree Balancing I-CH'] = []
		DATA['Path Balancing I-CH'] = []	   		

		DATA['Tree Balancing Unassigned'] = []
		DATA['Path Balancing Unassigned'] = []						

		for data in INPUTDATA:
			DATA['Emulation'].append(data[0])
			DATA['Minimum SNR'].append(data[1])
			DATA['Maximum SNR'].append(data[2])
			DATA['Median RE'].append(data[3])

			DATA['Tree Balancing CH'].append(data[4])
			DATA['Path Balancing CH'].append(data[5])	 			

			DATA['Tree Balancing I-CH'].append(data[6])
			DATA['Path Balancing I-CH'].append(data[7]) 			

			DATA['Tree Balancing Unassigned'].append(data[8])
			DATA['Path Balancing Unassigned'].append(data[9])						
		
		DataFrames = pd.DataFrame(data = DATA, columns = Columns)  #Create a Pandas dataframe from some data.
		Writer = pd.ExcelWriter(FileName, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
		DataFrames.to_excel(Writer, index=False, sheet_name=SheetName)
		Writer.save()

		if Results is True: print('DATA Saved to Excel File')


if __name__ is '__main__':
	import time

	Place = 'Lulekani'
	Code = '1818';
	Distribution = 'LogNormal'
	Date = datetime.datetime.now().strftime("%d-%m-%y")
	Time = datetime.datetime.now().strftime("%H-%M")

	RESULTS = []	
	End = 1

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
			Network.CreateNodes('./RF Planning/Location/Study/' + Place + '.json', Place, ClusterRadius = 10, ServiceProvider = ServiceProvider, Results = True)

			#MODELS
			print('\n#{0:5}: Running Models!'.format(i))
			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Tree Balancing';
			NODES, NETWORK, UNASSIGNED, DATA = Multisink.GreedySinkNodeSelectionWithSinksTree(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'LAP', ClusterRadius = Network.ClusterRadius)	
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = False, Save = True, Radius = Network.ClusterRadius, Type = '2D')
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Path Balancing';
			NODES, NETWORK, UNASSIGNED, DATA = Shortpaths.GreedySinkNodeSelection(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'LAP', ClusterRadius = Network.ClusterRadius)	
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = False, Save = True, Radius = Network.ClusterRadius, Type = '2D')
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			bar.update(i)
			RESULTS.append([i, Network.Minimum_SNR, Network.Maximum_SNR, Network.Median_ResidualEnergy] + Heads + Interclusters + Unassigned + Empty)
			del Network;

	Emulation.SaveToExcel(RESULTS, FileName = Place, SheetName = Distribution, Distribution=Distribution)

	print('\n\n-----DONE-----')


