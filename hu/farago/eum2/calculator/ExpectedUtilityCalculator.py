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
from hu.farago.eum2.dto.Model import Model

class ExpectedUtilityCalculator():
    
    def __init__(self, model:Model):
        self.model = model

    def calculate(self):
        ProbabilityOfSuccessCalculator(self.model).calculate()
        ProbabilityOfStatusQuoCalculator(self.model).calculate()
        
        for i, playerI in enumerate(self.model.players):
            for j, playerJ in enumerate(self.model.players):
                #if (i != j):
                probSucc = playerI.probabilityOfSuccess[playerJ.name]
                probSQ = playerI.probabilityOfStatusQuo[playerJ.name]
                
                if self.model.probabilityOfStatusQuoShouldCalculateWithOne:
                    probSQ = 1
                
                usi = USI(playerI, playerJ, self.model).calculate()
                ufi = UFI(playerI, playerJ, self.model).calculate()
                ubi = UBI(playerI, playerJ, self.model).calculate()
                uwi = UWI(playerI, playerJ, self.model).calculate()
                usq = USQ(playerI, playerJ, self.model).calculate()
                
                T = 1

                prevDistance = abs(playerI.previousPosition - playerJ.previousPosition)
                currentDistance = abs(playerI.position - playerJ.position)
                if prevDistance >= currentDistance:
                    T = 1
                else:
                    T = 0

                playerI.expectedUtilityI[playerJ.name] = playerJ.salience*(probSucc*usi + (1-probSucc)*ufi) + \
                                        (1 - playerJ.salience)*usi - probSQ*usq - \
                                        (1 - probSQ)*(T*ubi + (1 - T)*uwi)
                
                probSucc = playerJ.probabilityOfSuccess[playerI.name]
                probSQ = playerJ.probabilityOfStatusQuo[playerI.name]
                
                if self.model.probabilityOfStatusQuoShouldCalculateWithOne:
                    probSQ = 1
                
                usi = USI(playerJ, playerI, self.model).calculate()
                ufi = UFI(playerJ, playerI, self.model).calculate()
                ubi = UBI(playerJ, playerI, self.model).calculate()
                uwi = UWI(playerJ, playerI, self.model).calculate()
                usq = USQ(playerJ, playerI, self.model).calculate()
                
                playerI.expectedUtilityJ[playerJ.name] = playerJ.salience*(probSucc*usi + (1-probSucc)*ufi) + \
                                        (1 - playerJ.salience)*usi - probSQ*usq - \
                                        (1 - probSQ)*(T*ubi + (1 - T)*uwi)
                