from Roommates.Link import *;

class Node (Link):
    """
    The Man Class
    Women/Jobs are allocated to this class
    
    This class has only one list - The Preference list = which is its the list of preferred Jobs
    
    Based on preset criteria the Man/Machine proposes to a number of Women or Jobs 
    All proposals are placed on the suitor list of the proposed.
    
    @author: olasupoAjayi
    @date: 18/01/2020
    """
    def __init__(self, firsts):
        self.firsts = firsts
        self.name = firsts["name"]
        self.snr = firsts["snr"]
        self.pos = first["pos"]
        self.preferredMates = firsts["preferences"]
        self.mate = None #initially set mate to None
        self.potentialMates = None   #list of person objects
                
   #override the parent's receiveoptions
    def receiveOptions(self, mates):
        self.potentialMates = mates
        if self.getPreferredMates() is not None:
            #if already given then skip
            #print ("DEFAULT PREF LIST RECEIVED!! - MEN")
            return
        else:         
            for p in self.potentialMates:
                 #build own preference list based on certain criteria
                #add preference criteria here, example give below
                #in this example self.age is used as criterion
                if (p.getSNR() != self.getSNR()):
                    self.preferredMates.append(p)
                
    def propose(self):
        #selects & removes the first woman on the preferred list 
        for f in range (0,len(self.preferredMates),1):
            fianceName = self.preferredMates.pop(0) #get fiance's name
            for fiance in self.potentialMates:
                #self.potentialMates is just a list of OBJECTS of all available women in the system
                if fiance.getName() == fianceName:
                    if (self.getName() != fiance.getName()):
                    #this criteria was used as an example, please change to whatever criterion works for you
                        fiance.receiveProposal(self)   
                        #print ("Man {} proposed to Woman {}".format(self.getName(), fiance.getName()) )
  
