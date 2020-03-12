class Person(object):
    """ The actual individual class
        Both the Man and Woman classes inherit this class
        In essence both Men and Women are Persons
        
        @author: olasupoAjayi
        @date: 18/01/2020
    """
    def __init__ (self, idx, name, age, pref):
        self.idx = idx
        self.age = age
        self.name = name
        self.preferredMates = pref
        self.mate = None
                
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
                
    def getMate(self):
        return self.mate
    
    def receiveOptions(self, mates):
        self.preferredMates = mates
        
    def getPreferredMates(self):
        return self.preferredMates
    
    def getId(self):
        return self.idx
    
    def getAge(self):
        return self.age
    
    def getName(self):
        return self.name