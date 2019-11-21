"""         
Authors:     Kloni Maluleke (Msc), kloniphani@gmail.com
Date:        November 19, 2019
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
			 'TNS CH', 'TNS Gateways CH', 'SNS CH', 'SNS Gateways CH',
			 'TNS I-CH', 'TNS Gateways I-CH', 'SNS I-CH', 'SNS Gateways I-CH',
			 'TNS Unassigned', 'TNS Gateways Unassigned', 'SNS Unassigned', 'SNS Gateways Unassigned']
		
		DATA = {}
		DATA['Emulation'] = []
		DATA['Minimum SNR'] = []
		DATA['Maximum SNR'] = []
		DATA['Median RE'] = []

		DATA['TNS CH'] = []
		DATA['TNS Gateways CH'] = []		 		
		DATA['SNS CH'] = []
		DATA['SNS Gateways CH'] = []

		DATA['TNS I-CH'] = []
		DATA['TNS Gateways I-CH'] = []	   		
		DATA['SNS I-CH'] = []
		DATA['SNS Gateways I-CH'] = []

		DATA['TNS Unassigned'] = []
		DATA['TNS Gateways Unassigned'] = []						
		DATA['SNS Unassigned'] = []
		DATA['SNS Gateways Unassigned'] = []

		for data in INPUTDATA:
			DATA['Emulation'].append(data[0])
			DATA['Minimum SNR'].append(data[1])
			DATA['Maximum SNR'].append(data[2])
			DATA['Median RE'].append(data[3])

			DATA['TNS CH'].append(data[4])
			DATA['TNS Gateways CH'].append(data[5])	 			
			DATA['SNS CH'].append(data[6])
			DATA['SNS Gateways CH'].append(data[7])

			DATA['TNS I-CH'].append(data[15])
			DATA['TNS Gateways I-CH'].append(data[16]) 			
			DATA['SNS I-CH'].append(data[17])
			DATA['SNS Gateways I-CH'].append(data[18])

			DATA['TNS Unassigned'].append(data[26])
			DATA['TNS Gateways Unassigned'].append(data[27])						
			DATA['SNS Unassigned'].append(data[28])
			DATA['SNS Gateways Unassigned'].append(data[29])
		
		DataFrames = pd.DataFrame(data = DATA, columns = Columns)  #Create a Pandas dataframe from some data.
		Writer = pd.ExcelWriter(FileName, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
		DataFrames.to_excel(Writer, index=False, sheet_name=SheetName)
		Writer.save()

		if Results is True: print('DATA Saved to Excel File')


if __name__ is '__main__':
	import time

	Place = 'Soweto'
	Code = '1818';
	Distribution = 'Normal'
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
			Technique = 'TNS';
			NODES, NETWORK, UNASSIGNED, DATA = Multisink.GreedySinkNodeSelectionWithSinksTree(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'UAV', ClusterRadius = Network.ClusterRadius)	
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius, Type = '2D')
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'TNS Gateways';
			NODES, NETWORK, UNASSIGNED, DATA = Multisink.GreedySinkNodeSelectionWithSinksTree(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'LAP', ClusterRadius = Network.ClusterRadius)	
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius, Type = '2D')
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'SNS';
			NODES, NETWORK, UNASSIGNED, DATA = Shortpaths.GreedySinkNodeSelection(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'UAV', ClusterRadius = Network.ClusterRadius)	
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius, Type = '2D')
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'SNS Gateways';
			NODES, NETWORK, UNASSIGNED, DATA = Shortpaths.GreedySinkNodeSelection(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'LAP', ClusterRadius = Network.ClusterRadius)	
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			Display.DrawPoints(NODES, NETWORK, Place + '-' + Technique + '-' + Distribution + '-Distribution', Show = True, Save = True, Radius = Network.ClusterRadius, Type = '2D')
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			bar.update(i)
			RESULTS.append([i, Network.Minimum_SNR, Network.Maximum_SNR, Network.Median_ResidualEnergy] + Heads + Interclusters + Unassigned + Empty)
			del Network;

	Emulation.SaveToExcel(RESULTS, FileName = Place, SheetName = Distribution, Distribution=Distribution)

	print('\n\n-----DONE-----')


