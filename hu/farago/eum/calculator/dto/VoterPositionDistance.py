'''
Created on 2016 máj. 17

@author: Balázs
'''

class VoterPositionDistance():
    
    __position = 0
    __distance = 0
    
    def __init__(self, position, distance):
        self.__position = position
        self.__distance = distance

    def get_position(self):
        return self.__position


    def get_distance(self):
        return self.__distance


    def set_position(self, value):
        self.__position = value


    def set_distance(self, value):
        self.__distance = value


    def del_position(self):
        del self.__position


    def del_distance(self):
        del self.__distance

    position = property(get_position, set_position, del_position, "position's docstring")
    distance = property(get_distance, set_distance, del_distance, "distance's docstring")
        
    