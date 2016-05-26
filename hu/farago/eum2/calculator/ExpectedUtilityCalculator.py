'''
Created on 2016 máj. 23

@author: Balázs
'''

from typing import Iterable
from hu.farago.eum2.dto.Player import Player
from hu.farago.eum2.calculator.ProbabilityOfSuccessCalculator import ProbabilityOfSuccessCalculator
from hu.farago.eum2.calculator.ProbabilityOfStatusQuoCalculator import ProbabilityOfStatusQuoCalculator
from hu.farago.eum2.calculator.Utility import *

class ExpectedUtilityCalculator():

    __players = []
    __medianVoter = None
    __maxDifferenceBetweenPositions = 0
    __risks = []

    def __init__(self, players:Iterable[Player], medianVoter:Player, maxDifferenceBetweenPositions, risks):
        self.__players = players
        self.__medianVoter = medianVoter
        self.__maxDifferenceBetweenPositions = maxDifferenceBetweenPositions
        self.__risks = risks
        

    def calculateExpectedUtility(self):
        probSuccCalc = ProbabilityOfSuccessCalculator(self.__players)
        probabilityOfSuccess = probSuccCalc.calculate()
        probSQCalc = ProbabilityOfStatusQuoCalculator(self.__players, probabilityOfSuccess)
        probabilityOfStatusQuo = probSQCalc.calculate()
        
        length = len(self.__players)
        expectedUtility = [[0 for x in range(length)] for y in range(length)]
        
        for i, playerI in enumerate(self.__players):
            for j, playerJ in enumerate(self.__players):
                probSucc = probabilityOfSuccess[i][j]
                probSQ = probabilityOfStatusQuo[i][j]
                
                usi = USI(self.__medianVoter, playerI, playerJ, self.__maxDifferenceBetweenPositions, self.__risks[i]).calculate()
                ufi = UFI(self.__medianVoter, playerI, playerJ, self.__maxDifferenceBetweenPositions, self.__risks[i]).calculate()
                ubi = UBI(self.__medianVoter, playerI, playerJ, self.__maxDifferenceBetweenPositions, self.__risks[i]).calculate()
                uwi = UWI(self.__medianVoter, playerI, playerJ, self.__maxDifferenceBetweenPositions, self.__risks[i]).calculate()
                usq = USQ(self.__medianVoter, playerI, playerJ, self.__maxDifferenceBetweenPositions, self.__risks[i]).calculate()
                
                T = 1
                if playerI.previousPosition != None:
                    prevDistance = abs(playerI.previousPosition - playerJ.previousPosition)
                    currentDistance = abs(playerI.position - playerJ.position)
                    if prevDistance > currentDistance:
                        T = 1
                    else:
                        T = 0
                
                expectedUtility[i][j] = playerJ.salience*(probSucc*usi + (1-probSucc)*ufi) + \
                                        (1 - playerJ.salience)*usi - probSQ*usq - \
                                        (1 - probSQ)*(T*ubi + (1 - T)*uwi)
        
        return expectedUtility