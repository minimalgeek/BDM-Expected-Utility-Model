'''
Created on 2016 máj. 19

@author: Balázs
'''
from hu.farago.eum2.reader.PlayerCSVReader import PlayerCSVReader
from hu.farago.eum2.calculator.MedianVoterPositionCalculator import MedianVoterPositionCalculator

if __name__ == '__main__':
    
    reader = PlayerCSVReader()
    players = reader.readOilPricePlayers()
    
    print(players)
    
    medianVPC = MedianVoterPositionCalculator(players)
    medianVPC.calculateMedianVoterPosition()
    
    medianVoter = medianVPC.getMedianVoterPosition()
    maxDifference = medianVPC.getPositionMaxDifference()
    
    