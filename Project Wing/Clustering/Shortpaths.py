"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       January 3, 2019
Copyrights:  2017 ISAT, Department of Computer Science
			University of the Western Cape, Bellville, ZA
"""

from numpy import *
from networkx import *
from geopy import distance
import json, io, progressbar

from Clustering.Algorithms import *

class Shortpaths(object):
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

	def GreedySinkNodeSelection(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'LAP',
				Median_ResidualEnergy = None, MaximumClusterHeads = None, Maximum_SNR = None, Minimum_SNR = None, NumberOfNodes = None, ClusterRadius = 100,
				Theta = 0.5, Beta = 0.5, Alpha= 0.5, Profit = 0, Best_SNR = 10,
				HopLimit = -1):	 
		print("\nGreedy Sink Node Selection With Sinks Network Shortest Path Balancing Model at [{0}] Processing".format(Mode))
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

			while((Multisink.HasNonVisitedNode(NODES) == True) and (TrackA <= (len(NODES.values())))):
				for id in UNASSIGNED:
					Root = None;	   					
					if NODES[id].Type == None and (Profit <= REWARDS[id]):
						NODES[id].ChangeToRoot()
						NETWORK[id] = NODES[id]
						Root = NODES[id];

					if Root is not None:
						for child in UNASSIGNED:
							if str(child) is not str(Root.Id):
								PATH =  list(astar_path(G, Root.Id, child, weight='length')) 
								NODES[Root.Id].AddPath(PATH)
								#NETWORK[Root.Id].AddPath(PATH)

								for sink in PATH[1:]:
									NODES[Root.Id].AddMember(NODES[sink])
									#NETWORK[Root.Id].AddMember(NODES[sink])  	 							
									
								for i in PATH:
									if i in UNASSIGNED:
										NODES[i].ChangeToClusterMember(NODES[Root.Id])
										NODES[i].ChangeToChainNode()
										UNASSIGNED.remove(i)  	
						
						if len(NETWORK[Root.Id].SINKPATHS) == -5:	 
							NODES[Root.Id].ChangeToNode();
							NODES[Root.Id].Type = None;
							UNASSIGNED.append(Root.Id)
							del NETWORK[Root.Id]

						if Root.Id in UNASSIGNED:
							UNASSIGNED.remove(Root.Id)

					TrackA += 1; bar.update(TrackA);
		return NODES, NETWORK, UNASSIGNED, DATA;

	def BalanceNetwork(NODES, NETWORK, UNASSIGNED, DATA, 
				 MaximumClusterHeads = None, NumberOfNodes = None, ClusterRadius = 100,
				 HopDistance = 50, HopLimit = 2, Crowdness = 8,
				 Mode = 'All'):
		#BALANCING THE TREE
		TrackA = 1; EndA = len(UNASSIGNED); White = 0; Gray = 1; Black = 2;
		with progressbar.ProgressBar(max_value = progressbar.UnknownLength) as bar:
			G = Algorithms.CreateGraph(NODES, NETWORK, UNASSIGNED, Links = True)
			TrackA += 1; bar.update(TrackA);

			if Mode == 'All' or  Mode == 'Distance':
				#Redistribution of nodes to trees based on distance in number of hops
				for node in list(NETWORK.values()):
					if node.Type == -1:
						distance = 0; row = 0;
						for path in node.SINKPATHS:
							for i in range(len(path)-1):
								distance += NODES[path[i]].Distance(NODES[path[i + 1]].Position)
							child = path[-1]
							if distance > HopDistance:
								for n in list(NODES.values()):
									d = 0;
									if (str(n.Id) is not str(node.Id)) and (n.Type == -1):
										PATH =  list(astar_path(G, n.Id, NODES[child].Id, weight='length')) 
										
										for i in range(len(PATH)-1):
											d += NODES[PATH[i]].Distance(NODES[PATH[i + 1]].Position)
											
										if d + NODES[node.Id].Distance(NODES[n.Id].Position) < HopDistance:
											NODES[n.Id].AddPath(PATH)
											#NETWORK[n.Id].AddPath(PATH)	
											for s in PATH[1:]:
												NODES[n.Id].AddMember(NODES[s])
												NODES[node.Id].RemoveMember(NODES[s])
												#NETWORK[n.Id].AddMember(NODES[s])
												
											#if child in NODES[node.Id].MEMBERS:
											#	NODES[node.Id].MEMBERS.remove(child)
											if path in 	NODES[node.Id].SINKPATHS:
												NODES[node.Id].SINKPATHS.remove(path)
											#del NODES[node.Id].SINKPATHS[row]
												
											#if child in NETWORK[node.Id].MEMBERS:
											#	NETWORK[node.Id].MEMBERS.remove(child)
											#	del NETWORK[node.Id].SINKPATHS[row]
											break;
							else:
								row += 1 
					TrackA += 1; bar.update(TrackA);

			if Mode == 'All' or Mode == 'Crowdness':
				#Redistribution of nodes to trees based on crowdness (nodes count expressing the maximum number of nodes that a tree is will to carry)
				TEMP = list(NETWORK.values());
				TEMP.sort(key = lambda node: len(node.MEMBERS), reverse = False) 
				Track = 0;
				
				for node in list(NETWORK.values()):
					if node.Type == -1 and len(node.MEMBERS) > Crowdness:
						count = 0;
						while(count < (len(node.MEMBERS) - Crowdness) and Track < 100):
							for sink in node.MEMBERS:
								for n in TEMP:
									if (str(n.Id) is not str(node.Id)) and ( len(n.MEMBERS) < Crowdness) and n.Type == -1:
										PATH =  list(astar_path(G, n.Id, sink.Id, weight='length')) 
										NODES[n.Id].AddPath(PATH)

										for s in PATH[1:]:
											NODES[n.Id].AddMember(NODES[s])
											NODES[node.Id].RemoveMember(NODES[s])

										NODES[node.Id].RemoveMember(NODES[sink.Id])
										for path in NODES[node.Id].SINKPATHS:
											if str(path[-1]) is str(sink.Id):
												NODES[node.Id].SINKPATHS.remove(path);
												count += 1;
												break;
							Track += 1;
					TrackA += 1; bar.update(TrackA);

			if Mode == 'All' or Mode == 'Hop':
				#Redistribution of nodes to trees based on Hop limit
				for node in list(NETWORK.values()):
					if node.Type == -1:
						for path in node.SINKPATHS:
							if (len(path) - 1) > HopLimit:
								child = path[-1]
								for root in list(NETWORK.values()):
									PATH =  list(astar_path(G, root.Id, child, weight='length'))
									if ((len(PATH) -  1) <= HopLimit):
										NODES[root.Id].AddPath(PATH)
										if path in NODES[node.Id].SINKPATHS:
											NODES[node.Id].SINKPATHS.remove(path)
										for s in PATH[1:]:											
											NODES[root.Id].AddMember(NODES[s])
											NODES[node.Id].RemoveMember(NODES[s])
										break;

					TrackA += 1; bar.update(TrackA);
			
			if Mode != 'All' and Mode != 'Hop' and Mode != 'Crowdness' and  Mode != 'Distance':
				print("! Wrong balancing Mode");
				TrackA += 1; bar.update(TrackA);
		return NODES, NETWORK, UNASSIGNED, DATA;


