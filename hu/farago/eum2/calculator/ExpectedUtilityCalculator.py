'''
Created on 2016 máj. 23

@author: Balázs
'''

from typing import Iterable
from hu.farago.eum2.dto.Player import Player

class ExpectedUtilityCalculator():

    __players = []

    def __init__(self, players:Iterable[Player]):
        self.__players = players
        

    def calculateExpectedUtility(self, playerI):
        probabilityOfSuccess = self.calculateAllianceProbability(playerI)
        
    def calculateAllianceProbability(self, playerI):
        length = len(self.__players)
        probabilityOfSuccess = [[0 for x in range(length)] for y in range(length)]
        
        for i, playerI in enumerate(self.__players):
            for j, playerJ in enumerate(self.__players):
                numerator = 0
                denominator = 0
                for k, playerK in enumerate(self.__players):
                    arg = self.calculateAllianceProbabilityArg(playerI, playerJ, playerK)
                    if (arg > 0):
                        numerator += arg
                    denominator += arg
                
                probabilityOfSuccess[i][j] = numerator / denominator
                
        return probabilityOfSuccess
                                    
    def calculateAllianceProbabilityArg(self, voteI: Player, voteJ: Player, voteK: Player):
        return voteK.power()*(abs(voteK.position - voteJ.position) - abs(voteK.position - voteI.position))