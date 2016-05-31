'''
Created on 2016 máj. 19

@author: Balázs
'''

class Player():
    '''
    Player of EUM
    '''
    preferredPosition = None
    previousPosition = None
    
    name = None
    capability = None
    position = None
    salience = None
    
    sumOfVotes = 0

    def __init__(self, name, capability, position, salience):
        self.name = name
        self.capability = float(capability)
        self.position = float(position)
        self.previousPosition = float(position)
        self.salience = float(salience)
        
        self.preferredPosition = self.position
        
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