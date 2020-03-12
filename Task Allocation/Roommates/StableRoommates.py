from Roommates import *; 

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
        
        self.Women = []
        self.Men = []        
            #define arrays for Men and Women
        self.converter(firstList, secondList)
   
    def converter (self, firstList, secondList):
        """Used to map external lists to Men & Women List"""
    
        #this function should be called when the two lists are to be supplied external
        #and there is a need to map them to men & women list.
        #both arrays have to be of equal size in SRM
    
        #check that both lists are of equal size
        if len(firstList) != len(secondList):
            print ("Error: Supplied Lists are of different length!")
            return
        else:    
            for f in firstList:
                self.Men.append(Man(f))
            for s in secondList:
                self.Women.append(Woman(s))
            

        #assign preferences - 
        #if preference list is already supplied, it extracts from the list
        #else it builds its own
        for w in self.Women:
            w.receiveOptions(self.Men)
            
        for m in self.Men:
            m.receiveOptions(self.Women)
    
       
        self.findStableRoommates(self.Women, self.Men)
        
    
    def menPropose(): 
        for man in Men: 
             man.propose()
    
    
    def womanChoose(id):
        return women.get(id).chooseMate()
    

    def findStableRoommates(self, women, men):
            for man in men:
                #a man can propose even if he already has a partner                                
                man.propose()                    
                    
            #women then pick thier favourite suitor
            #this is still not an allocation. This is only the women describing what they wld like
            #hence the name Delayed Allocation
            for woman in women:                
                woman.chooseMate()        
            
            #Now Clean up all unallocated
            
            self.availableMen = []
            self.SingleWomen = []
            
            for woman in women:                
                if woman.getMate() is None: 
                    self.SingleWomen.append(woman)
                    #print("Single Ladies -> {}".format(woman.getName()))
        
            for m in self.Men:                
                if m.isLonely():
                    self.availableMen.append(m)
                   # print("Single Men -> {}".format(m.getName()))
            
            self.forceMatch(self.SingleWomen, self.availableMen)
            

    def forceMatch(self, singleList, fMen):
        """This ensures that no individual is left without a pair"""
        #This is called as a last resort to ensure that all individuals are paired
                         
        for sg in singleList:
            sg.chooseMate(fMen)    
