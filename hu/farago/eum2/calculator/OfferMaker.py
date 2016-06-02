'''
Created on 2016 máj. 25

@author: Balázs
'''

class OfferMaker(object):

    __players = None
    __expectedUtilityCalculator = None

    def __init__(self, players, expectedUtilityCalculator):
        self.__players = players
        self.__expectedUtilityCalculator = expectedUtilityCalculator
        
    def makeOffers(self):
        
        offersMatrix = []
        for i, playerI in enumerate(self.__players):
            offers = []
            # calculate where i get offers from
            for j, playerJ in enumerate(self.__players):
                if i != j:
                    Ei = self.__expectedUtilityCalculator.get_expected_utility_ij()[i][j]
                    Ej = self.__expectedUtilityCalculator.get_expected_utility_ji()[i][j]
                    # conflict
                    if Ei > 0 and Ej > 0 and Ej > Ei:
                        offers.append({"force": Ei, "position": playerJ.position})
                    # compromise
                    elif Ei < 0 and Ej > 0 and abs(Ei) < abs(Ej):
                        newPos = (playerI.position - playerJ.position)*abs(Ei/Ej)
                        offers.append({"force": Ei, "position": playerI.position - newPos})
                    # capitulate
                    elif Ei < 0 and Ej > 0 and abs(Ei) > abs(Ej):
                        offers.append({"force": Ei, "position": playerJ.position})
            offersMatrix.append(offers)
        
        #print("Offers matrix: ", offersMatrix) 
        for i, offersForI in enumerate(offersMatrix):
            if len(offersForI) > 0:
                player = self.__players[i]
                minDistancePosition = max(offersForI, key = lambda x : x["force"])["position"]
                player.updatePosition(minDistancePosition)