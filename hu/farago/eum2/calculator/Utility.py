'''
Created on 2016 máj. 24

@author: Balázs
'''

import abc

class Utility(object):

    __metaclass__ = abc.ABCMeta

    _playerI = None
    _playerJ = None
    _model = None
    
    def __init__(self, playerI, playerJ, model):
        self._playerI = playerI
        self._playerJ = playerJ
        self._model = model

    @abc.abstractmethod
    def calculate(self):
        """Calculates expected utility"""
        return
    
    def player_I_J_Difference(self):
        return abs(self._playerI.position - self._playerJ.position)
    
    def player_I_Median_Difference(self):
        return abs(self._playerI.position - self._model.medianVoter.position)

class USI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 - 0.5*(self.player_I_J_Difference()/self._model.posDistance()))**self._playerI.risk)

class UFI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 + 0.5*(self.player_I_J_Difference()/self._model.posDistance()))**self._playerI.risk)
    
class UBI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 - 0.25*((self.player_I_Median_Difference() + self.player_I_J_Difference())/self._model.posDistance()))**self._playerI.risk)
                
class UWI(Utility):
    
    def calculate(self):
        return 2 - 4*((0.5 + 0.25*((self.player_I_Median_Difference() + self.player_I_J_Difference())/self._model.posDistance()))**self._playerI.risk)
    
class USQ(Utility):
    
    def calculate(self):
        return 2 - 4*(0.5**self._playerI.risk)