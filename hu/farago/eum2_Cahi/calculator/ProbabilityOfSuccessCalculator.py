'''
Created on 2016 máj. 24

@author: Balázs
'''

from typing import Iterable
from hu.farago.eum2_Cahi.dto.Player import Player
from hu.farago.eum2_Cahi.calculator.Helper import tablePrint

class ProbabilityOfSuccessCalculator(object):

    __players = []

    def __init__(self, players:Iterable[Player]):
        self.__players = players

    def calculate(self):
        length = len(self.__players)
        probabilityOfSuccess = [[0 for x in range(length)] for y in range(length)]
        
        for i, playerI in enumerate(self.__players):
            for j, playerJ in enumerate(self.__players):
                numerator = 0
                denominator = 0

                for k, playerK in enumerate(self.__players):
                    if k != i and k != j:
                        arg = self.calculateAllianceProbabilityArg(playerI, playerJ, playerK)
                        if (arg > 0):
                            numerator += arg
                        denominator += abs(arg)
                    
                if denominator != 0:
                    probabilityOfSuccess[i][j] = (numerator / denominator)
                else:
                    # is it right?
                    probabilityOfSuccess[i][j] = 0
                    
        print ("====Prob of Success =====")
        tablePrint(probabilityOfSuccess)

        return probabilityOfSuccess
                                    
    def calculateAllianceProbabilityArg(self, voteI: Player, voteJ: Player, voteK: Player):
        return voteK.power()*(abs(voteK.position - voteJ.position) - abs(voteK.position - voteI.position))
    
