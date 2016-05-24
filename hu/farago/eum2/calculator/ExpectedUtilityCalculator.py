'''
Created on 2016 máj. 23

@author: Balázs
'''

from typing import Iterable
from hu.farago.eum2.dto.Player import Player
from hu.farago.eum2.calculator.ProbabilityOfSuccessCalculator import ProbabilityOfSuccessCalculator
from hu.farago.eum2.calculator.ProbabilityOfStatusQuoCalculator import ProbabilityOfStatusQuoCalculator

class ExpectedUtilityCalculator():

    __players = []
    __medianVoter = None
    __maxDifferenceBetweenPositions = 0

    def __init__(self, players:Iterable[Player], medianVoter:Player, maxDifferenceBetweenPositions):
        self.__players = players
        self.__medianVoter = medianVoter
        self.__maxDifferenceBetweenPositions = maxDifferenceBetweenPositions
        

    def calculateExpectedUtility(self):
        probSuccCalc = ProbabilityOfSuccessCalculator(self.__players)
        probabilityOfSuccess = probSuccCalc.calculate()
        probSQCalc = ProbabilityOfStatusQuoCalculator(self.__players, probabilityOfSuccess)
        probabilityOfStatusQuo = probSQCalc.calculate()
        
        print(probabilityOfStatusQuo)
    