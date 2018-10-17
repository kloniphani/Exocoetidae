"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       December 10, 2017
Copyright:  2017 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""

from numpy import *
from networkx import *
from geopy import distance
import json, io, progressbar

class Model(object):
	"""description of class"""

	def RemoveNode(N, Index, List, Results = False):
		"""REMOVE NODE
		The function takes a @N - Node list and delete all it's members from @List by using @Index to identify the correct node
		"""
		Total = len(List)
		for node in N[Index].MEMBERS:
				position = 0; length = len(List)
				while(position < len(List)):
					if(node.Id is List[position] or Index is List[position] or int(Index) == int(List[position])):
						del List[position]
						continue
					else:
						position += 1
		if Results is True: print('Nodes Deleted: {0:3}\tNodes Remaining: {1:3}\tNodes Before: {2:3}'.format(Total - len(List), len(List), Total))

	def RemoveItems(ListA, ListB, Results = False):
		"""
		The functions removes items taht are in @ListB from @ListA
		"""
		Total = len(ListA)
		for item in ListB:
			if item.Id in [node.Id for node in ListA]:
				i = 0; End = len(ListA);
				while i < End:
					if item.Id == ListA[i].Id:
						del ListA[i]
						End = len(ListA)
					else:
						i += 1

		if Results is True: print('Nodes Deleted: {0:3}\tNodes in List B: {1:3}\tNodes Before: {2:3}\tNodes in List A: {3:3}'.format(Total - len(ListA), len(ListB), Total, len(ListA)))
		return ListA, ListB;
	
	def Backhauling(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50):
		"""
		"""
		print("\nBackhauling Model Processing")
		if Median_ResidualEnergy is None and MaximumClusterHeads is None and Maximum_SNR is None and Minimum_SNR is None:
			#Sorting the Nodes in Descending order based on their SNR
			TEMP = list(self.NODES.values());
			TEMP.sort(key = lambda node: node.SNR, reverse = True) 

			Best_SNR = 2e-07
			Minimum_SNR = TEMP[0].SNR
			Maximum_SNR = TEMP[-1].SNR

			Median_ResidualEnergy = median([node.ResidualEnergy for node in TEMP])

		TrackA = 0; TrackB = 0; EndA = len(NODES); EndB = 10; TransmissionGain = 3; Type = 0;
		with progressbar.ProgressBar(max_value = EndA) as bar:
			while len(UNUSSIGNED) > 0 and TrackA < EndA:
				index = 0; Head = None
				#Selecting the Node from the proccessing set that has the highest recieved SNR at the LAP
				#Check if the Residual Energy Ei of the selected node is greater than or equal to the median Residual Energy of the set node within the processing set 
				while(index < len(UNUSSIGNED)):	
					if NODES[UNUSSIGNED[index]].ResidualEnergy >=  Median_ResidualEnergy:
						Head = UNUSSIGNED[index]; NODES[Head].ChangeToClusterHead(); break; 
					index += 1

				if Head is not None:
					#Calculating the number of Nodes per Cluster
					NumberOfNodes = int(ceil(abs((sqrt(len(NODES)) * NODES[Head].SNR)/(Maximum_SNR - Minimum_SNR))))

					#Assigning the Cluster Member to the Cluster Head based on the calculate number of Nodes above.
					NETWORK[Head] = NODES[Head]

					count = 1;
					for node in UNUSSIGNED:
						if(count > NumberOfNodes): break;
						else:
							if(NODES[Head].Distance(NODES[node].Position) <= ClusterRadius and Head is not node):
								NODES[node].ChangeToClusterMember(NODES[Head])
								NETWORK[Head].MEMBERS.append(NODES[node])
								count +=1

					#Removing Selected Nodes for a cluster Network.
					if Head is not None:	
						Model.RemoveNode(NETWORK, Head, UNUSSIGNED)
				TrackA += 1
				bar.update(TrackA)
		return NODES, NETWORK, UNUSSIGNED, DATA

	def Myopic(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50):
		"""
		"""
		print("\nMyopic Model Processing")
		if Median_ResidualEnergy is None and MaximumClusterHeads is None and Maximum_SNR is None and Minimum_SNR is None:
			#Sorting the Nodes in Descending order based on their SNR
			TEMP = list(NODES.values());
			TEMP.sort(key = lambda node: node.SNR, reverse = True) 

			UNUSSIGNED = [node.Id for node in TEMP]

			Best_SNR = 2e-07
			Minimum_SNR = TEMP[0].SNR
			Maximum_SNR = TEMP[-1].SNR

			Median_ResidualEnergy = median([node.ResidualEnergy for node in TEMP])

		TrackA = 0; TrackB = 0; EndA = len(NODES); EndB = 10; TransmissionGain = 3; Type = 0;
		with progressbar.ProgressBar(max_value = EndA) as bar:
			while(len(UNUSSIGNED) > 0 and TrackA < EndA):
				index = 0; Head = None
				#Selecting the Node from the proccessing set that has the highest recieved SNR at the LAP
				#Check if the Residual Energy Ei of the selected node is greater than or equal to the median Residual Energy of the set node within the processing set 
				while(index < len(UNUSSIGNED)):	
					if NODES[UNUSSIGNED[index]].ResidualEnergy >= Median_ResidualEnergy:
						Head = UNUSSIGNED[index]; NODES[Head].ChangeToClusterHead(); break; 
					index += 1

				if Head is not None:
					#Calculating the number of Nodes per Cluster.
					#NumberOfNodes = int(ceil(abs((len(NODES) * (NODES[Head].SNR + abs(Minimum_SNR)) * 0.05)/(Maximum_SNR + abs(Minimum_SNR)))))
					NumberOfNodes = int(ceil(abs((sqrt(len(NODES)) * NODES[Head].SNR)/(Maximum_SNR - Minimum_SNR))))

					#Assigning the Cluster Member to the Cluster Head based on the calculate number of Nodes above.
					NETWORK[Head] = NODES[Head]

					count = 1;
					for node in UNUSSIGNED:
						if(count > NumberOfNodes): break;
						else:
							if(NODES[Head].Distance(NODES[node].Position) <= ClusterRadius and Head is not node):
								NODES[node].ChangeToClusterMember(NODES[Head])
								NETWORK[Head].MEMBERS.append(NODES[node])
								count +=1

					#Checking if The Head Cluster has Leaf Nodes, If Not, delete the Head from Cluster and append to the Unussiged list.
					if len(NETWORK[Head].MEMBERS) == 0:
						if Head not in UNUSSIGNED:
							UNUSSIGNED.append(Head)

						NODES[Head].ChangeToNode(Results = False)
						if Head in list(NETWORK.keys()):
							NETWORK.pop(Head)
							Head = None

					#Removing Selected Nodes for a cluster Network.
					if Head is not None:	
						Model.RemoveNode(NETWORK, Head, UNUSSIGNED)
				TrackA += 1
				bar.update(TrackA)
		return NODES, NETWORK, UNUSSIGNED, DATA

	def Successive(NODES, NETWORK, UNUSSIGNED, DATA, 
				Median_ResidualEnergy = None, MaximumClusterHeads = None, Maximum_SNR = None, Minimum_SNR = None, NumberOfNodes = None, ClusterRadius = 100,
				Theta = 0.5, Beta = 0.5, Profit = 0):
		"""
		"""
		print("\nSuccessive Selection Model Processing")
		if Median_ResidualEnergy is None and MaximumClusterHeads is None and Maximum_SNR is None and Minimum_SNR is None:
			#Sorting the Nodes in Descending order based on their SNR
			TEMP = list(NODES.values());
			TEMP.sort(key = lambda node: node.SNR, reverse = True) 

			UNUSSIGNED = [node.Id for node in TEMP]

			Best_SNR = 2e-07
			Minimum_SNR = TEMP[-1].SNR
			Maximum_SNR = TEMP[0].SNR

			Median_ResidualEnergy = median([node.ResidualEnergy for node in TEMP])
			Average_ResidualEnergy = average([node.ResidualEnergy for node in TEMP])
			Maximum_ResidualEnergy = max([node.ResidualEnergy for node in TEMP])

		TrackA = 0; TrackB = 0; EndA = len(NODES); EndB = 10; TransmissionGain = 3; Type = 0;
		with progressbar.ProgressBar(max_value = EndA) as bar:			
			while(len(UNUSSIGNED) > 0 and TrackA < EndA):
				index = 0; Head = None				
				#Selecting the Node from the proccessing set that has the highest recieved SNR at the LAPTime?
				for node in UNUSSIGNED:
					Reward = (Theta * (NODES[node].SNR/Maximum_SNR) - Beta * ((Average_ResidualEnergy - NODES[node].ResidualEnergy)/(Maximum_ResidualEnergy - Average_ResidualEnergy)))/2;
					if Reward >= Profit:
						Head = UNUSSIGNED[index]; NODES[Head].ChangeToClusterHead(); break; 
					index += 1

				if Head is not None:
					#Calculating the number of Nodes per Cluster.
					#NumberOfNodes = int(ceil(abs((len(NODES) * (NODES[Head].SNR + abs(Minimum_SNR)) * 0.05)/(Maximum_SNR + abs(Minimum_SNR)))))
					NumberOfNodes = int(ceil(abs((sqrt(len(NODES)) * NODES[Head].SNR)/(Maximum_SNR - Minimum_SNR))))

					#Assigning the Cluster Member to the Cluster Head based on the calculate number of Nodes above.
					NETWORK[Head] = NODES[Head]

					count = 1;
					for node in UNUSSIGNED:
						if(count > NumberOfNodes): break;
						else:
							if(NODES[Head].Distance(NODES[node].Position) <= ClusterRadius and Head is not node):
								NODES[node].ChangeToClusterMember(NODES[Head])
								NETWORK[Head].MEMBERS.append(NODES[node])
								count +=1

					#Checking if The Head Cluster has Leaf Nodes, If Not, delete the Head from Cluster and append to the Unussiged list.
					if len(NETWORK[Head].MEMBERS) == 0:
						if Head not in UNUSSIGNED:
							UNUSSIGNED.append(Head)

						NODES[Head].ChangeToNode(Results = False)
						if Head in list(NETWORK.keys()):
							NETWORK.pop(Head)
							Head = None

					#Removing Selected Nodes for a cluster Network.
					if Head is not None:	
						Model.RemoveNode(NETWORK, Head, UNUSSIGNED)

				TrackA += 1
				bar.update(TrackA)
		return NODES, NETWORK, UNUSSIGNED, DATA

	def Greedy(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50):
		pass

	def Odd(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50):
		"""
		"""
		print("\nOdd Model Processing")
		if Median_ResidualEnergy is None and MaximumClusterHeads is None and Maximum_SNR is None and Minimum_SNR is None:
			#Sorting the Nodes in Descending order based on their SNR
			TEMP = list(NODES.values());
			TEMP.sort(key = lambda node: node.SNR, reverse = True) 

			UNUSSIGNED = [node.Id for node in TEMP]

			Best_SNR = 2e-07
			Minimum_SNR = TEMP[0].SNR
			Maximum_SNR = TEMP[-1].SNR

			Median_ResidualEnergy = median([node.ResidualEnergy for node in TEMP])

		TrackA = 0; TrackB = 0; EndA = len(NODES); EndB = 10; TransmissionGain = 3; Type = 0;
		with progressbar.ProgressBar(max_value = EndA) as bar:
			while(len(UNUSSIGNED) > 0 and TrackA < EndA):
				index = 0; Head = None
				#Selecting the Node from the proccessing set that has the highest recieved SNR at the LAP
				#Check if the Residual Energy Ei of the selected node is greater than or equal to the median Residual Energy of the set node within the processing set 
				while(index < len(UNUSSIGNED)):	
					if NODES[UNUSSIGNED[index]].ResidualEnergy >= Median_ResidualEnergy:
						Head = UNUSSIGNED[index]; NODES[Head].ChangeToClusterHead(); break; 
					index += 1

				if Head is not None:
					#Calculating the number of Nodes per Cluster.
					#NumberOfNodes = int(ceil(abs((len(NODES) * (NODES[Head].SNR + abs(Minimum_SNR)) * 0.05)/(Maximum_SNR + abs(Minimum_SNR)))))
					NumberOfNodes = int(ceil(abs((sqrt(len(NODES)) * NODES[Head].SNR)/(Maximum_SNR - Minimum_SNR))))

					#Assigning the Cluster Member to the Cluster Head based on the calculate number of Nodes above.
					NETWORK[Head] = NODES[Head]

					count = 1;
					while(count <= NumberOfNodes):
						if(count > NumberOfNodes or len(UNUSSIGNED) == 0): break;
						start = 0
						end = len(UNUSSIGNED)
						if end > 1:
							i = random.choice(range(start, end))
						else:
							i = 0
						node = UNUSSIGNED[i]						
						if(NODES[Head].Distance(NODES[node].Position) <= ClusterRadius and Head is not node):
							NODES[node].ChangeToClusterMember(NODES[Head])
							NETWORK[Head].MEMBERS.append(NODES[node])
							Model.RemoveNode(NETWORK, Head, UNUSSIGNED)
							count +=1

					#Checking if The Head Cluster has Leaf Nodes, If Not, delete the Head from Cluster and append to the Unussiged list.
					if len(NETWORK[Head].MEMBERS) == 0:
						if Head not in UNUSSIGNED:
							UNUSSIGNED.append(Head)

						NODES[Head].ChangeToNode(Results = False)
						if Head in list(NETWORK.keys()):
							NETWORK.pop(Head)
							Head = None

				TrackA += 1
				bar.update(TrackA)
		return NODES, NETWORK, UNUSSIGNED, DATA

	def OddRange(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50):
		"""
		"""
		print("\nOddRange Model Processing")
		if Median_ResidualEnergy is None and MaximumClusterHeads is None and Maximum_SNR is None and Minimum_SNR is None:
			#Sorting the Nodes in Descending order based on their SNR
			TEMP = list(NODES.values());
			TEMP.sort(key = lambda node: node.SNR, reverse = True) 

			UNUSSIGNED = [node.Id for node in TEMP]

			Best_SNR = 2e-07
			Minimum_SNR = TEMP[0].SNR
			Maximum_SNR = TEMP[-1].SNR

			Median_ResidualEnergy = median([node.ResidualEnergy for node in TEMP])

		TrackA = 0; TrackB = 0; EndA = len(NODES); EndB = 10; TransmissionGain = 3; Type = 0;
		with progressbar.ProgressBar(max_value = EndA) as bar:
			while(len(UNUSSIGNED) > 0 and TrackA < EndA):
				index = 0; Head = None
				#Selecting the Node from the proccessing set that has the highest recieved SNR at the LAP
				#Check if the Residual Energy Ei of the selected node is greater than or equal to the median Residual Energy of the set node within the processing set 
				while(index < len(UNUSSIGNED)):	
					if NODES[UNUSSIGNED[index]].ResidualEnergy >= Median_ResidualEnergy:
						Head = UNUSSIGNED[index]; NODES[Head].ChangeToClusterHead(); break; 
					index += 1

				if Head is not None:
					#Calculating the number of Nodes per Cluster.
					#NumberOfNodes = int(ceil(abs((len(NODES) * (NODES[Head].SNR + abs(Minimum_SNR)) * 0.05)/(Maximum_SNR + abs(Minimum_SNR)))))
					NumberOfNodes = int(ceil(abs((sqrt(len(NODES)) * NODES[Head].SNR)/(Maximum_SNR - Minimum_SNR))))

					#Assigning the Cluster Member to the Cluster Head based on the calculate number of Nodes above.
					NETWORK[Head] = NODES[Head]

					count = 1;
					while(count < NumberOfNodes):
						if(count > NumberOfNodes or len(UNUSSIGNED) == 0): break;
						start = int(floor(sqrt(len(UNUSSIGNED))))
						end = len(UNUSSIGNED)
						if end > 1:
							i = random.choice(range(start, end))
						else:
							i = 0
						node = UNUSSIGNED[i]
						
						if sqrt(len(NODES)) > len(UNUSSIGNED): 
							if(NODES[Head].Distance(NODES[node].Position) <= ClusterRadius and Head is not node and NODES[node].ResidualEnergy < Median_ResidualEnergy):
								NODES[node].ChangeToClusterMember(NODES[Head])
								NETWORK[Head].MEMBERS.append(NODES[node])
								Model.RemoveNode(NETWORK, Head, UNUSSIGNED)
								count +=1
						else:
							if(NODES[Head].Distance(NODES[node].Position) <= ClusterRadius and Head is not node):
								NODES[node].ChangeToClusterMember(NODES[Head])
								NETWORK[Head].MEMBERS.append(NODES[node])
								Model.RemoveNode(NETWORK, Head, UNUSSIGNED)
								count +=1

					#Checking if The Head Cluster has Leaf Nodes, If Not, delete the Head from Cluster and append to the Unussiged list.
					if len(NETWORK[Head].MEMBERS) == 0:
						if Head not in UNUSSIGNED:
							UNUSSIGNED.append(Head)

						NODES[Head].ChangeToNode(Results = False)
						if Head in list(NETWORK.keys()):
							NETWORK.pop(Head)
							Head = None

				TrackA += 1
				bar.update(TrackA)
		return NODES, NETWORK, UNUSSIGNED, DATA

	def Converse(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50):
		"""
		"""
		print("\nConverse Model Processing")
		#Sorting the Nodes in Descending order based on their SNR
		TEMP = list(NODES.values());
		TEMP.sort(key = lambda node: node.ResidualEnergy, reverse = False) 

		NOTCONNECTED = [node.Id for node in TEMP]

		TrackA = 0; TrackB = 0; EndA = len(NODES); EndB = 10; TransmissionGain = 3; Type = 0;
		with progressbar.ProgressBar(max_value = EndA) as bar:
			while(len(UNUSSIGNED) > 0 and TrackA < EndA):
				index = 0; Head = None
				#Selecting the Node from the proccessing set that has the highest recieved SNR at the LAP
				#Check if the Residual Energy Ei of the selected node is greater than or equal to the median Residual Energy of the set node within the processing set 
				while(index < len(UNUSSIGNED)):	
					if NODES[UNUSSIGNED[index]].ResidualEnergy >= Median_ResidualEnergy:
						Head = UNUSSIGNED[index]; NODES[Head].ChangeToClusterHead(); break; 
					index += 1

				if Head is not None:
					#Calculating the number of Nodes per Cluster.
					#NumberOfNodes = int(ceil(abs((len(NODES) * (NODES[Head].SNR + abs(Minimum_SNR)) * 0.05)/(Maximum_SNR + abs(Minimum_SNR)))))
					NumberOfNodes = int(ceil(abs((sqrt(len(NODES)) * NODES[Head].SNR)/(Maximum_SNR - Minimum_SNR))))

					#Assigning the Cluster Member to the Cluster Head based on the calculate number of Nodes above.
					NETWORK[Head] = NODES[Head]

					count = 1;
					for node in NOTCONNECTED:
						if(count >= NumberOfNodes or len(NOTCONNECTED) == 0): break;					
						elif(NODES[Head].Distance(NODES[node].Position) <= ClusterRadius and Head is not node):
							NODES[node].ChangeToClusterMember(NODES[Head])
							NETWORK[Head].MEMBERS.append(NODES[node])
							count +=1

					#Checking if The Head Cluster has Leaf Nodes, If Not, delete the Head from Cluster and append to the Unussiged list.
					if len(NETWORK[Head].MEMBERS) == 0:
						if Head not in UNUSSIGNED:
							UNUSSIGNED.append(Head)

						NODES[Head].ChangeToNode(Results = False)
						if Head in list(NETWORK.keys()):
							NETWORK.pop(Head)
							Head = None

					if Head is not None:
						Model.RemoveNode(NETWORK, Head, UNUSSIGNED)
						Model.RemoveNode(NETWORK, Head, NOTCONNECTED)

				TrackA += 1
				bar.update(TrackA)
		return NODES, NETWORK, UNUSSIGNED, DATA

	def Balancing(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50):
		"""
		"""
		print("\nBalancing Model Processing")
		#Selecting the nearest Clustered Head with less Children, then add new Children to network	
		TrackA = 0; EndA = len(UNUSSIGNED);	

		if NumberOfNodes is None:
			NumberOfNodes = int(ceil(len(NODES)/(MaximumClusterHeads)))

		if EndA > 0:
			with progressbar.ProgressBar(max_value = EndA) as bar:
				Counter = 0;
				while(TrackA <= EndA and Counter <= len(NETWORK)):
					head = None
					for i in NETWORK.values():
						NumberOfNodes = int(ceil(abs((sqrt(len(NODES)) * i.SNR)/(Maximum_SNR - Minimum_SNR))))
						if len(i.MEMBERS) < NumberOfNodes:
							head = i;
							for j in NETWORK.values():
								NumberOfNodes = int(ceil(abs((sqrt(len(NODES)) * j.SNR)/(Maximum_SNR - Minimum_SNR))))
								if i.Id is not j.Id and len(j.MEMBERS) < NumberOfNodes and len(head.MEMBERS) > len(j.MEMBERS):
									head = j

					if head is not None:
						count = 1;
						for id in UNUSSIGNED:
							NODES[id].ChangeToClusterMember(NODES[head.Id])
							NETWORK[head.Id].MEMBERS.append(NODES[id])	
							if count > int(ceil(abs((len(NODES) * head.SNR)/(Maximum_SNR - Minimum_SNR)))):
								break;
							count += 1
							TrackA += 1
							bar.update(TrackA);

						#Removing Selected Nodes for a cluster Network.	
						Model.RemoveNode(NETWORK, head.Id, UNUSSIGNED)
						EndB = len(UNUSSIGNED)
						if len(UNUSSIGNED) is 0:
							break;	
					Counter += 1

			if TrackA >= EndA or len(UNUSSIGNED) > 0:
				TrackB = 0; EndB = len(UNUSSIGNED);
				with progressbar.ProgressBar(max_value = EndB) as bar:
					while(len(UNUSSIGNED) > 0):
						Head = None;
						for h in NETWORK.values():
							for n in h.MEMBERS:
								if n.ResidualEnergy >= Median_ResidualEnergy:
									Head = n.Id;
									NODES[Head].ChangeToNode();
									NODES[Head].ChangeToClusterHead()
									#Delete a Member from a list?
									NETWORK[h.Id].RemoveMember(n)
									break;
							if Head is not None:
								break;
						if Head is not None:
							NumberOfNodes = int(ceil(abs((sqrt(len(NODES)) * NODES[Head].SNR)/(Maximum_SNR - Minimum_SNR))))

							#Assigning the Cluster Member to the Cluster Head based on the calculate number of Nodes above.
							NETWORK[Head] = NODES[Head]

							count = 1;
							for node in UNUSSIGNED:
								if(count > NumberOfNodes): break;
								if(NODES[Head].Distance(NODES[node].Position) <= ClusterRadius and Head is not node):
									NODES[node].ChangeToClusterMember(NODES[Head])
									NETWORK[Head].MEMBERS.append(NODES[node])
									TrackB += 1
									count +=1
									bar.update(TrackB)

							#Checking if The Head Cluster has Leaf Nodes, If Not, delete the Head from Cluster and append to the Unussiged list.
							if len(NETWORK[Head].MEMBERS) == 0:
								if Head not in UNUSSIGNED:
									UNUSSIGNED.append(Head)

								NODES[Head].ChangeToNode(Results = False)
								if Head in list(NETWORK.keys()):
									NETWORK.pop(Head)
									Head = None

							#Removing Selected Nodes for a cluster Network.
							if Head is not None:	
								Model.RemoveNode(NETWORK, Head, UNUSSIGNED)
		else:
			print('All NODES are CONNECTED')
			
		return NODES, NETWORK, UNUSSIGNED, DATA

	def Redistribute(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50, Results = False):
		"""
		"""
		print("\nRedistribute Model Processing")
		#Selecting the nearest Clustered Head with less Children, then add new Children to network	
		TrackA = 0; EndA = len(NETWORK);
		head = None

		if NumberOfNodes is None:
			NumberOfNodes = int(ceil(sqrt(len(NODES))))

		with progressbar.ProgressBar(max_value = EndA) as bar:
			#Count the average number of Children in the Cluster Head
			ChildrenCounts = []
			for head in NETWORK.values():
				ChildrenCounts.append(len(head.MEMBERS))
			AverageChildren = average(ChildrenCounts)

			#Moving children to a Cluster Head that have better SNR connection with them
			for head in NETWORK.values():
				NumberOfNodes = int(ceil(abs((sqrt(len(NODES)) * head.SNR)/(Maximum_SNR - Minimum_SNR))))
				if AverageChildren > len(head.MEMBERS) and len(head.MEMBERS) < NumberOfNodes:
					for h in NETWORK.values():
						Temp = []
						if head.Id is not h.Id and AverageChildren < len(h.MEMBERS):
							for node in h.MEMBERS:
								if float(head.ComputeSNR(node.Position)) > float(h.ComputeSNR(node.Position)):
									head.MEMBERS.append(NODES[node.Id])
									Temp.append(NODES[node.Id])
									NODES[node.Id].ChangeToClusterMember(head)
								if len(head.MEMBERS) >= NumberOfNodes:
									break;

							Model.RemoveItems(h.MEMBERS, Temp, Results)
							NETWORK[head.Id] = head
							NETWORK[h.Id] = h
				TrackA += 1
				bar.update(TrackA);

		return NODES, NETWORK, UNUSSIGNED, DATA

	def Chaining(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50):
		"""
		"""
		print("\nChaining Model Processing")
		#Selecting the nearest Clustered Head with less Children, then add new Children to network	
		TrackA = 0; EndA = len(NETWORK);
		head = None

		if NumberOfNodes is None:
			NumberOfNodes = int(ceil(sqrt(len(NODES))))

		with progressbar.ProgressBar(max_value = EndA) as bar:
			#Obtain the Maxium Radius of the Cluster Head coverage
			RADIUS = {}
			for head in NETWORK.values():
				Temp = []
				for node in head.MEMBERS:
					Temp.append(head.Distance(node.Position))
				RADIUS[head.Id] = max(Temp)

			#Checking the Node in an Ovelayed Coverage
			#If a node found is in a ovelayed coverage with best properties, the it can chain the network
			CHAIN = {}
			for head in NETWORK.values():
				for node in head.MEMBERS:
					for h in NETWORK.values():
						if h.Id is not head.Id and ((node.Position[0] - head.Position[0])**2 + (node.Position[1] - head.Position[1])**2 < RADIUS[head.Id]**2 and (node.Position[0] - h.Position[0])**2 + (node.Position[1] - h.Position[1])**2 < RADIUS[h.Id]**2):
							if node.ResidualEnergy > Median_ResidualEnergy and node.Type is 0:
								if node.Type is not 2 and node.Type is not -1:
									node.ChangeToChainNode()
								node.AddMember(h)
								if node.Id not in [n.Id for n in NETWORK.values()] and node.Id not in [key for key in CHAIN.keys()]:
									CHAIN[node.Id] = node
				TrackA += 1
				bar.update(TrackA);
			NETWORK.update(CHAIN)			
		return NODES, NETWORK, UNUSSIGNED, DATA

	def RemovePathKeys(Nodes, Network, List, G, Source, Destination, Results = False):
		L = len(List)

		Path = astar_path(G, Source, Destination)
		if len(Path) > 2:
			for i in range(0, len(Path) - 2):
				next = i + 1
				if Nodes[Path[i]].Id not in [node.Id for node in Network[Path[next]].MEMBERS] and Path[i] in List:
					Nodes[Path[i]].SetHoopHead(Nodes[Path[next]])
					Network[Path[next]].MEMBERS.append(Nodes[Path[i]])
			for p in Path:
				if p in List:
					List.remove(p)
		else:
			return Nodes, Network, None
	
		if Results is True: print('Nodes Deleted: {0:3}\tNodes Remaining: {1:3}\tNodes Before: {2:3}'.format(L - len(List), len(List), L)) 
		return Nodes, Network, List

	def Hoop(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50, ServiceProvider = None):
		"""
		"""
		TEMP = []
		print("\nHooping Cluster Head Model Processing")
		if len(NETWORK) > 0 and len(NODES) > 0:
			#Sorting the Nodes in Descending order based on their SNR
			TEMP = list(NODES.values());
			TEMP.sort(key = lambda node: node.SNR, reverse = True) 

			Best_SNR = 2e-07
			Minimum_SNR = TEMP[-1].SNR
			Maximum_SNR = TEMP[0].SNR

			Median_ResidualEnergy = median([node.ResidualEnergy for node in TEMP])
			
		G = Graph()
		G.add_node(ServiceProvider.Id)
		G.add_nodes_from([node.Id for node in TEMP])
		TrackA = 0; EndA = len(NETWORK);
		with progressbar.ProgressBar(max_value = EndA) as bar:
			for s in NETWORK.values(): 
				G.add_edge(s.Id, ServiceProvider.Id, weight = s.ComputeSNR(ServiceProvider.Position))
				for j in NETWORK.values():
					if s.Id is not j.Id:
						G.add_edge(s.Id, j.Id, weight = s.ComputeSNR(j.Position))				
				TrackA += 1
				bar.update(TrackA)

		Unussigned = [key for key in NETWORK.keys()]
		
		TrackA = 0; TrackB = 0; EndA = len(NETWORK); EndB = len(UNUSSIGNED); TransmissionGain = 3; Type = 0;
		with progressbar.ProgressBar(max_value = EndA) as bar:
			Destination = '00' #The LAP		
			for Source in NETWORK.keys():	
				NODES, NETWORK, Temp = Model.RemovePathKeys(NODES, NETWORK, Unussigned, G, Source, Destination)
				if Temp is not None:
					Unussigned = Temp
				elif Source in Unussigned:
					Unussigned.remove(Source)

				TrackA += 1
				bar.update(TrackA)
		return NODES, NETWORK, UNUSSIGNED, DATA

	def KMeans(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50, Results = False):
		"""
		"""
		print("\nK-Means Model Processing")

		from sklearn.cluster import KMeans

		TrackA = 0; EndA = len(NODES);
		Points = []

		for key, value in NODES.items():
			Points.append([value.Position[0], value.Position[1]])
		Points = array(Points)

		kmeans = KMeans(n_clusters = int(len(NODES)), n_init = 10, max_iter = 1000000, init = 'random', n_jobs = -1)
		kmeans.fit_predict(Points)

		with progressbar.ProgressBar(max_value = kmeans.n_clusters) as bar:
			"""for i in range(len(kmeans)):
			index = str(i + 1) 
			head = str(int(kmeans[i]) + 1)
			if head not in [NODES.keys()]:
				NODES[head].ChangeToClusterHead()
				NETWORK[head] = NODES[head]
			if head is not index and head != index:
				NETWORK[head].MEMBERS.append(NODES[index])
				NODES[index].ChangeToClusterMember(NODES[head])"""
				
			labels = kmeans.labels_
			centroids = kmeans.cluster_centers_

			for i in range(int(sqrt(len(NODES)))):
				ds = Points[where(labels == i)]
					
				head = None
				for node in NODES.values():
					if node.Position[0] == centroids[i,0] and node.Position[1] == centroids[i,1]:
						head = node
						if head is not None:
							if head.Type is not -2:
								NODES[head.Id].ChangeToClusterHead()
								NETWORK[head.Id] = NODES[head.Id]
						break;

				for item in ds:
					for node in NODES.values():
						if node.Position[0] == item[0] and node.Position[1] == item[1] and head is not None and node.Id is not head.Id:
							NODES[node.Id].ChangeToClusterMember(NODES[head.Id])
							NETWORK[head.Id].MEMBERS.append(NODES[node.Id])

				if head is not None:
				   Model.RemoveNode(NETWORK, head.Id, UNUSSIGNED, Results)
				bar.update(i)

		return NODES, NETWORK, UNUSSIGNED, DATA

	def Hierarchical(NODES, NETWORK, UNUSSIGNED, DATA, Median_ResidualEnergy, MaximumClusterHeads, Maximum_SNR, Minimum_SNR, NumberOfNodes = None, ClusterRadius = 50, Results = False):
		"""
		"""
		print("\nHierarchical Model Processing")

		from sklearn.cluster import KMeans

		TrackA = 0; EndA = len(NODES);
		Points = []

		for key, value in NODES.items():
			Points.append([value.Position[0], value.Position[1]])
		Points = array(Points)

		return NODES, NETWORK, UNUSSIGNED, DATA
