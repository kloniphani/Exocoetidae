"""         
Authors:     Kloni Maluleke (Msc), kloniphani@gmail.com
Date:        November 11, 2018
Copyrights:  2017 ISAT, Department of Computer Science
             University of the Western Cape, Bellville, ZA
"""
from . import *

from numpy import *
from networkx import *

from Clustering.Distribution import *

import progressbar

class Algorithms(object):
	"""description of class"""

	def SelectBaseStations(NODES, NETWORK, UNASSIGNED, Total, Results = False):
		BASESTATIONS = []; Count = 0;
		while Count < Total:
			node = random.choice(UNASSIGNED)
			BASESTATIONS.append(node) 
			NODES[node].ChangeToBaseStation()
			UNASSIGNED.remove(node)
			Count += 1
		return NODES, NETWORK, UNASSIGNED, BASESTATIONS;

	def CreateGraph(NODES, NETWORK, UNASSIGNED, Links = False, Results = False):
		G = Graph()
		G.add_nodes_from([node.Id for node in NODES.values()])
		if Links == True:
			for node in NODES.values(): 
				for link in node.LINKS:
					if str(node.Id) is not str(link.Id) and (node.Type != -2 and link.Type != -2):
						G.add_edge(node.Id, link.Id, weight = node.Distance(link.Position, Type = '2D', Results = Results))
		elif Links == False:
			for node in NODES.values():
				for s in NODES.values(): 
					if str(node.Id) is not str(s.Id):
						G.add_edge(s.Id, NODES[node.Id].Id, weight = s.Distance(NODES[node.Id].Position, Type = '2D', Results = Results))	
		return G

	def FindLAPProfit(NODES, NETWORK, UNASSIGNED, BASESTATIONS, G,
				   Average_ResidualEnergy,
				   Theta = 0.5, Beta = 0.5, Alpha = 0.5, Results = False):
		#Average Geodesic Distance
		_GDS = 0;  _GDN = 0; Count = 1;
		for i in BASESTATIONS:
			for j in BASESTATIONS: 				
				try:
					if i != j:
						_GDS += NODES[i].Distance(NODES[j].Position, Type = '2D', Results = Results)
				except:
					continue
		
		for i in UNASSIGNED:
			for j in UNASSIGNED:   				
				try:  					
					if str(i) is not str(j):
						Temp = astar_path_length(G, i, j)
						#Temp += shortest_path_length(G, i, j)
						_GDN += Temp
						if Results == True: print("- Path from Node #{0} to #{1} is {2} in length".format(i, j, Temp))
				except:
					continue

		Average_GD_Basestations = _GDS/len(BASESTATIONS)
		Average_GD_Nodes = _GDN/len(UNASSIGNED)

		Profit = sqrt(len(BASESTATIONS)/(((Theta*Average_GD_Basestations) - Average_GD_Basestations) **2)) + sqrt(len(UNASSIGNED)/(((Beta*Average_GD_Nodes) - Average_GD_Nodes) **2)) + (Alpha * Average_ResidualEnergy)
		return Profit, Average_GD_Basestations, Average_GD_Nodes;

	def LAPReward(node, NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, 
			   Average_GD_Basestations, Average_GD_Nodes, Results = False):
		_GDS = 0; _GDN = 0;
		for i in BASESTATIONS:
			_GDS += NODES[i].Distance(node.Position, Type = '2D', Results = False)

		for i in NODES.values():
			try:
				if (str(i.Id) is not str(node.Id)):
					_GDN += astar_path_length(G, node.Id, i.Id)
					#_GDN += shortest_path_length(G, node.Id, i.Id)
			except:
				continue

		#Checking the standard deviation.
		try:
			Average_GDS = sqrt((len(BASESTATIONS) - 1)/((_GDS - Average_GD_Basestations) **2))
		except ZeroDivisionError: 
			Average_GDS = 0;
		try:
			Average_GDN = sqrt((len(NODES) - len(BASESTATIONS) - 1)/((_GDN - Average_GD_Nodes) **2))
		except ZeroDivisionError:
			Average_GDN = 0;
					
		return Average_GDS + Average_GDN + node.ResidualEnergy;

	def AllLAPRewards(NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, Average_GD_Basestations, Average_GD_Nodes):
		REWARDS = {}
		for key, value in NODES.items():
			REWARDS[key] = Algorithms.LAPReward(value, NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, Average_GD_Basestations, Average_GD_Nodes)
		return REWARDS;

	def FindUAVProfit(NODES, NETWORK, UNASSIGNED,
			   Average_SNR, Maximum_SNR, Average_ResidualEnergy, Maximum_ResidualEnergy,
			   Alpha = 0.5, Beta = 0.5, Results = False):
		Profit = (Alpha * Average_SNR) + (Beta * (Maximum_ResidualEnergy - Average_ResidualEnergy))
		return Profit;

	def UAVReward(node, NODES, NETWORK, UNASSIGNED,
			   Maximum_SNR, Average_ResidualEnergy, Maximum_ResidualEnergy,
			   Alpha = 0.5, Beta = 0.5, Results = False):
		Reward = (Alpha * (node.SNR)) + (Beta * (node.ResidualEnergy - Average_ResidualEnergy));
		return Reward;

	def AllUAVRewards(NODES, NETWORK, UNASSIGNED,
			   Maximum_SNR, Average_ResidualEnergy, Maximum_ResidualEnergy, 
			   Alpha = 0.5, Beta = 0.5, Results = False):
		REWARDS = {}
		for key, value in NODES.items():
			REWARDS[key] = Algorithms.UAVReward(value, NODES, NETWORK, UNASSIGNED, Maximum_SNR, Average_ResidualEnergy, Maximum_ResidualEnergy, Alpha = Alpha, Beta = Beta)
		return REWARDS;

	def GenerateRandomLinks(NODES, Results = False):
		ResidualEnergies, SNRs = Distribution.Normal() # Random Values
		BestSNR = quantile(list(node.SNR for node in list(NODES.values())), 0.65)

		if Results is True:
			print("Generating Random Links")

		Track = 0;
		with progressbar.ProgressBar(max_value = len(NODES)) as bar:		 
			for	node in NODES.values():
				for link in NODES.values():
					if str(node.Id)	is not str(link.Id):
						SNR = random.choice(SNRs)
						if(SNR > BestSNR):
							NODES[node.Id].LINKS.append(link)

			Track += 1
			bar.update(Track)
		return NODES;

