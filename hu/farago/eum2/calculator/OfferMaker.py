'''
Created on 2016 máj. 25

@author: Balázs
'''

from collections import defaultdict
from hu.farago.eum2.dto.Model import Model
from hu.farago.eum2.calculator.Helper import objectListPrint

class OfferMaker(object):
    
    def __init__(self, model:Model):
        self.model = model

    def makeOffers(self):
        
        for playerI in self.model.players:
            playerI.offers = {}
            for playerJ in self.model.players:
                if playerI.position != playerJ.position:
                    if self.model.offerMakerUseTheFirstMatrix:
                        Ei = playerJ.expectedUtilityI[playerI.name]
                        Ej = playerI.expectedUtilityI[playerJ.name]
    
                        if Ei > Ej > 0:
                            playerI.offers[playerJ.name] = Offer(playerJ, Offer.CONFRONTATION, playerJ.position, Ei)
                        elif Ei > 0 and Ej < 0 and abs(Ei) > abs(Ej):
                            xHat = (playerI.position - playerJ.position)/abs(Ei/Ej)
                            playerI.offers[playerJ.name] = Offer(playerJ, Offer.COMPROMISE, playerI.position - xHat, Ei)
                        elif Ei > 0 and Ej < 0 and abs(Ei) < abs(Ej):
                            playerI.offers[playerJ.name] = Offer(playerJ, Offer.CAPITULATION, playerJ.position, Ei)
                    else:
                        Ei = playerJ.expectedUtilityI[playerI.name]
                        Ej = playerJ.expectedUtilityJ[playerI.name]
    
                        if Ei > Ej > 0:
                            playerI.offers[playerJ.name] = Offer(playerJ, Offer.CONFRONTATION, playerJ.position, Ei)
                        elif Ei > 0 and Ej < 0 and abs(Ei) > abs(Ej):
                            xHat = (playerI.position - playerJ.position)/abs(Ei/Ej)
                            playerI.offers[playerJ.name] = Offer(playerJ, Offer.COMPROMISE, playerI.position - xHat, Ei)
                        elif Ei > 0 and Ej < 0 and abs(Ei) < abs(Ej):
                            playerI.offers[playerJ.name] = Offer(playerJ, Offer.CAPITULATION, playerJ.position, Ei)
                        
            print("==== Offers for %s ====" % playerI.name)
            objectListPrint(playerI.offers.values())
        
        for player in self.model.players:
            if len(player.offers) > 0:
                if self.model.offerMakerAcceptOffersByMinDistance:
                    offer = min(player.offers.values(), key=lambda x: abs(player.position - x.offered_position))
                    # player.updatePosition(offer.offered_position)
                    player.bestOffer = offer
                else:
                    max_util = max([offer.eu for offer in player.offers.values()])
                    max_offers = [offer for offer in player.offers.values() if offer.eu == max_util]
                    offer = min(max_offers, key=lambda x: abs(player.position - x.offered_position))
                    player.bestOffer = offer
        
        for playerI in self.model.players:
            if playerI.bestOffer : 
                for playerJ in self.model.players:
                    if (playerI.bestOffer.other_actor == playerJ and playerJ.bestOffer != None and playerJ.bestOffer.other_actor == playerI) :
                        playerI.updatePosition(playerI.bestOffer.offered_position)
                        break
                    
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
