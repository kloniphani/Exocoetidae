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
									 Theta = 0.5, Beta = 0.5, Alpha = 0.5, Profit = 0, Best_SNR = 0):
		
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
			NODES = Backbone.InitialiseNodes(NODES, BestSNR = 50)
			#Selecting the Base Station and Creating the Network Graph
			Total = 2; 

			bar.update(TrackA)

			NODES, NETWORK, UNASSIGNED, BASESTATIONS = Algorithms.SelectBaseStations(NODES, NETWORK, UNASSIGNED, Total)
			for id in BASESTATIONS:
				NODES[id].SetGraphHeight(-1)
				NODES[id].SetGraphColor('olive')

			G = Algorithms.CreateGraph(NODES, NETWORK, UNASSIGNED, Links = True)

			#Finding the Profit
			if Mode == 'LAP':
				Profit, Average_GD_Basestations, Average_GD_Nodes = Algorithms.FindLAPProfit(NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, Average_ResidualEnergy, Theta, Beta, Alpha)
				REWARDS = Algorithms.AllLAPRewards(NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, 
			   Average_GD_Basestations, Average_GD_Nodes)
			elif Mode == 'UAV':
				Profit = Algorithms.FindUAVProfit(NODES, NETWORK, UNASSIGNED, Maximum_SNR, Average_SNR, Maximum_SNR, Average_ResidualEnergy, Maximum_ResidualEnergy, Alpha, Beta)
				REWARDS = Algorithms.AllUAVRewards(NODES, NETWORK, UNASSIGNED, Maximum_SNR, Average_ResidualEnergy, Maximum_ResidualEnergy, Alpha, Beta)


			for key, value in NODES.items():
				if key not in BASESTATIONS and key in UNASSIGNED and value.GraphColor == 'white' and (Profit <= REWARDS[key]):
					NODES[key].SetGraphColor('gray')
					#UNASSIGNED.remove(key)

			while(Backbone.HasWhiteNode(NODES) == True):
				#Picking the best Gray node
				if len(UNASSIGNED) < 1: break;
				key = 1; BestGrayNode = NODES[UNASSIGNED[0]]
				while(key < len(UNASSIGNED)):
					if(REWARDS[BestGrayNode.Id] < REWARDS[UNASSIGNED[key]]):
						BestGrayNode = NODES[UNASSIGNED[key]]
					else:
						key += 1

				NODES[BestGrayNode.Id].SetGraphColor('black')
				NODES[BestGrayNode.Id].ChangeToClusterHead()
				NETWORK[BestGrayNode.Id] = NODES[BestGrayNode.Id]

				for link in NODES[BestGrayNode.Id].LINKS:
					if (link.Id in UNASSIGNED):
						NODES[link.Id].SetGraphColor('gray')
						NODES[link.Id].SetGraphHeight(BestGrayNode.GraphHeight + 1)
						NODES[link.Id].ChangeToClusterMember(BestGrayNode)
						NETWORK[BestGrayNode.Id].MEMBERS.append(NODES[link.Id])
						UNASSIGNED.remove(link.Id)
				
				UNASSIGNED.remove(BestGrayNode.Id)

				TrackA += 1
				bar.update(TrackA)
		return NODES, NETWORK, UNASSIGNED, DATA;
			