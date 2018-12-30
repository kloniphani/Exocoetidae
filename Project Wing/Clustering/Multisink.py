"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       October 19, 2018
Copyrights:  2017 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""

from numpy import *
from networkx import *
from geopy import distance
import json, io, progressbar

from Clustering.Algorithms import *

class Multisink(object):
	"""description of class"""

	def InitialiseNodes(NODES, BestSNR = 0, Height = 0, Results = False):
		"""
		@Height = 0, White
				  1, Gray
				  2, Black
		"""
		TrackA = 0;
		with progressbar.ProgressBar(max_value = progressbar.UnknownLength) as bar:
			for node in NODES.values():
				node.SetGraphColor('white')
				for other in NODES.values():
					try:
						if (node.Name != other.Name) and (node.MESH[other.Name] >= BestSNR):
							NODES[node.Id].LINKS.append(other)
						if Results == True: print('{0} {1} {2}'.format(node.MESH[other.Name], (BestSNR), (node.MESH[other.Name] >= float(BestSNR))))
					except:
						PredictedSNR = float64(log(node.ComputeSNR(other.Position, Results = Results))/log(20))
						if Results == True: print('{0} {1} {2}'.format((float64(PredictedSNR).item()), (BestSNR), (float64(PredictedSNR).item() >= float(BestSNR)))) 
						if (node.Id != other.Id) and (PredictedSNR >= BestSNR):
							NODES[node.Id].LINKS.append(other)
					TrackA += 1
					bar.update(TrackA)

		return NODES

	def HasNonVisitedNode(NODES, Type = None, Results = False):
		for node in NODES.values():
			if node.Type == Type: return True;
		return False

	def HasNonVisitedNeighbour(self, Node, Type = None, Results = False):
		for link in Node.LINKS:
			if link.Type == Type: return True;
		return False

	def GreedySinkNodeSelectionWithSinksTreeBalancing(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'LAP',
				Median_ResidualEnergy = None, MaximumClusterHeads = None, Maximum_SNR = None, Minimum_SNR = None, NumberOfNodes = None, ClusterRadius = 100,
				Theta = 0.5, Beta = 0.5, Alpha= 0.5, Profit = 0, Best_SNR = 10,
				HopLimit = -1):	 
		print("\nGreedy Sink Node Selection With Sinks Tree Balancing Model at [{0}] Processing".format(Mode))
		if Median_ResidualEnergy is None and MaximumClusterHeads is None and Maximum_SNR is None and Minimum_SNR is None:
			#Sorting the Nodes in Descending order based on their SNR
			TEMP = list(NODES.values());
			TEMP.sort(key = lambda node: node.SNR, reverse = True) 

			UNASSIGNED = [node.Id for node in TEMP]

			Minimum_SNR = TEMP[-1].SNR
			Maximum_SNR = TEMP[0].SNR
			Deviation_SNR = std([node.SNR for node in TEMP])
			Average_SNR = average([node.SNR for node in TEMP])

			Median_ResidualEnergy = median([node.ResidualEnergy for node in TEMP])
			Average_ResidualEnergy = average([node.ResidualEnergy for node in TEMP])
			Maximum_ResidualEnergy = max([node.ResidualEnergy for node in TEMP])
		
		TrackA = 1; EndA = len(UNASSIGNED); White = 0; Gray = 1; Black = 2;
		with progressbar.ProgressBar(max_value = progressbar.UnknownLength) as bar:
			#Selecting the Base Station and Creating the Network Graph
			Total = 2; 
			NODES = Multisink.InitialiseNodes(NODES, BestSNR = 50)
			NODES, NETWORK, UNASSIGNED, BASESTATIONS = Algorithms.SelectBaseStations(NODES, NETWORK, UNASSIGNED, Total)
			for id in BASESTATIONS:
				NODES[id].SetGraphHeight(-1)
				NODES[id].SetGraphColor('olive')

			G = Algorithms.CreateGraph(NODES, NETWORK, UNASSIGNED, Links = True)

			#Finding the Profit
			if Mode == 'LAP':
				Profit, Average_GD_Basestations, Average_GD_Nodes = Algorithms.FindLAPProfit(NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, Average_ResidualEnergy, Theta, Beta, Alpha)
				REWARDS = Algorithms.AllLAPRewards(NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, Average_GD_Basestations, Average_GD_Nodes)
			elif Mode == 'UAV':
				Profit = Algorithms.FindUAVProfit(NODES, NETWORK, UNASSIGNED, Maximum_SNR, Average_SNR, Maximum_SNR, Average_ResidualEnergy, Maximum_ResidualEnergy, Alpha, Beta)
				REWARDS = Algorithms.AllUAVRewards(NODES, NETWORK, UNASSIGNED, Maximum_SNR, Average_ResidualEnergy, Maximum_ResidualEnergy, Alpha, Beta)

			while(Multisink.HasNonVisitedNode(NODES) == True):
				#Selecting the best Sink candidate node
				if len(UNASSIGNED) == 0:
					break;

				for id in UNASSIGNED:
					Root = None;	   					
					if NODES[id].Type == None and (Profit <= REWARDS[id]):
						NODES[id].ChangeToClusterHead()
						NETWORK[id] = NODES[id]
						Root = NODES[id];

					if Root is not None:
						for child in UNASSIGNED:
							if str(child) is not str(Root.Id):
								PATH =  list(astar_path(G, Root.Id, child, weight='length'))
								NODES[Root.Id].AddMember(NODES[PATH[0]])
								for i in range(1, len(PATH)):
									NODES[PATH[i]].SetHoopHead(NODES[PATH[i-1]])
									if str(Root.Id) is not str(PATH[i]):	  
										NODES[PATH[i-1]].ChangeToChainNode()
										NETWORK[PATH[i-1]] = NODES[PATH[i-1]]
									NODES[PATH[i-1]].AddMember(NODES[PATH[i]])	 							
									NETWORK[PATH[i-1]].AddMember(NODES[PATH[i]])
									
								for i in PATH:
									if i in UNASSIGNED:
										UNASSIGNED.remove(i)
						if len(NODES[Root.Id].MEMBERS) == -9:
							NODES[Root.Id].ChangeToNode();
							UNASSIGNED.append(Root.Id)
							del NETWORK[Root.Id]
				
				TrackA += 1
				bar.update(TrackA)

		TrackA = 1; EndA = len(UNASSIGNED); White = 0; Gray = 1; Black = 2;
		with progressbar.ProgressBar(max_value = progressbar.UnknownLength) as bar:
			TrackA += 1
			bar.update(TrackA)

		return NODES, NETWORK, UNASSIGNED, DATA;