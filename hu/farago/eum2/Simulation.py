'''
Created on 2016 máj. 19

@author: Balázs

'''
from hu.farago.eum2.reader.PlayerCSVReader import PlayerCSVReader
from hu.farago.eum2.calculator.MedianVoterPositionCalculator import MedianVoterPositionCalculator
from hu.farago.eum2.calculator.ExpectedUtilityCalculator import ExpectedUtilityCalculator
from hu.farago.eum2.calculator.OfferMaker import OfferMaker
from hu.farago.eum2.calculator.RiskCalculator import RiskCalculator
from hu.farago.eum2.calculator.Helper import objectListPrint

import plotly.plotly as py
import plotly.graph_objs as go

def createDataToPlot(data, i):
    xVec = [z for z in range(i)]
    dataToPlot = []
    for dataItem in data:
        dataToPlot.append(go.Scatter(x=xVec, y=dataItem["values"], mode='lines', name=dataItem["name"]))
    
    return dataToPlot

if __name__ == '__main__':
    
    reader = PlayerCSVReader()
    players = reader.readOilPricePlayers()
    objectListPrint(players);
    
    print("================ START ================")    
    medianVPC = MedianVoterPositionCalculator(players)
    
    risks = [1 for x in range(len(players))]
    
    data = [{"name":x.name, "values":[]} for x in players]
    i = 0
    for i in range(50):
        medianVPC.calculateMedianVoterPosition()
        medianVoter = medianVPC.getMedianVoterPosition()
        print("Median Voter:", medianVoter, '\n')
        maxDifference = medianVPC.getPositionMaxDifference()
        if maxDifference == 0:
            break
        
        expectedCalc = ExpectedUtilityCalculator(players, medianVoter, maxDifference, risks)
        expectedCalc.calculateExpectedUtility()
        
        riskCalc = RiskCalculator(players, expectedCalc.get_expected_utility_ij())
        risks = riskCalc.calculate()
        
        offerMaker = OfferMaker(players, expectedCalc)
        offerMaker.makeOffers()
        
        for i, p in enumerate(players):
            print(p)
            first_or_default = next((x for x in data if x["name"] == p.name), None)
            first_or_default["values"].append(p.position)
        
        print("=========== END OF THE ROUND =============")
    
    py.sign_in("neural", "u47280okou")

    dataToPlot = createDataToPlot(data, i)
    
    # Plot and embed in ipython notebook!
    py.iplot(dataToPlot, filename='line-mode')
    
