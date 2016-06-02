'''
Created on 2016 máj. 23

@author: Balázs
'''

from typing import Iterable
from hu.farago.eum2.dto.Player import Player
from hu.farago.eum2.calculator.ProbabilityOfSuccessCalculator import ProbabilityOfSuccessCalculator
from hu.farago.eum2.calculator.ProbabilityOfStatusQuoCalculator import ProbabilityOfStatusQuoCalculator
from hu.farago.eum2.calculator.Utility import *
from hu.farago.eum2.calculator.Helper import tablePrint

class ExpectedUtilityCalculator():

    __players = []
    __medianVoter = None
    __maxDifferenceBetweenPositions = 0
    __risks = []

    __expectedUtilityIJ = []
    __expectedUtilityJI = []

    def __init__(self, players:Iterable[Player], medianVoter:Player, maxDifferenceBetweenPositions, risks):
        self.__players = players
        self.__medianVoter = medianVoter
        self.__maxDifferenceBetweenPositions = maxDifferenceBetweenPositions
        self.__risks = risks

    def get_expected_utility_ij(self):
        return self.__expectedUtilityIJ


    def get_expected_utility_ji(self):
        return self.__expectedUtilityJI

    def calculateExpectedUtility(self):
        probSuccCalc = ProbabilityOfSuccessCalculator(self.__players)
        probabilityOfSuccess = probSuccCalc.calculate()
        probSQCalc = ProbabilityOfStatusQuoCalculator(self.__players, probabilityOfSuccess)
        probabilityOfStatusQuo = probSQCalc.calculate()
        
        length = len(self.__players)
        
        self.__expectedUtilityIJ = [[0 for x in range(length)] for y in range(length)]
        self.__expectedUtilityJI = [[0 for x in range(length)] for y in range(length)]
        
        for i, playerI in enumerate(self.__players):
            for j, playerJ in enumerate(self.__players):
                probSucc = probabilityOfSuccess[i][j]
                probSQ = 1 #probabilityOfStatusQuo[i][j]
                
                usi = USI(self.__medianVoter, playerI, playerJ, self.__maxDifferenceBetweenPositions, self.__risks[i]).calculate()
                ufi = UFI(self.__medianVoter, playerI, playerJ, self.__maxDifferenceBetweenPositions, self.__risks[i]).calculate()
                ubi = UBI(self.__medianVoter, playerI, playerJ, self.__maxDifferenceBetweenPositions, self.__risks[i]).calculate()
                uwi = UWI(self.__medianVoter, playerI, playerJ, self.__maxDifferenceBetweenPositions, self.__risks[i]).calculate()
                usq = USQ(self.__medianVoter, playerI, playerJ, self.__maxDifferenceBetweenPositions, self.__risks[i]).calculate()
                
                T = 1

                prevDistance = abs(playerI.previousPosition - playerJ.previousPosition)
                currentDistance = abs(playerI.position - playerJ.position)
                if prevDistance >= currentDistance:
                    T = 1
                else:
                    T = 0
                
                self.__expectedUtilityIJ[i][j] = playerJ.salience*(probSucc*usi + (1-probSucc)*ufi) + \
                                        (1 - playerJ.salience)*usi - probSQ*usq - \
                                        (1 - probSQ)*(T*ubi + (1 - T)*uwi)
                                        
                probSucc = probabilityOfSuccess[j][i]
                probSQ = 1 #probabilityOfStatusQuo[i][j]
                
                usi = USI(self.__medianVoter, playerJ, playerI, self.__maxDifferenceBetweenPositions, self.__risks[j]).calculate()
                ufi = UFI(self.__medianVoter, playerJ, playerI, self.__maxDifferenceBetweenPositions, self.__risks[j]).calculate()
                ubi = UBI(self.__medianVoter, playerJ, playerI, self.__maxDifferenceBetweenPositions, self.__risks[j]).calculate()
                uwi = UWI(self.__medianVoter, playerJ, playerI, self.__maxDifferenceBetweenPositions, self.__risks[j]).calculate()
                usq = USQ(self.__medianVoter, playerJ, playerI, self.__maxDifferenceBetweenPositions, self.__risks[j]).calculate()
                
                self.__expectedUtilityJI[i][j] = playerJ.salience*(probSucc*usi + (1-probSucc)*ufi) + \
                                        (1 - playerJ.salience)*usi - probSQ*usq - \
                                        (1 - probSQ)*(T*ubi + (1 - T)*uwi)
        
        print ("==== Expected Utility Matrix IJ =====")
        tablePrint(self.__expectedUtilityIJ)
        
        print ("==== Expected Utility Matrix JI =====")
        tablePrint(self.__expectedUtilityJI)
