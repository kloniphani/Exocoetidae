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

	def SelectBaseStations(self, NODES, NETWORK, UNUSSIGNED, Total, Results = False):
		BASESTATIONS = []; Count = 0;
		while Count < Total:
			node = random.choice(UNUSSIGNED)
			BASESTATIONS.append(node) 
			NODES[node].ChangeToBaseStation()
			UNUSSIGNED.remove(node)
			Count += 1
		return NODES, NETWORK, UNUSSIGNED, BASESTATIONS;

	def CreateGraph(self, NODES, NETWORK, UNUSSIGNED, Results = False):
		G = Graph()
		G.add_nodes_from([node.Id for node in TEMP])
		for node in UNUSSIGNED:
			for s in NODES.values(): 
				if node is not s.Id:
					G.add_edge(s.Id, NODES[node].Id, weight = s.Distance(NODES[node].Position, Type = '2D', Results = False))	
		return G

	def FindLAPProfit(self, NODES, NETWORK, UNUSSIGNED, BASESTATIONS, G, Results = False):
		#Average Geodesic Distance
		_GDS = 0;  _GDN = 0; Count = 1;
		for i in BASESTATIONS:
			for j in BASESTATIONS:
				if i != j:
					_GDS += NODES[i].Distance(NODES[j].Position, Type = '2D', Results = False)
	
		for i in UNUSSIGNED:
			for j in UNUSSIGNED:
				if i is not j:
					_GDN += astar_path_length(G, i, j)

		Average_GD_Basestations = _GDS/len(BASESTATIONS)
		Average_GD_Nodes = _GDN/len(UNUSSIGNED)

		Profit = sqrt(len(BASESTATIONS)/(((Theta*Average_GD_Basestations) - Average_GD_Basestations) **2)) + sqrt(len(UNUSSIGNED)/(((Beta*Average_GD_Nodes) - Average_GD_Nodes) **2)) + (Alpha * Average_ResidualEnergy)
		return Profit

	def LAPReward(self, node, NODES, NETWORK, UNUSSIGNED, BASESTATIONS, G, Results = False):
		_GDS = 0; _GDN = 0;
		for i in BASESTATIONS:
			_GDS += NODES[i].Distance(node.Position, Type = '2D', Results = False)

		for i in NODES.values():
			if (str(i.Id) is not str(node.Id)) and (i.Id not in BASESTATIONS):
				_GDN += astar_path_length(G, UNUSSIGNED[index], i.Id)
					
		#Checking the standard deviation.
		Average_GDS = sqrt((len(BASESTATIONS) - 1)/((_GDS - Average_GD_Basestations) **2))
		Average_GDN = sqrt((len(NODES) - len(BASESTATIONS) - 1)/((_GDN - Average_GD_Nodes) **2))
					
		return Average_GDS + Average_GDN + node.ResidualEnergy;