'''
Created on 2016 jún. 8

@author: Balázs
'''

from hu.farago.eum3.GroupDecisionModel import Model
from hu.farago.eum3.PlayerCSVReader import PlayerCSVReader

if __name__ == '__main__':

    players = PlayerCSVReader().readDefaultPlayers()
    model = Model(players)
    
    for i in range(200):
        model.run_model()
        for actor in players:
            print(actor)
    
        print('================= END OF ROUND =================')