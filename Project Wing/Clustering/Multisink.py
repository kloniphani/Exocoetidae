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

	def GreedySinkNodeSelectionWithSinksTree(NODES, NETWORK, UNASSIGNED, DATA, Mode = 'LAP',
				Median_ResidualEnergy = None, MaximumClusterHeads = None, Maximum_SNR = None, Minimum_SNR = None, NumberOfNodes = None, ClusterRadius = 100,
				Theta = 0.5, Beta = 0.5, Alpha= 0.5, Profit = 0, Best_SNR = -60,
				HopLimit = 2):	 
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
			NODES = Multisink.InitialiseNodes(NODES, BestSNR = -60)
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
						MST = list(minimum_spanning_edges(G, algorithm = 'kruskal', data = False, weight = 'length'))
						PATHS = []
						
						for path in MST:
							PATHS.append(list(path))
							TrackA += 1; bar.update(TrackA);

						for path in PATHS: 							
							for i in path:
								if i not in NODES[Root.Id].MEMBERS and str(i) is not str(Root.Id):
									NODES[Root.Id].AddMember(NODES[i])
								if i in UNASSIGNED:
									NODES[i].ChangeToClusterMember(NODES[Root.Id])
									NODES[i].ChangeToChainNode()
									UNASSIGNED.remove(i)  
							
							NODES[path[1]].SetHoopHead(NODES[path[0]])
							NODES[path[0]].AddMember(NODES[path[1]])
							TrackA += 1; bar.update(TrackA);

						if Root.Id in UNASSIGNED:
							UNASSIGNED.remove(Root.Id)

						#for path in PATHS:
						#	for p in PATHS:
						#		if p is not path and path[-1] == p[0]:
						#			path.append(p[-1])
						#			PATHS.remove(p)
					
						for path in PATHS:
							NODES[Root.Id].AddPath(path)

					TrackA += 1; bar.update(TrackA);
		return NODES, NETWORK, UNASSIGNED, DATA;

	def BalanceTree(NODES, NETWORK, UNASSIGNED, DATA, 
				 MaximumClusterHeads = None, NumberOfNodes = None, ClusterRadius = 100,
				 HopDistance = 40, HopLimit = 2, Crowdness = 8,
				 Mode = 'All'):
		#BALANCING THE TREE
		TrackA = 1; EndA = len(UNASSIGNED); White = 0; Gray = 1; Black = 2;
		with progressbar.ProgressBar(max_value = progressbar.UnknownLength) as bar:
			TrackA += 1; bar.update(TrackA);

			if Mode == 'All' or  Mode == 'Distance':
				#Redistribution of nodes to trees based on distance in number of hops 				
				for root in list(NETWORK.values()):
					G = Graph();
					G.add_nodes_from([n.Id for n in list(NODES.values())])
					G.add_edges_from(root.SINKPATHS)

					for node in root.MEMBERS:
						Distance = 0;
						path = dijkstra_path(G,node.Id,root.Id)
						for i in range(len(path)-1):
							Distance += NODES[path[i]].Distance(NODES[path[i + 1]].Position)

						if Distance > HopDistance:
							for n in root.MEMBERS:
								if str(node.Id) is not str(n.Id):
									p = dijkstra_path(G,n.Id,root.Id)
									distance = 0;
									for i in range(len(p)-1):
										distance += NODES[p[i]].Distance(NODES[p[i + 1]].Position)
									
									if distance + node.Distance(n.Position) <= HopDistance:
										for sinkpath in root.SINKPATHS:
											if (node.Head.Id in sinkpath and node.Id in sinkpath):
												NODES[root.Id].SINKPATHS.remove(sinkpath)
												break;
										
										if str(node.Head.Id) is not str(root.Id):
											NODES[node.Head.Id].RemoveMember(NODES[node.Id])

										NODES[root.Id].SINKPATHS.append([node.Id, n.Id])
										NODES[node.Id].SetHoopHead(NODES[n.Id])
										NODES[n.Id].AddMember(NODES[node.Id])

						TrackA += 1; bar.update(TrackA);

			if Mode == 'All' or Mode == 'Crowdness':
				#Redistribution of nodes to trees based on crowdness (nodes count expressing the maximum number of nodes that a tree is will to carry)
				for root in list(NETWORK.values()):	
					G = Graph();
					G.add_nodes_from([n.Id for n in list(NODES.values())])
					G.add_edges_from(root.SINKPATHS)

					for node in root.MEMBERS:
						Track = 0; count = 0;
						if len(node.MEMBERS) > Crowdness:
							while(count < (len(node.MEMBERS) - Crowdness) and Track < 100):
								for sink in root.MEMBERS:
									if str(node.Id) is not str(sink.Id) and len(sink.MEMBERS) < Crowdness:
										if len(node.MEMBERS) > 0:
											child = random.choice(node.MEMBERS)
											try:
												if sink.Id in [c.Id for c in child.LINKS] and len(dijkstra_path(G, sink.Id, root.Id)) > 0:
													for sinkpath in root.SINKPATHS:
														if (child.Head.Id in sinkpath and child.Id in sinkpath):
															NODES[root.Id].SINKPATHS.remove(sinkpath)
															break;
										
													if str(child.Head.Id) is not str(root.Id):
														NODES[child.Head.Id].RemoveMember(NODES[child.Id]) 
														G.remove_edge(child.Head.Id, child.Id)

													NODES[root.Id].SINKPATHS.append([child.Id, sink.Id])
													G.add_edge([child.Id, sink.Id])
													NODES[child.Id].SetHoopHead(NODES[sink.Id])
													NODES[sink.Id].AddMember(NODES[child.Id])
													count += 1;
											except:
												pass
										else:
											break;
								Track += 1;
						TrackA += 1; bar.update(TrackA);

			if Mode == 'All' or Mode == 'Hop':
				#Redistribution of nodes to trees based on Hop limit
				for root in list(NETWORK.values()):
					G = Graph();
					G.add_nodes_from([n.Id for n in list(NODES.values())])
					G.add_edges_from(root.SINKPATHS)

					for node in root.MEMBERS:
						PATH = dijkstra_path(G, node.Id, root.Id)
						if (len(PATH) - 1 > HopLimit):
							for sink in root.MEMBERS:
								if str(node.Id) is not str(sink.Id):
									path = dijkstra_path(G, sink.Id, root.Id)
									if len(path) - 1 < HopLimit:
										for sinkpath in root.SINKPATHS:
											if (node.Head.Id in sinkpath and node.Id in sinkpath):
												NODES[root.Id].SINKPATHS.remove(sinkpath)
										
										if str(node.Head.Id) is not str(root.Id):
											NODES[node.Head.Id].RemoveMember(NODES[node.Id])

										NODES[root.Id].SINKPATHS.append([node.Id, sink.Id])
										NODES[node.Id].SetHoopHead(NODES[sink.Id])
										NODES[sink.Id].AddMember(NODES[node.Id])
					TrackA += 1; bar.update(TrackA);
			
			if Mode != 'All' and Mode != 'Hop' and Mode != 'Crowdness' and  Mode != 'Distance':
				print("! Wrong balancing Mode");
				TrackA += 1; bar.update(TrackA);
		return NODES, NETWORK, UNASSIGNED, DATA;