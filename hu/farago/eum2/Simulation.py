'''
Created on 2016 máj. 19

@author: Balázs
'''
from hu.farago.eum2.reader.PlayerCSVReader import PlayerCSVReader
from hu.farago.eum2.calculator.MedianVoterPositionCalculator import MedianVoterPositionCalculator
from hu.farago.eum2.calculator.ExpectedUtilityCalculator import ExpectedUtilityCalculator
from hu.farago.eum2.calculator.OfferMaker import OfferMaker
from hu.farago.eum2.calculator.RiskCalculator import RiskCalculator

if __name__ == '__main__':
    
    reader = PlayerCSVReader()
    players = reader.readOilPricePlayers()
    
    print(players)
    
    medianVPC = MedianVoterPositionCalculator(players)
    
    risks = [1 for x in range(len(players))]
    
    for i in range(20):
        medianVPC.calculateMedianVoterPosition()
        medianVoter = medianVPC.getMedianVoterPosition()
        maxDifference = medianVPC.getPositionMaxDifference()
        if maxDifference == 0:
            break
        
        expectedCalc = ExpectedUtilityCalculator(players, medianVoter, maxDifference, risks)
        expUt = expectedCalc.calculateExpectedUtility()
        
        riskCalc = RiskCalculator(players, expUt)
        risks = riskCalc.calculate()
        
        offerMaker = OfferMaker(players, expUt)
        offerMaker.makeOffers()
        
        print(players)
        print("Median Voter:", medianVoter)