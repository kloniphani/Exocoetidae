"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       October 19, 2018
Copyrights:  2017 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""

from . import *

from numpy import *
from networkx import *
from geopy import distance
import json, io, progressbar

class Backbone(object):
	"""Class Description"""

	def InitialiseNodes(self, NODES, Height = 0, BestSNR = 30, Results = False):
		"""
		@Height = 0, White
				  1, Gray
				  2, Black
		"""

		for node in NODES:
			node.SetGraphHeight(Height)
			for other in NODES:	
				if node.Id != other.Id and node != other and node.ComputeSNR(other.Position, Results = Results) >= BestSNR:
					node.LINKS.append(other)

		return NODES

	def HasWhiteNode(self, NODES, Height = 0, Results = False):
		for node in NODES:
			if node.GrapHeight == Height: return True;
		return False

	def HasWhiteNodeNeighbour(self, Node, Height = 0, Results = False):
		for link in Node.LINKS:
			if link.GraphHeight == Height: return True;
		return False

	def GraphColouringWithHeightControl(self, NODES, NETWORK, UNUSSIGNED, DATA, 
									 Mode = 'LAP',
									 Median_ResidualEnergy = None, MaximumClusterHeads = None, Maximum_SNR = None, Minimum_SNR = None, NumberOfNodes = None, ClusterRadius = 100,
									 Theta = 0.5, Beta = 0.5, Profit = 0, Best_SNR = 10):
		
		"""
		"""
		print("\nGraph Colouring With Height Control Model at [{0}] Processing".format(Mode))
		if Median_ResidualEnergy is None and MaximumClusterHeads is None and Maximum_SNR is None and Minimum_SNR is None:
			#Sorting the Nodes in Descending order based on their SNR
			TEMP = list(NODES.values());
			TEMP.sort(key = lambda node: node.SNR, reverse = True) 

			UNUSSIGNED = [node.Id for node in TEMP]

			Minimum_SNR = TEMP[-1].SNR
			Maximum_SNR = TEMP[0].SNR
			Deviation_SNR = std([node.SNR for node in TEMP])
			Average_SNR = average([node.SNR for node in TEMP])

			Median_ResidualEnergy = median([node.ResidualEnergy for node in TEMP])
			Average_ResidualEnergy = average([node.ResidualEnergy for node in TEMP])
			Maximum_ResidualEnergy = max([node.ResidualEnergy for node in TEMP])

		#Selecting the Base Station and Creating the Network Graph
		Total = 2
		NODES, NETWORK, UNUSSIGNED, BASESTATIONS = Algorithms.SelectBaseStations(NODES, NETWORK, UNUSSIGNED, Total)
		G = Algorithms.CreateGraph(NODES, NETWORK, UNUSSIGNED)

		#Finding the Profit
		if Mode == 'LAP':
			Profit = Algorithms.FindLAPProfit(NODES, NETWORK, UNUSSIGNED, BASESTATIONS, G)

		TrackA = 0; EndA = len(UNUSSIGNED); White = 0; Gray = 1; Black = 2;
		with progressbar.ProgressBar(max_value = EndA) as bar:
			NetworkTree = Graph()

			for key, value in NODES:
				if key not in BASESTATIONS and value.GraphHeight == White and (Profit <= Algorithms.LAPReward(value, NODES, NETWORK, UNUSSIGNED, BASESTATIONS, G)):
					value.SetGraphHeight(Gray)
					for link in value.LINKS:


			TrackA += 1
			bar.update(TrackA)
			