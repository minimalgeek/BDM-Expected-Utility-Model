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
            offers = []
            for j, playerJ in enumerate(self.__players):
                if i != j:
                    Ei = self.__expectedUtility[i][j]
                    Ej = self.__expectedUtility[j][i]
                    # conflict
                    if Ei > 0 and Ej > 0:
                        if Ej > Ei:
                            offers.append(playerJ.position)
                        else:
                            offers.append(playerI.position)
                    # compromise - i upper hand
                    elif Ei > 0 and Ej < 0 and abs(Ei) > abs(Ej):
                        #newPos = (playerI.position - playerJ.position)*abs(Ej/Ei)
                        offers.append(playerI.position)
                    # compromise - j upper hand
                    elif Ei < 0 and Ej > 0 and abs(Ej) > abs(Ei):
                        newPos = (playerI.position - playerJ.position)*abs(Ei/Ej)
                        offers.append(newPos)
                    # capitulate - i upper hand
                    elif Ei > 0 and Ej < 0 and abs(Ei) < abs(Ej):
                        offers.append(playerI.position)
                    # capitulate - j upper hand
                    elif Ei < 0 and Ej > 0 and abs(Ei) > abs(Ej):
                        offers.append(playerJ.position)
                    # stalemate
                    elif Ei < 0 and Ej < 0:
                        offers.append(playerI.position)
            
            minDistancePosition = min(offers, key = lambda x : abs(x - playerI.position))
            playerI.updatePosition(minDistancePosition)