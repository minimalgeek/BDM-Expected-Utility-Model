'''
Created on 2016 máj. 19

@author: Balázs
'''

from typing import Iterable
from hu.farago.eum2.dto.Player import Player
from hu.farago.eum2.calculator.Helper import tablePrint

class MedianVoterPositionCalculator():

    __players = []
    __positionMin = 0
    __positionMax = 0
    
    __positionMaxDifference = 0
    __medianVoterPosition = None

    def __init__(self, players:Iterable[Player]):
        self.__players = players

    def getPositionMaxDifference(self):
        return self.__positionMaxDifference
    
    def getMedianVoterPosition(self):
        return self.__medianVoterPosition

    def calculateMedianVoterPosition(self):
        def playerPos(p):
            return p.position
        
        # self.__players.sort(key=playerPos)
        self.__positionMin = min(self.__players, key=playerPos).position
        self.__positionMax = max(self.__players, key=playerPos).position
        self.__positionMaxDifference = abs(self.__positionMax - self.__positionMin)
        
        if self.__positionMaxDifference == 0:
            return
        
        length = len(self.__players)
        votesForJVersusK = [[0 for x in range(length)] for y in range(length)]
        
        for j, playerJ in enumerate(self.__players):
            for k, playerK in enumerate(self.__players):
                sumOfVotes = 0
                for playerI in self.__players:
                    #if playerI != playerJ and playerI != playerK:
                    sumOfVotes += self.voteBetweenPlayers(playerI, playerJ, playerK)
                
                votesForJVersusK[j][k] = sumOfVotes
                playerJ.addToSum(sumOfVotes)
                
        #tablePrint(votesForJVersusK)
        
        self.__medianVoterPosition = max(self.__players, key=lambda x: x.sumOfVotes)
        
    def voteBetweenPlayers(self, voteI: Player, voteJ: Player, voteK: Player):
        diffIK = abs(voteI.position - voteK.position)
        diffIJ = abs(voteI.position - voteJ.position)
        
        return voteI.power()*((diffIK - diffIJ)/self.__positionMaxDifference)
        
