'''
Created on 2016 máj. 24

@author: Balázs
'''

from typing import Iterable
from hu.farago.eum2.dto.Player import Player

class ProbabilityOfStatusQuoCalculator(object):

    __players = []
    __probabilitOfSuccess = []

    def __init__(self, players:Iterable[Player], probabilitOfSuccess):
        self.__players = players
        self.__probabilitOfSuccess = probabilitOfSuccess

    def calculate(self):
        length = len(self.__players)
        probabilityOfStatusQuo = [[0 for x in range(length)] for y in range(length)]
        
        for i, playerI in enumerate(self.__players):
            for j, playerJ in enumerate(self.__players):
                multiplication = 1.0
                for k, playerK in enumerate(self.__players):
                    if k != i and k != j:
                        multiplication *= (self.__probabilitOfSuccess[i][k] + (1 - playerK.salience))
                probabilityOfStatusQuo[i][j] = multiplication
        return probabilityOfStatusQuo