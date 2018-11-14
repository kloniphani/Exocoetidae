"""         
Authors:     Kloni Maluleke (Msc), kloniphani@gmail.com
Date:        November 11, 2018
Copyrights:  2017 ISAT, Department of Computer Science
             University of the Western Cape, Bellville, ZA
"""
from . import *

from numpy import *
from networkx import *

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

	def CreateGraph(NODES, NETWORK, UNASSIGNED, Results = False):
		G = Graph()
		G.add_nodes_from([node.Id for node in NODES.values()])
		for node in UNASSIGNED:
			for s in NODES.values(): 
				if node is not s.Id:
					G.add_edge(s.Id, NODES[node].Id, weight = s.Distance(NODES[node].Position, Type = '2D', Results = False))	
		return G

	def FindLAPProfit(NODES, NETWORK, UNASSIGNED, BASESTATIONS, G,
				   Average_ResidualEnergy,
				   Theta, Beta, Alpha, Results = False):
		#Average Geodesic Distance
		_GDS = 0;  _GDN = 0; Count = 1;
		for i in BASESTATIONS:
			for j in BASESTATIONS:
				if i != j:
					_GDS += NODES[i].Distance(NODES[j].Position, Type = '2D', Results = False)
	
		for i in UNASSIGNED:
			for j in UNASSIGNED:
				if i is not j:
					_GDN += astar_path_length(G, i, j)

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
			if (str(i.Id) is not str(node.Id)) and (i.Id not in BASESTATIONS):
				_GDN += astar_path_length(G, node.Id, i.Id)
					
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

	def AllRewards(NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, Average_GD_Basestations, Average_GD_Nodes):
		REWARDS = {}
		for key, value in NODES.items():
			REWARDS[key] = Algorithms.LAPReward(value, NODES, NETWORK, UNASSIGNED, BASESTATIONS, G, Average_GD_Basestations, Average_GD_Nodes)
		return REWARDS;