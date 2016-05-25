'''
Created on 2016 máj. 24

@author: Balázs
'''

import abc

class Utility(object):

    __metaclass__ = abc.ABCMeta

    __medianVoter = None
    __playerI = None
    __playerJ = None
    __maxDifferenceBetweenPositions = 0
    __riskIJ = 0

    def __init__(self, medianVoter, playerI, playerJ, maxDifferenceBetweenPositions, riskIJ = 1):
        self.__medianVoter = medianVoter
        self.__playerI = playerI
        self.__playerJ = playerJ
        self.__maxDifferenceBetweenPositions = maxDifferenceBetweenPositions
        self.__riskIJ = riskIJ    

    @abc.abstractmethod
    def calculate(self):
        """Calculates expected utility"""
        return
    
    def player_I_J_Difference(self):
        return abs(self.__playerI.position - self.__playerJ.position)
    
    def player_I_Median_Difference(self):
        return abs(self.__playerI.position - self.__medianVoter.position)

class USI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 - 0.5*(self.player_I_J_Difference()/self.__maxDifferenceBetweenPositions))**self.__riskIJ)

class UFI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 + 0.5*(self.player_I_J_Difference()/self.__maxDifferenceBetweenPositions))**self.__riskIJ)
    
class UBI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 - 0.25*((self.player_I_Median_Difference() + self.player_I_J_Difference())/self.__maxDifferenceBetweenPositions))**self.__riskIJ)
                
class UWI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 + 0.25*((self.player_I_Median_Difference() + self.player_I_J_Difference())/self.__maxDifferenceBetweenPositions))**self.__riskIJ)
    
class USQ(Utility):
    
    def calculate(self):
        return 2 - 4*(0.5**self.__riskIJ)