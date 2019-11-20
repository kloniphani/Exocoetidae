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
			FileName = './Source/Results/Network/Backhauling/Results.xlsx'
		else:
			if Distribution is None: Distribution = '';
			Stamp = str(strftime("%Y %b %d %H-%M", gmtime()))
			FileName = './Source/Results/Network/Backhauling/{0}-[{1}]-{2}.xlsx'.format(FileName, Stamp, Distribution)

		Columns = ['Emulation', 'Minimum SNR', 'Maximum SNR', 'Median RE', 
			 'Backhauling CH', 'Myopic CH', 'MSGBACK CH', 'MSLBACK CH', 'Redistribution CH', 'Chaining CH', 'Hooping CH', 'K-Means CH', 'Odd CH', 'Odd Range CH', 'Converse CH',
			 'Backhauling I-CH', 'Myopic I-CH', 'MSGBACK I-CH', 'MSLBACK I-CH', 'Redistribution I-CH',	'Chaining I-CH', 'Hooping I-CH', 'K-Means I-CH', 'Odd I-CH', 'Odd Range I-CH', 'Converse I-CH',
			 'Backhauling Unassigned', 'Myopic Unassigned', 'MSGBACK Unassigned', 'MSLBACK Unassigned', 'Redistribution Unassigned', 'Chaining Unassigned', 'Hooping Unassigned', 'K-Means Unassigned', 'Odd Unassigned', 'Odd Range Unassigned', 'Converse Unassigned']
		
		DATA = {}
		DATA['Emulation'] = []
		DATA['Minimum SNR'] = []
		DATA['Maximum SNR'] = []
		DATA['Median RE'] = []

		DATA['Myopic CH'] = []
		DATA['Backhauling CH'] = []		 		
		DATA['MSGBACK CH'] = []
		DATA['MSLBACK CH'] = []
		DATA['Redistribution CH'] = []
		DATA['Chaining CH'] = []
		DATA['Hooping CH'] = []		 		
		DATA['K-Means CH'] = []
		DATA['Odd CH'] = []
		DATA['Odd Range CH'] = []
		DATA['Converse CH'] = []

		DATA['Myopic I-CH'] = []
		DATA['Backhauling I-CH'] = []	   		
		DATA['MSGBACK I-CH'] = []
		DATA['MSLBACK I-CH'] = []
		DATA['Redistribution I-CH'] = []
		DATA['Chaining I-CH'] = []
		DATA['Hooping I-CH'] = []	   		
		DATA['K-Means I-CH'] = []
		DATA['Odd I-CH'] = []
		DATA['Odd Range I-CH'] = []
		DATA['Converse I-CH'] = []

		DATA['Myopic Unassigned'] = []
		DATA['Backhauling Unassigned'] = []						
		DATA['MSGBACK Unassigned'] = []
		DATA['MSLBACK Unassigned'] = []
		DATA['Redistribution Unassigned'] = []
		DATA['Chaining Unassigned'] = []
		DATA['Hooping Unassigned'] = []						
		DATA['K-Means Unassigned'] = []
		DATA['Odd Unassigned'] = []
		DATA['Odd Range Unassigned'] = []
		DATA['Converse Unassigned'] = []

		for data in INPUTDATA:
			DATA['Emulation'].append(data[0])
			DATA['Minimum SNR'].append(data[1])
			DATA['Maximum SNR'].append(data[2])
			DATA['Median RE'].append(data[3])

			DATA['Myopic CH'].append(data[4])
			DATA['Backhauling CH'].append(data[5])	 			
			DATA['MSGBACK CH'].append(data[6])
			DATA['MSLBACK CH'].append(data[7])
			DATA['Redistribution CH'].append(data[8])
			DATA['Chaining CH'].append(data[9])
			DATA['Hooping CH'].append(data[10])	 			
			DATA['K-Means CH'].append(data[11])
			DATA['Odd CH'].append(data[12])
			DATA['Odd Range CH'].append(data[13])
			DATA['Converse CH'].append(data[14])

			DATA['Myopic I-CH'].append(data[15])
			DATA['Backhauling I-CH'].append(data[16]) 			
			DATA['MSGBACK I-CH'].append(data[17])
			DATA['MSLBACK I-CH'].append(data[18])
			DATA['Redistribution I-CH'].append(data[19])
			DATA['Chaining I-CH'].append(data[20])
			DATA['Hooping I-CH'].append(data[21]) 			
			DATA['K-Means I-CH'].append(data[22])
			DATA['Odd I-CH'].append(data[23])
			DATA['Odd Range I-CH'].append(data[24])
			DATA['Converse I-CH'].append(data[25])

			DATA['Myopic Unassigned'].append(data[26])
			DATA['Backhauling Unassigned'].append(data[27])						
			DATA['MSGBACK Unassigned'].append(data[28])
			DATA['MSLBACK Unassigned'].append(data[29])
			DATA['Redistribution Unassigned'].append(data[30])
			DATA['Chaining Unassigned'].append(data[31])
			DATA['Hooping Unassigned'].append(data[32])						
			DATA['K-Means Unassigned'].append(data[33])
			DATA['Odd Unassigned'].append(data[34])
			DATA['Odd Range Unassigned'].append(data[35])
			DATA['Converse Unassigned'].append(data[36])
		
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
	End = 20

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
			Network.CreateNodes('./RF Planning/Location/Study/' + Place + '.json', Place, ClusterRadius = 1000, ServiceProvider = ServiceProvider, Results = True)

			#MODELS
			print('\n#{0:5}: Running Models!'.format(i))
			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Myopic';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Backhauling(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Backhauling';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Myopic(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Balancing(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'MSGBACK';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Greedy(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'MSLBACK';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Successive(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Redistribution';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Myopic(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Balancing(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Redistribute(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Chaining';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Myopic(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Balancing(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Chaining(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Hooping';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Myopic(NODES, NETWORK, UNASSIGNED, DATA, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Balancing(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			NODES, NETWORK, UNASSIGNED, DATA = Model.Hoop(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius, ServiceProvider = ServiceProvider)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'K-Means';
			NODES, NETWORK, UNASSIGNED, DATA = Model.KMeans(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Odd';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Odd(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Odd Range';
			NODES, NETWORK, UNASSIGNED, DATA = Model.OddRange(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			NODES, NETWORK, UNASSIGNED, DATA = Network.Network()
			Technique = 'Converse';
			NODES, NETWORK, UNASSIGNED, DATA = Model.Converse(NODES, NETWORK, UNASSIGNED, DATA, Network.Median_ResidualEnergy, Network.MaximumClusterHeads, Network.Maximum_SNR, Network.Minimum_SNR, ClusterRadius = Network.ClusterRadius)
			CHs, ICHs, ECH = Display.ConnectNodes(NODES = NODES, NETWORK = NETWORK, UNASSIGNED = UNASSIGNED)
			Heads.append(CHs); Unassigned.append(len(UNASSIGNED)); Interclusters.append(ICHs); Empty.append(ECH)
			Display.SaveNetworkJSON(NODES, NETWORK, UNASSIGNED, Counter = i, Date = Date, Time = Time, Radius = Network.ClusterRadius, Model = Technique, Distribution = Distribution, Area = Place)
			NODES.clear(); NETWORK.clear(); UNASSIGNED.clear();
			NODES = None; NETWORK = None; UNASSIGNED = None; DATA = None;

			bar.update(i)
			RESULTS.append([i, Network.Minimum_SNR, Network.Maximum_SNR, Network.Median_ResidualEnergy] + Heads + Interclusters + Unassigned + Empty)
			del Network;

	Emulation.SaveToExcel(RESULTS, FileName = Place, SheetName = Distribution, Distribution=Distribution)

	print('\n\n-----DONE-----')

