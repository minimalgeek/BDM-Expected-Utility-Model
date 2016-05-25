'''
Created on 2016 máj. 25

@author: Balázs
'''

class OfferMaker(object):

    __players = None
    __expectedUtility = None

    def __init__(self, players, expectedUtility):
        self.__players = players
        self.__expectedUtility = expectedUtility
        
    def makeOffers(self):
        
        for i, playerI in enumerate(self.__players):
            for j, playerJ in enumerate(self.__players):
                Ei = self.__expectedUtility[i][j]
                Ej = self.__expectedUtility[j][i]
                # conflict
                if Ei > 0 and Ej > 0:
                    if Ej > Ei:
                        playerI.updatePosition(playerJ.position)
                        playerJ.updatePosition(playerJ.position)
                    else:
                        playerJ.updatePosition(playerI.position)
                        playerI.updatePosition(playerI.position)
                # compromise - i upper hand
                elif Ei > 0 and Ej < 0 and Ei > abs(Ej):
                    newPos = (playerI.position - playerJ.position)*abs(Ej/Ei)
                    playerJ.updatePosition(newPos)
                    playerI.updatePosition(playerI.position)
                # compromise - j upper hand
                elif Ei < 0 and Ej > 0 and Ej > abs(Ei):
                    newPos = (playerI.position - playerJ.position)*abs(Ei/Ej)
                    playerI.updatePosition(newPos)
                    playerJ.updatePosition(playerJ.position)
                # capitulate - i upper hand
                elif Ei > 0 and Ej < 0 and Ei < abs(Ej):
                    playerJ.updatePosition(playerI.position)
                    playerI.updatePosition(playerI.position)
                # capitulate - j upper hand
                elif Ei < 0 and Ej > 0 and abs(Ei) > Ej:
                    playerI.updatePosition(playerJ.position)
                    playerJ.updatePosition(playerJ.position)
                # stalemate
                elif Ei < 0 and Ej < 0:
                    playerI.updatePosition(playerI.position)
                    playerJ.updatePosition(playerJ.position)
                    
                    