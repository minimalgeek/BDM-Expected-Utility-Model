'''
Created on 2016 máj. 26

@author: Balázs
'''

from hu.farago.eum2.dto.Player import Player
from hu.farago.eum2.dto.Model import Model

class RiskCalculator(object):
    
    def __init__(self, model:Model):
        self.model = model
    
    def calculate(self):
        for playerI in self.model.players:
            euSum = 0
            for playerJ in self.model.players:
                if playerI != playerJ:
                    euSum += playerI.expectedUtilityI[playerJ.name]
            playerI.risk = euSum # playerI.risk is used temporarily to store the sum value
        
        maxSum = max(self.model.players, key = lambda x : x.risk).risk
        minSum = min(self.model.players, key = lambda x : x.risk).risk
        
        for playerI in self.model.players:
            Ri = (2 * playerI.risk - maxSum - minSum)/(maxSum - minSum)
            ri = (1 - Ri/3)/(1 + Ri/3)
            playerI.risk = ri