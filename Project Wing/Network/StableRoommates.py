from Network.Node import *; 
from Network.User import *;

class StableRoommates(object):
    '''
    STABLE ROOMMATE ALLOCATION ALGORITHM

    Two parties are involved in this allocation - Men and Women or Machine & Tasks/Job
    Jobs are allocated to Machines.

    In the Stable Roommate and unlike the Stable Marriage Allocation (SMA)
    multiple women/jobs can be allocated to a single man / machine 
    
    Please note that this algorithm gives preference to women/jobs - that is
    the women/jobs ultimately choose which Man or Machine to be allocated onto
    
    @author: olasupoAjayi
    @date: 18/01/2020
    '''

    def __init__(self, firstList, secondList):
        self.firstList = firstList
        self.secondList = secondList
        
        self.Users = []
        self.Nodes = []        
            #define arrays for Men and Women
        self.converter(firstList, secondList)
   
    def converter (self, firstList, secondList):
        """Used to map external lists to Men & Women List"""
    
        #this function should be called when the two lists are to be supplied external
        #and there is a need to map them to men & women list.
        #both arrays have to be of equal size in SRM
  
        for f in firstList:
            self.Nodes.append(Node(f))
        for s in secondList:
            self.Users.append(User(s))

        #assign preferences - 
        #if preference list is already supplied, it extracts from the list
        #else it builds its own
        for w in self.Users:
            w.receiveOptions(self.Nodes)
            
        for m in self.Nodes:
            m.receiveOptions(self.Users)
           
        self.findStableRoommates(self.Users, self.Nodes)  
        self.findRandomMates(self.Users, self.Nodes) 
    
    def nodesPropose(): 
        for node in Nodes: 
             node.propose()
    
    def userChoose(id):
        return users.get(id).chooseMate()

    def findStableRoommates(self, users, nodes):
            for node in nodes:
                #a man can propose even if he already has a partner                                
                node.propose()                    
                    
            #women then pick thier favourite suitor
            #this is still not an allocation. This is only the women describing what they wld like
            #hence the name Delayed Allocation
            for user in users:                
                user.chooseMate()        
            
            #Now Clean up all unallocated
            
            self.availableNodes = []
            self.SingleUsers = []
            
            for user in users:                
                if user.getMate() is None: 
                    self.SingleUsers.append(user)
                    #print("Single Ladies -> {}".format(woman.getName()))
        
            for m in self.Nodes:                
                if m.isLonely():
                    self.availableNodes.append(m)
                   # print("Single Men -> {}".format(m.getName()))
            
            self.forceMatch(self.SingleUsers, self.availableNodes)

    def findRandomMates(self, users, nodes):
        import numpy as np
        from geopy import distance

        DISTANCES = {}
        for user in users:
            temp = []
            for node in nodes:                
                Vincenty = distance.vincenty((user.pos[0], user.pos[1]),(node.pos[0], node.pos[1])).kilometers
                GreatCircle = distance.great_circle((user.pos[0], user.pos[1]),(node.pos[0], node.pos[1])).kilometers
                d = (Vincenty + GreatCircle)/2
                temp.append((node, d))
            DISTANCES[str(user.id)] = sorted(temp, key=lambda x: x[1])

        distances = np.array([[d[1] for d in value] for key, value in DISTANCES.items()])
        mean = distances.mean()
        standard = distances.std()
        shape = mean 
        scale = np.log(standard)
        s = np.random.gamma(shape, scale, len(nodes)**2)

        for user in users:
            hasMate = False;
            while(hasMate != True):
                temp = np.random.choice(s)
                for n, d in DISTANCES[user.id]:
                    if int(temp) == int(d):
                        user.setRandomMate(n)
                        hasMate = True
                        break

        print(shape, standard, scale)

        import matplotlib.pyplot as plt
        import scipy.special as sps  

        count, bins, ignored = plt.hist(s, len(nodes), density=True)
        y = bins**(shape-1)*(np.exp(-bins/scale) /  
                            (sps.gamma(shape)*scale**shape))
        plt.plot(bins, y, linewidth=2, color='r')  
        plt.show()

    def forceMatch(self, singleList, fNodes):
        """This ensures that no individual is left without a pair"""
        #This is called as a last resort to ensure that all individuals are paired
                         
        for sg in singleList:
            sg.chooseMate(fNodes)    

    def getNodes(self):
        return self.Nodes

    def getUsers(self):
        return self.Users