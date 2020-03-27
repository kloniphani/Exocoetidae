from Roommates.Node import *; 
from Roommates.User import *;

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
            

    def forceMatch(self, singleList, fNodes):
        """This ensures that no individual is left without a pair"""
        #This is called as a last resort to ensure that all individuals are paired
                         
        for sg in singleList:
            sg.chooseMate(fNodes)    
