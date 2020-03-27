from Roommates.Link import *;

import csv;

class User (Link):
    """
    The Woman Class
    A Woman or Job gets allocated to a Man/Machine
    This class has two list
    a. The Preference list = which is its the list of preferred Men / Machine
    b. The Suitor list = list of Men / Machine that have proposed to it
    
    Upon receiving proposals, this Class cross references its preference list
    against its suitor list. It only accepts a proposal if
    the proposal is in its suitor list and its preference list.
    
    In this algorithm a woman/job can accept a proposal from a Man/Machine even if
    such Man/Machine is already engaged 
    
    @author: olasupoAjayi
    @date: 18/01/2020
    """
    
    def __init__(self, seconds):
        self.seconds = seconds
        self.suitors = [] #holds the list of men that proposed to this woman
        self.name = seconds["name"]
        self.bandwidth = seconds["bandwidwith"]
        self.pos = seconds["pos"]
        self.preferredMates = seconds["preferences"]   #list of this woman's preferred men
        self.preferredMates2 = []  #reserved 4 overloaded call
        self.mate = None #initially set mate to None
        self.potentialMates = None            
    
    #override the parent's receiveoptions
    def receiveOptions(self, mates):
        self.potentialMates = mates
        if self.getPreferredMates() is not None:
            return
        else:         
            for p in self.potentialMates:
            #build own preference list based on certain criteria
            #add preference criteria here, example give below
            #in this example self.age is used as criterion
                if (p.getSNR() != self.getSNR()):
                    preferredMates.append(p)
       
    def receiveProposal (self, suitor):
        #adds men from which proposal were received to the suitor list
        self.suitors.append(suitor)        
        
    def chooseMate(self, forcedPartners = None):
                                              
        if forcedPartners == None:
            #NORMAL CALL        
            ###############################################################################################
            for d in range(0,len(self.preferredMates),1):         
                mostDesiredName = self.getPreferredMates().pop(0)  #get name of most desired partner
                self.preferredMates2.append(mostDesiredName)  #used by overloaded call
                #next find the partner within the list of potential men in the system
                for fian in self.potentialMates:
                    if fian.getName() == mostDesiredName:
                        if ((fian in self.suitors)):                         
                            self.setMate(fian)
                            break                         
            
                if self.getMate() is None:
                    #only continue searching if the most desired partner (first on the preferredMates list) is unavailable                    
                    continue
                else:
                    print ("{} chose {} as an Access Point".format(self.getName(), self.getMate().getName()))     
                    
                    filename = "results.csv" 
                    with open(filename, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow([self.getName(), self.getMate().getName()])

                    break
                    #break ensures that the priority of the preference list is considered.
        
        elif forcedPartners is not None:
                                            #OVERLOADED  CALL        
            ###############################################################################################
    
            #final attempt 2 match based on preference
            for d in range(0,len(self.preferredMates2),1): 
                desirable = self.preferredMates2.pop(0)  #get name of most desired partner                
                #next find the partner within the list of unattached men in the system
                for f in range (0, len(forcedPartners), 1):
                    if forcedPartners[f].getName() == desirable:
                        self.setMate(forcedPartners[f])  #found a free man who is also in the woman's pref list - though further down the list
                        break
                if (self.getMate() is None):
                #if none of the available men r on pref list, then force partnership with first available man
                    self.setMate(forcedPartners[0])
                else:
                    print ("{} chose {} as a partner*".format(self.getName(), forcedPartners[f].getName()))
                    
                    filename = "results.csv"
                    with open(filename, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow([self.getName(), self.getMate().getName()])

                    break
            
