'''
Created on 2016 máj. 19

@author: Balázs
'''
from hu.farago.eum2.reader.PlayerCSVReader import PlayerCSVReader
from hu.farago.eum2.calculator.MedianVoterPositionCalculator import MedianVoterPositionCalculator
from hu.farago.eum2.calculator.ExpectedUtilityCalculator import ExpectedUtilityCalculator
from hu.farago.eum2.calculator.OfferMaker import OfferMaker

if __name__ == '__main__':
    
    reader = PlayerCSVReader()
    players = reader.readOilPricePlayers()
    
    print(players)
    
    medianVPC = MedianVoterPositionCalculator(players)
    
    for i in range(20):
        medianVPC.calculateMedianVoterPosition()
        medianVoter = medianVPC.getMedianVoterPosition()
        maxDifference = medianVPC.getPositionMaxDifference()
        if maxDifference == 0:
            break
        
        expectedCalc = ExpectedUtilityCalculator(players, medianVoter, maxDifference)
        expUt = expectedCalc.calculateExpectedUtility()
        
        offerMaker = OfferMaker(players, expUt)
        offerMaker.makeOffers()
        
        print(players)