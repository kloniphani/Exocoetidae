"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       January 4, 2019
Copyrights:  2017 ISAT, Department of Computer Science
			University of the Western Cape, Bellville, ZA
"""

from numpy import *
from networkx import *
from geopy import distance
import json, io, progressbar

from Clustering.Algorithms import *

class Orginising(object):
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