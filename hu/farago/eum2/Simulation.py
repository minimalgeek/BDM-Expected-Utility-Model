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
from hu.farago.eum2.calculator.Helper import *

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot

def handlePlotly(data, i):
    #py.sign_in("neural", "u47280okou")
    dataToPlot = createDataToPlot(data, i)
    fileName = '-'.join(['simulation', 
                        str(model.votesIncludeSelf), 
                        str(model.probabilityOfStatusQuoShouldCalculateWithOne),
                        str(model.offerMakerUseTheFirstMatrix),
                        str(model.offerMakerAcceptOffersByMinDistance),
                        str(model.stabilizedDistance)])
    plot(dataToPlot, filename=fileName)

def createDataToPlot(data, i):
    xVec = [z for z in range(i)]
    dataToPlot = []
    for dataItem in data:
        dataToPlot.append(go.Scatter(x=xVec, y=dataItem["values"], mode='lines', name=dataItem["name"]))
    
    return dataToPlot

def printMatrices(model):
    if model.printMatrices:
        print("===== Median Voter =====")
        print(model.medianVoter)
        print("===== Risks =====")
        [dumpclean(player.risk) for player in model.players]
        print("===== Probability Of Success =====")
        [dumpclean(player.probabilityOfSuccess) for player in model.players]
        print("===== Probability Of Status Quo =====")
        [dumpclean(player.probabilityOfStatusQuo) for player in model.players]
        print("===== Ei =====")
        [dumpclean(player.expectedUtilityI) for player in model.players]
        print("===== Ej =====")
        [dumpclean(player.expectedUtilityJ) for player in model.players]

if __name__ == '__main__':
    
    players = PlayerCSVReader().readDefaultPlayers()
    model = Model(players)
    
    model.votesIncludeSelf = False
    model.probabilityOfStatusQuoShouldCalculateWithOne = True
    model.offerMakerUseTheFirstMatrix = False
    model.offerMakerAcceptOffersByMinDistance = False
    model.printMatrices = True
    model.stabilizedDistance = 0.01
    
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
        
        printMatrices(model)
        
        offerMaker.makeOffers()
        print('===== Players at the end of the round =====')
        objectListPrint(players)
        
        for idx, p in enumerate(model.players):
            first_or_default = next((x for x in data if x["name"] == p.name), None)
            first_or_default["values"].append(p.position)
        
        model.calculateMinMax()
        if model.posDistance() <= model.stabilizedDistance or i >= 200:
            shouldRun = False
        i+=1
        print("=========== END OF THE ROUND: %i =============" % i)
        
    handlePlotly(data, i)
    
