'''
Created on 2016 máj. 19

@author: Balázs
'''

import csv
from hu.farago.eum2_Cahi.dto.Player import Player
from hu import APP_RESOURCES

class PlayerCSVReader():
    '''
    classdocs
    '''
    #__defaultFileName = 'oil_price.csv'
    __defaultFileName = 'countries.csv'
    #__defaultFileName = 'countries_test.csv'

    def __init__(self):
        '''
        Constructor
        '''
    
    def readPlayers(self, fileName):
        print('Reading from: ', fileName)
        players = []
        with open(fileName) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                player = Player(row['name'], row['capability'], row['position'], row['salience'])
                players.append(player)
        return players
    
    def readDefaultPlayers(self):
        return self.readPlayers(APP_RESOURCES + PlayerCSVReader.__defaultFileName);
