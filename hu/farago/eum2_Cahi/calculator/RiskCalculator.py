'''
Created on 2016 máj. 26

@author: Balázs
'''

from hu.farago.eum2_Cahi.calculator.Helper import objectListPrint


class RiskCalculator(object):
    
    __players = None
    __expectedUtility = None

    def __init__(self, players, expectedUtility):
        self.__players = players
        self.__expectedUtility = expectedUtility
    
    def calculate(self):
        
        sums = []
        
        length = len(self.__expectedUtility)
        for i in range(length):
            euSum = 0
            for j in range(length):
                if j != i:
                    euSum += self.__expectedUtility[i][j]
            
            sums.append(euSum)
        
        maxSum = max(sums)
        minSum = min(sums)
        
        riskVector = []
        for i in range(length):
            Ri = (2 * sums[i] - maxSum - minSum)/(maxSum - minSum)
            ri = (1 - Ri/3)/(1 + Ri/3)
            riskVector.append(ri)

        print ("==== risk vector =====")
        objectListPrint(riskVector)    
            
        return riskVector
