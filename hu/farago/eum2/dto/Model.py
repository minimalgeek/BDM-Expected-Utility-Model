'''
Created on 2016 jún. 9

@author: Balázs
'''

from hu.farago.eum2.dto.Player import Player

class Model(object):

    votesIncludeSelf = False
    probabilityOfStatusQuoShouldCalculateWithOne = True
    offerMakerUseTheFirstMatrix = False
    offerMakerAcceptOffersByMinDistance = False
    printMatrices = True
    stabilizedDistance = 0.001

    players = []
    minPos = None
    maxPos = None
    medianVoter = None

    def __init__(self, players):
        self.players = players
        
    def posDistance(self):
        return abs(self.maxPos - self.minPos)
    
    def calculateMinMax(self):
        def playerPos(p):
            return p.position

        self.minPos = min(self.players, key=playerPos).position
        self.maxPos = max(self.players, key=playerPos).position