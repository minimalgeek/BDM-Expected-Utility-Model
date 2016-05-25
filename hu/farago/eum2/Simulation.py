'''
Created on 2016 máj. 19

@author: Balázs
'''
from hu.farago.eum2.reader.PlayerCSVReader import PlayerCSVReader
from hu.farago.eum2.calculator.MedianVoterPositionCalculator import MedianVoterPositionCalculator
from hu.farago.eum2.calculator.ExpectedUtilityCalculator import ExpectedUtilityCalculator

if __name__ == '__main__':
    
    reader = PlayerCSVReader()
    players = reader.readOilPricePlayers()
    
    print(players)
    
    anyPossibleOffer = True
    medianVPC = MedianVoterPositionCalculator(players)
    
    while anyPossibleOffer:
        medianVPC.calculateMedianVoterPosition()
        medianVoter = medianVPC.getMedianVoterPosition()
        maxDifference = medianVPC.getPositionMaxDifference()
        
        expectedCalc = ExpectedUtilityCalculator(players, medianVoter, maxDifference)
        expectedCalc.calculateExpectedUtility()
        
        