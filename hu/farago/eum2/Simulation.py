'''
Created on 2016 máj. 19

@author: Balázs
'''
from hu.farago.eum2.reader.PlayerCSVReader import PlayerCSVReader
from hu.farago.eum2.dto.Model import Model
from hu.farago.eum2.calculator.MedianVoterPositionCalculator import MedianVoterPositionCalculator
from hu.farago.eum2.calculator.ExpectedUtilityCalculator import ExpectedUtilityCalculator
from hu.farago.eum2.calculator.OfferMaker import OfferMaker
from hu.farago.eum2.calculator.RiskCalculator import RiskCalculator
from hu.farago.eum2.calculator.Helper import objectListPrint

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot

def handlePlotly(data, i):
    #py.sign_in("neural", "u47280okou")
    dataToPlot = createDataToPlot(data, i)
    plot(dataToPlot, filename='line-mode')

def createDataToPlot(data, i):
    xVec = [z for z in range(i)]
    dataToPlot = []
    for dataItem in data:
        dataToPlot.append(go.Scatter(x=xVec, y=dataItem["values"], mode='lines', name=dataItem["name"]))
    
    return dataToPlot

if __name__ == '__main__':
    
    players = PlayerCSVReader().readDefaultPlayers()
    model = Model(players)
    
    model.votesIncludeSelf = False
    model.probabilityOfStatusQuoShouldCalculateWithOne = False
    model.offerMakerUseTheFirstMatrix = False
    model.offerMakerAcceptOffersByMinDistance = False
    model.stabilizedDistance = 0.001
    
    objectListPrint(players)
    print("================ START ================")    
    
    medianVPC = MedianVoterPositionCalculator(model)
    expectedCalc = ExpectedUtilityCalculator(model)
    riskCalc = RiskCalculator(model)
    offerMaker = OfferMaker(model)
    
    data = [{"name":x.name, "values":[x.position]} for x in players]
    
    shouldRun = True
    i = 0
    model.calculateMinMax()
    while shouldRun:
        
        medianVPC.calculate()
        expectedCalc.calculate()
        riskCalc.calculate()
        offerMaker.makeOffers()
        
        for idx, p in enumerate(model.players):
            first_or_default = next((x for x in data if x["name"] == p.name), None)
            first_or_default["values"].append(p.position)
        
        objectListPrint(players)
        
        model.calculateMinMax()
        if model.posDistance() <= model.stabilizedDistance or i >= 200:
            shouldRun = False
        i+=1
        print("=========== END OF THE ROUND: %i =============" % i)
        
    handlePlotly(data, i)
    
