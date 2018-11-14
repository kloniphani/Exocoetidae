"""         
Authors:     Kloni Maluleke (Msc), kloniphani@gmail.com
Date:        October 19, 2018
Copyrights:  2017 ISAT, Department of Computer Science
             University of the Western Cape, Bellville, ZA
"""

from Clustering.Algorithms import *

from numpy import *
from networkx import *

import progressbar

class Backbone(object):
	"""Class Description"""

	def InitialiseNodes(NODES, BestSNR = 2, Height = 0, Results = False):
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
					PredictedSNR = ceil(log(node.ComputeSNR(other.Position, Results = Results))/log(20))
					if Results == False: print('{0} {1} {2}'.format(type(float64(PredictedSNR).item()), float64(BestSNR), greater_equal([PredictedSNR], [float64(BestSNR)]))) 
					if (node.Id != other.Id) and (PredictedSNR >= float64(BestSNR)):
						print('{0}'.format(PredictedSNR)) 
						NODES[node.Id].LINKS.append(other)
						print('Hello')
					TrackA += 1
					bar.update(TrackA)

		return NODES

	def HasWhiteNode(NODES, Height = 0, Results = False):
		for node in NODES.values():
			if node.GraphHeight == Height: return True;
		return False

	def HasWhiteNodeNeighbour(self, Node, Height = 0, Results = False):
		for link in Node.LINKS:
			if link.GraphHeight == Height: return True;
		return False

	def GraphColouringWithHeightControl(NODES, NETWORK, UNASSIGNED, DATA, 
									 Mode = 'LAP',
									 Median_ResidualEnergy = None, MaximumClusterHeads = None, Maximum_SNR = None, Minimum_SNR = None, NumberOfNodes = None, ClusterRadius = 5,
									 Theta = 0.5, Beta = 0.5, Alpha = 0.5, Profit = 0, Best_SNR = 10):
		
		"""
		"""
		print("\nGraph Colouring With Height Control Model at [{0}] Processing".format(Mode))
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
			NODES = Backbone.InitialiseNodes(NODES, BestSNR = 4)
			#Selecting the Base Station and Creating the Network Graph
			Total = 2; 

			bar.update(TrackA)

			NODES, NETWORK, UNASSIGNED, BASESTATIONS = Algorithms.SelectBaseStations(NODES, NETWORK, UNASSIGNED, Total)
			G = Algorithms.CreateGraph(NODES, NETWORK, UNASSIGNED)


			#Finding the Profit
			if Mode == 'LAP':
				Profit, Average_GD_Basestations, Average_GD_Nodes = Algorithms.FindLAPProfit(NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, Average_ResidualEnergy, Theta, Beta, Alpha)

			REWARDS = Algorithms.AllRewards(NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, 
			   Average_GD_Basestations, Average_GD_Nodes)

			NetworkTree = Graph();
			NetworkTree.add_nodes_from([node.Id for node in NODES.values()])

			for key, value in NODES.items():
				if Mode == 'LAP':
					if key not in BASESTATIONS and key in UNASSIGNED and value.GraphColor == 'white' and (Profit <= REWARDS[key]):
						NODES[value.Id].SetGraphColor('gray')
						#UNASSIGNED.remove(key)

			while(Backbone.HasWhiteNode(NODES) == True):
				#Picking the best Gray node
				if len(UNASSIGNED) < 1: break;
				key = 1; BestGrayNode = NODES[UNASSIGNED[0]]
				while(key < len(UNASSIGNED)):
					if(REWARDS[BestGrayNode.Id] < REWARDS[UNASSIGNED[key]]):
						BestGrayNode = NODES[UNASSIGNED[key]]
						del UNASSIGNED[key]
					else:
						key += 1

				del UNASSIGNED[0]

				NODES[BestGrayNode.Id].SetGraphColor('black')
				NODES[BestGrayNode.Id].ChangeToClusterHead()
				NETWORK[BestGrayNode.Id] = NODES[BestGrayNode.Id]

				for link in NODES[BestGrayNode.Id].LINKS:
					NODES[link.Id].SetGraphColor('gray')
					NODES[link.Id].SetgraphHeight(BestGrayNode.GrapgHeight + 1)
					NetworkTree.add_edge(NODES[BestGrayNode.Id].Id, link.Id, weight = link.Distance(NODES[BestGrayNode.Id].Position, Type = '2D', Results = False))	
					NODES[link.Id].ChangeToClusterMember(BestGrayNode)
					NETWORK[BestGrayNode.Id].MEMBERS.append(NODES[link.Id])
						
				TrackA += 1
				bar.update(TrackA)
		return NODES, NETWORK, UNASSIGNED, DATA, G, NetworkTree;
			