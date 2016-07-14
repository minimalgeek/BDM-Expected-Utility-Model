'''
Created on 2016 június

@author: Balázs + Gábor

'''
from hu.farago.eum2_Cahi.reader.PlayerCSVReader import PlayerCSVReader
from hu.farago.eum2_Cahi.calculator.MedianVoterPositionCalculator import MedianVoterPositionCalculator
from hu.farago.eum2_Cahi.calculator.ExpectedUtilityCalculator import ExpectedUtilityCalculator
from hu.farago.eum2_Cahi.calculator.OfferMaker import OfferMaker
#from hu.farago.eum2_Cahi.calculator.OfferMaker3 import OfferMaker
from hu.farago.eum2_Cahi.calculator.RiskCalculator import RiskCalculator
from hu.farago.eum2_Cahi.calculator.Helper import objectListPrint
from hu import APP_RESOURCES

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot

def createDataToPlot(data, i):
    xVec = [z for z in range(i)]
    dataToPlot = []
    for dataItem in data:
        dataToPlot.append(go.Scatter(x=xVec, y=dataItem["values"], mode='lines', name=dataItem["name"]))
    
    return dataToPlot

if __name__ == '__main__':
    
    #players = PlayerCSVReader().readPlayers(APP_RESOURCES + "countries_test.csv")
    players = PlayerCSVReader().readPlayers(APP_RESOURCES + "WW1.csv")
    objectListPrint(players)
    
    print("================ START ================")    
    medianVPC = MedianVoterPositionCalculator(players)
    
    risks = [1 for x in range(len(players))]
    
    data = [{"name":x.name, "values":[x.position]} for x in players]
    
    i = 0
    for i in range(10):                              #RANGE!!!
        medianVPC.calculateMedianVoterPosition()
        medianVoter = medianVPC.getMedianVoterPosition()
        print("==> Median Voter:", medianVoter, '\n')
        maxDifference = medianVPC.getPositionMaxDifference()
        if maxDifference == 0:
            break
        
        expectedCalc = ExpectedUtilityCalculator(players, medianVoter, maxDifference, risks)
        expectedCalc.calculateExpectedUtility()



        riskCalc = RiskCalculator(players, expectedCalc.get_expected_utility_ij())
        risks = riskCalc.calculate()

        if i >= 1:        
            offerMaker = OfferMaker(players, expectedCalc)
            offerMaker.makeOffers()
        
            for idx, p in enumerate(players):
                print(p.name," old: ",round(p.previousPosition,4)," ==> new positions:", round(p.position,4), '\n')
                first_or_default = next((x for x in data if x["name"] == p.name), None)
                first_or_default["values"].append(p.position)
        
        print("=========== END OF THE ROUND: %i =============" % i)
    
    #py.sign_in("neural", "u47280okou")

    dataToPlot = createDataToPlot(data, i)
    
    # Plot and embed in ipython notebook!
    #py.iplot(dataToPlot, filename='line-mode')
    plot(dataToPlot, filename='line-mode')
    
