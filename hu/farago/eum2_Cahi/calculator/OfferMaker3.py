'''
Created on 2016 máj. 25

@author: Balázs
'''
from collections import defaultdict
from hu.farago.eum2_Cahi.calculator.Helper import objectListPrint
from hu.farago.eum2_Cahi.calculator.Helper import tablePrint

class Offer(object):
    CONFRONTATION = 'confrontation'
    CONFRONT = 'confrontation+'
    COMPROMISE = 'compromise'
    CAPITULATION = 'capitulation'
    OFFER_TYPES = (
        CONFRONTATION,
        CONFRONT,
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

class OfferMaker(object):

    __players = None
    __expectedCalc = None
    __deltaIJ = []                          # !! probálkozás az xHat matrix létrehozásársa
    __offersIJ = []


    def __init__(self, players, expectedCalc):
        self.__players = players
        self.__expectedCalc = expectedCalc
        
    def makeOffers(self):
        
        length = len(self.__players)
        self.__deltaIJ = [[0 for x in range(length)] for y in range(length)]
        self.__offersIJ = [[0 for x in range(length)] for y in range(length)]
        
        for i, playerI in enumerate(self.__players):
            # calculate where i get offers from
            playerI.offers = []
            
        for i, playerI in enumerate(self.__players):
            # calculate where i get offers from
            for j, playerJ in enumerate(self.__players):
                if i != j and playerI.position != playerJ.position:
                    EIi = self.__expectedCalc.get_expected_utility_ij()[j][i]               #az i ilyennek látja saját győzelmének hasznosságát
                    EIj = self.__expectedCalc.get_expected_utility_ji()[j][i]               #i azt gondolja, hogy ha j győz, akkor ennek j ilyen hasznoságot tulajdonít

                    EJj = self.__expectedCalc.get_expected_utility_ij()[i][j]               #az j ilyennek látja saját győzelmének hasznosságát
                    EJi = self.__expectedCalc.get_expected_utility_ji()[i][j]               #j azt gondolja, hogy ha i győz, akkor ennek i ilyen hasznoságot tulajdonít


                    # 1.) CONFLICT                                                          # Ha mind a két fél azt gondolja, hogy ő az erősebb, akkor confrontáció lesz:
                    if EIi > EIj and EIi > 0 and EJj > EJi and EJj > 0:   

                        if playerI.power() >= playerJ.power():                              # ha I erősebb, akkor az ő pozíciója változatlan marad
                            playerI.offers.append(Offer(playerJ, Offer.CONFRONTATION, playerI.position, EIi))
                            self.__offersIJ[i][j] = playerI.position
                            
                        elif playerI.power() < playerJ.power():                             # ha I gyengébbnek bizonyul, átveszi J pozícióját
                            playerI.offers.append(Offer(playerJ, Offer.CONFRONTATION, playerJ.position, EIi))
                            self.__offersIJ[i][j] = playerJ.position

                    # 2.) COMPROMISE+        
                    elif EIi > EIj and EIi > 0 and EJj < EJi and EJj > 0:
    
                        xHatI = (playerI.position - playerJ.position) * (abs(EIi) / (abs(EIi) + abs(EJj)))
                           
                        playerI.offers.append(Offer(playerJ, Offer.COMPROMISE, playerI.position - xHatI, EIi))           #player I kap kiegyezésre ajánlatot...
                        playerJ.offers.append(Offer(playerJ, Offer.COMPROMISE, playerI.position - xHatI, EIi))           #...ami player j-t, a kompromisszumos ajánlattevőt is köti

                        self.__offersIJ[i][j] = playerI.position - xHatI
                        self.__offersIJ[j][i] = playerI.position - xHatI

                    # 3.) CAPITULATE+   
                    elif EIi > EIj and EIi > 0 and EJj < 0:                                                             #player I kapitulációra kényszeríti J-t 
                        playerJ.offers.append(Offer(playerI, Offer.CAPITULATION, playerI.position, EIi))
                        self.__offersIJ[i][j] = playerJ.position                       

                    # 4.) COMPROMISE-
                    elif EIi < EIj and EIi > 0 and EJj > EJi and EJj > 0:                                               # Ha I azt gondolja, hogy ő az erősebb, J pedig azt, hogy ő a gyengébb:

                        xHatI = (playerI.position - playerJ.position) * (abs(EIi) / (abs(EIi) + abs(EJj)))
            
                        playerI.offers.append(Offer(playerJ, Offer.COMPROMISE, playerI.position - xHatI, EIi))           #player I kap kiegyezésre ajánlatot...
                        playerJ.offers.append(Offer(playerJ, Offer.COMPROMISE, playerI.position - xHatI, EIi))           #...ami player j-t, a kompromisszumos ajánlattevőt is köti

                        self.__offersIJ[i][j] = playerI.position - xHatI
                        self.__offersIJ[j][i] = playerI.position - xHatI

                    # 7.) CAPITULATE-   
                    elif EIi < 0 and EJj > EJi and EJj > 0:                                                  #player J kapitulációra kényszeríti I-t 
                        playerI.offers.append(Offer(playerJ, Offer.CAPITULATION, playerJ.position, EIi))
                        self.__offersIJ[i][j] = playerJ.position 
                         
                        
            print("==== Offers for %s ====" % playerI.name)
            objectListPrint(playerI.offers)



        print("==== offers ====")                                                         # offer mátrix nyomtatási célból
        tablePrint(self.__offersIJ)
        
        for player in self.__players:
            if len(player.offers) > 0:

                # Ha a max EU alapján akarjuk kiválasztani az offereket, ezt kell használni
                #max_util = max([offer.eu for offer in player.offers])                              
                #max_offers = [offer for offer in player.offers if offer.eu == max_util]
                #offer = min(max_offers, key=lambda x: abs(player.position - x.offered_position))
                compromiseOffers = [offer for offer in player.offers if offer.offer_type == Offer.COMPROMISE]
                confrontationOffers = [offer for offer in player.offers if offer.offer_type == Offer.CONFRONT]
                capOffers = [offer for offer in player.offers if offer.offer_type == Offer.CAPITULATION]

                if len(compromiseOffers) > 0:
                    minComp = min(compromiseOffers, key=lambda x: abs(player.position - x.offered_position))
                    player.updatePosition(minComp.offered_position)
                elif len(confrontationOffers) > 0: 
                    minConf = min(confrontationOffers, key=lambda x: abs(player.position - x.offered_position))
                    player.updatePosition(minConf.offered_position)
                elif len(capOffers) > 0:
                    minCap = min(capOffers, key=lambda x: abs(player.position - x.offered_position))
                    player.updatePosition(minCap.offered_position)
                

