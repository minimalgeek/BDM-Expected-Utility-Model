'''
Created on 2016 máj. 24

@author: Balázs
'''

from typing import Iterable
from hu.farago.eum2.dto.Player import Player
from hu.farago.eum2.dto.Model import Model

class ProbabilityOfStatusQuoCalculator(object):

    def __init__(self, model:Model):
        self.model = model

    def calculate(self):
        
        for i, playerI in enumerate(self.model.players):
            for j, playerJ in enumerate(self.model.players):
                multiplication = 1.0
                for k, playerK in enumerate(self.model.players):
                    if k != i and k != j:
                        multiplication *= (playerI.probabilityOfSuccess[playerK.name] + (1 - playerK.salience))
                playerI.probabilityOfStatusQuo[playerJ.name] = multiplication