'''
Created on 2016 máj. 24

@author: Balázs
'''

import abc

class Utility(object):

    __metaclass__ = abc.ABCMeta

    _medianVoter = None
    _playerI = None
    _playerJ = None
    _maxDifferenceBetweenPositions = 0
    _riskIJ = 0

    def __init__(self, medianVoter, playerI, playerJ, maxDifferenceBetweenPositions, riskIJ = 1):
        self._medianVoter = medianVoter
        self._playerI = playerI
        self._playerJ = playerJ
        self._maxDifferenceBetweenPositions = maxDifferenceBetweenPositions
        self._riskIJ = riskIJ    

    @abc.abstractmethod
    def calculate(self):
        """Calculates expected utility"""
        return
    
    def player_I_J_Difference(self):
        return abs(self._playerI.position - self._playerJ.position)
    
    def player_I_Median_Difference(self):
        return abs(self._playerI.position - self._medianVoter.position)

class USI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 - 0.5*(self.player_I_J_Difference()/self._maxDifferenceBetweenPositions))**self._riskIJ)

class UFI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 + 0.5*(self.player_I_J_Difference()/self._maxDifferenceBetweenPositions))**self._riskIJ)
    
class UBI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 - 0.25*((self.player_I_Median_Difference() + self.player_I_J_Difference())/self._maxDifferenceBetweenPositions))**self._riskIJ)
                
class UWI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 + 0.25*((self.player_I_Median_Difference() + self.player_I_J_Difference())/self._maxDifferenceBetweenPositions))**self._riskIJ)
    
class USQ(Utility):
    
    def calculate(self):
        return 2 - 4*(0.5**self._riskIJ)