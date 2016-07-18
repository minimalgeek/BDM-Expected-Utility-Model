'''
Created on 2016 júl. 18

@author: Balázs
'''

from typing import Iterable
from hu.farago.eum2_Cahi.dto.Player import Player

class WeightedPositionCalculator(object):
    
    def __init__(self, players:Iterable[Player]):
        self.players = players
        
    def calculate(self):
        powerSum = sum(x.power() for x in self.players)
        weightedSum = sum((x.power()/powerSum)*x.position for x in self.players)
        return weightedSum