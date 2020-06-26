class Link(object):
    """ The actual individual class
        Both the Man and Woman classes inherit this class
        In essence both Men and Women are Persons
        
        @author: olasupoAjayi
        @date: 18/01/2020
    """
    def __init__ (self, idx, name, snr, pos, pref):
        self.idx = idx
        self.snr = snr
        self.name = name
        self.pos = pos
        self.preferredMates = pref
        self.mate = None
        self.randomMate = None
                
    def isLonely(self):
        return self.mate is None
                
    def setMate(self, mate):
        if self.getMate() != mate:
            
            if self.mate is not None:
                self.mate.mate = None
                
            #set new mate if old mate is diff or non existent
            self.mate = mate
            
            if mate != None:
                mate.mate = self

    def setRandomMate(self, randomMate):
        if self.getRandomMate() != randomMate:
            
            if self.randomMate is not None:
                self.randomMate.randomMate = None
                
            #set new mate if old mate is diff or non existent
            self.randomMate = randomMate
            
            if randomMate != None:
                randomMate.randomMate = self
                
    def getMate(self):
        return self.mate

    def getRandomMate(self):
        return self.randomMate
    
    def receiveOptions(self, mates):
        self.preferredMates = mates
        
    def getPreferredMates(self):
        return self.preferredMates
    
    def getId(self):
        return self.idx
    
    def getSNR(self):
        return self.snr

    def getPos(self):
        return self.pos
    
    def getName(self):
        return self.name