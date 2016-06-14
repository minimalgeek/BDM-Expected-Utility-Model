'''
Created on 2016 máj. 19

@author: Balázs
'''

import collections 

class Player():
    '''
    Player of EUM
    '''
    previousPosition = None
    
    name = None
    capability = None
    position = None
    salience = None
    
    risk = None
    sumOfVotes = 0
    probabilityOfSuccess = None
    probabilityOfStatusQuo = None
    expectedUtilityI = None
    expectedUtilityJ = None
    offers = None
    
    def __init__(self, name, capability, position, salience):
        self.name = name
        self.capability = float(capability)
        self.position = float(position)
        self.previousPosition = float(position)
        self.salience = float(salience)
        
        self.risk = 1
        self.sumOfVotes = 0
        self.probabilityOfSuccess = collections.OrderedDict()
        self.probabilityOfStatusQuo = collections.OrderedDict()
        self.expectedUtilityI = collections.OrderedDict()
        self.expectedUtilityJ = collections.OrderedDict()
        self.offers = collections.OrderedDict()
                
    def power(self):
        return self.capability*self.salience
    
    def addToSum(self, value):
        self.sumOfVotes += value
        
    def updatePosition(self, value):
        self.previousPosition = self.position
        self.position = value
    
    def __str__(self):
        return ','.join([self.name, str(self.capability), str(round(self.position, 3)), str(self.salience)])
    def __repr__(self):
        return self.__str__()