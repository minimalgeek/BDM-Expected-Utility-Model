'''
Created on 2016 máj. 25

@author: Balázs
'''
from collections import defaultdict
from hu.farago.eum2_Cahi.calculator.Helper import objectListPrint

class OfferMaker(object):

    __players = None
    __expectedCalc = None
    
    def __init__(self, players, expectedCalc):
        self.__players = players
        self.__expectedCalc = expectedCalc
        
    def makeOffers(self):
        
        for i, playerI in enumerate(self.__players):
            # calculate where i get offers from
            playerI.offers = []
            for j, playerJ in enumerate(self.__players):
                if i != j and playerI.position != playerJ.position:
                    EIi = self.__expectedCalc.get_expected_utility_ij()[j][i]               #az i ilyennek látja saját győzelmének hasznosságát
                    EIj = self.__expectedCalc.get_expected_utility_ji()[j][i]               #i azt gondolja, hogy ha j győz, akkor ennek j ilyen hasznoságot tulajdonít

                    EJj = self.__expectedCalc.get_expected_utility_ij()[i][j]               #az j ilyennek látja saját győzelmének hasznosságát
                    EJi = self.__expectedCalc.get_expected_utility_ji()[i][j]               #j azt gondolja, hogy ha i győz, akkor ennek i ilyen hasznoságot tulajdonít

                    if EIi > EIj and EJj > EJi:
                        if playerI.power() >= playerJ.power():
                            playerI.offers.append(Offer(playerJ, Offer.CONFRONTATION, playerI.position, EIi))
                        elif playerI.power() < playerJ.power():
                            playerI.offers.append(Offer(playerJ, Offer.CONFRONTATION, playerJ.position, EIi))
                            
                    elif EIi > 0 and EIj < 0 and abs(EIi) > abs(EIj) and EJj < 0 and EJi > 0 and abs(EJj) < abs(EJi) :
    
                        xHat = playerJ.power() * ((playerI.position - playerJ.position)/(playerI.power() + playerJ.power()))
                        playerI.offers.append(Offer(playerJ, Offer.COMPROMISE, playerI.position - xHat, EIi))
                        
                    elif EIi > 0 and EIj < 0 and abs(EIi) < abs(EIj):
                        playerI.offers.append(Offer(playerJ, Offer.CAPITULATION, playerJ.position, EIi))
                        
            print("==== Offers for %s ====" % playerI.name)
            objectListPrint(playerI.offers)
        
        for player in self.__players:
            if len(player.offers) > 0:
                
                max_util = max([offer.eu for offer in player.offers])
                max_offers = [offer for offer in player.offers if offer.eu == max_util]
                offer = min(max_offers, key=lambda x: abs(player.position - x.offered_position))
                
                #bestOfferFunc = lambda offer : abs(offer.offered_position - player.position)
                #bestOffer = min(player.offers, key = bestOfferFunc)
                
                player.updatePosition(offer.offered_position)
                
class Offer(object):
    CONFRONTATION = 'confrontation'
    COMPROMISE = 'compromise'
    CAPITULATION = 'capitulation'
    OFFER_TYPES = (
        CONFRONTATION,
        COMPROMISE,
        CAPITULATION,
    )

    def __init__(self, other_actor, offer_type, offered_position, eu):
        if offer_type not in self.OFFER_TYPES:
            raise ValueError('offer_type "%s" not in %s'
                             % (offer_type, self.OFFER_TYPES))

        self.other_actor = other_actor  # actor proposing the offer
        self.offer_type = offer_type
        self.offered_position = offered_position
        self.eu = eu
        
    def __str__(self):
        return ','.join([self.other_actor.name, self.offer_type, str(round(self.offered_position, 3))])
