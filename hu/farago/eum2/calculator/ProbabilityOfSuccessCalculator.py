'''
Created on 2016 máj. 24

@author: Balázs
'''

from hu.farago.eum2.dto.Player import Player
from hu.farago.eum2.dto.Model import Model
from hu.farago.eum2.calculator.Helper import tablePrint

class ProbabilityOfSuccessCalculator(object):

    def __init__(self, model:Model):
        self.model = model

    def calculate(self):
        players = self.model.players        
        for i, playerI in enumerate(players):
            for j, playerJ in enumerate(players):
                numerator = 0
                denominator = 0

                for k, playerK in enumerate(players):
                    if k != i and k != j:
                        arg = self.calculateAllianceProbabilityArg(playerI, playerJ, playerK)
                        if (arg > 0):
                            numerator += arg
                        denominator += abs(arg)
                    
                if denominator != 0:
                    playerI.probabilityOfSuccess[playerJ.name] = (numerator / denominator)
                else:
                    playerI.probabilityOfSuccess[playerJ.name] = 0
                                                            
    def calculateAllianceProbabilityArg(self, voteI: Player, voteJ: Player, voteK: Player):
        return voteK.power()*(abs(voteK.position - voteJ.position) - abs(voteK.position - voteI.position))
    
