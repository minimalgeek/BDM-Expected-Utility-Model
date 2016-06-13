'''
Created on 2016 máj. 19

@author: Balázs
'''

from hu.farago.eum2.dto.Player import Player
from hu.farago.eum2.dto.Model import Model
from hu.farago.eum2.calculator.Helper import tablePrint

class MedianVoterPositionCalculator():

    def __init__(self, model:Model):
        self.model = model

    def calculate(self):

        players = self.model.players
        
        for j, playerJ in enumerate(players):
            playerJ.sumOfVotes = 0
            for k, playerK in enumerate(players):
                sumOfVotes = 0
                for i, playerI in enumerate(players):
                    if self.model.votesIncludeSelf:
                        sumOfVotes += self.voteBetweenPlayers(playerI, playerJ, playerK)
                    else:
                        if i != j and i != k:
                            sumOfVotes += self.voteBetweenPlayers(playerI, playerJ, playerK)
                
                playerJ.addToSum(sumOfVotes)

        self.model.medianVoter = max(players, key=lambda x: x.sumOfVotes)
        
    def voteBetweenPlayers(self, voteI: Player, voteJ: Player, voteK: Player):
        diffIK = abs(voteI.position - voteK.position)
        diffIJ = abs(voteI.position - voteJ.position)
        
        return voteI.power()*((diffIK - diffIJ)/self.model.posDistance())
        
