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

class Multisink(object):
	"""description of class"""
	def Greedy(NODES, NETWORK, UNASSIGNED, DATA, 
				Median_ResidualEnergy = None, MaximumClusterHeads = None, Maximum_SNR = None, Minimum_SNR = None, NumberOfNodes = None, ClusterRadius = 100,
				Theta = 0.5, Beta = 0.5, Profit = 0, Best_SNR = 10):
		pass

	def Successive(NODES, NETWORK, UNASSIGNED, DATA, 
				Median_ResidualEnergy = None, MaximumClusterHeads = None, Maximum_SNR = None, Minimum_SNR = None, NumberOfNodes = None, ClusterRadius = 100,
				Theta = 0.5, Beta = 0.5, Profit = 0, Best_SNR = 10):
		pass

