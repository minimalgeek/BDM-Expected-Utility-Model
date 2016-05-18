'''
Created on 2016 máj. 12

@author: Balázs
'''

class PowerDistribution():
    '''
    Power distribution
    '''

    _position = 0
    _power = 0
    _cumulative_power = 0

    def __init__(self, position, power):
        '''
        Constructor
        '''
        self._position = position
        self._power = power
        
    def add_power(self, power):
        self._power += power

    def get_cumulative_power(self):
        return self.__cumulative_power


    def set_cumulative_power(self, value):
        self.__cumulative_power = value


    def del_cumulative_power(self):
        del self.__cumulative_power


    def __lt__(self, other):
        return self._position < other._position
    
    def __eq__(self, other):
        return self._position == other._position

    def get_position(self):
        return self.__position


    def get_power(self):
        return self.__power


    def set_position(self, value):
        self.__position = value


    def set_power(self, value):
        self.__power = value


    def del_position(self):
        del self.__position


    def del_power(self):
        del self.__power

    position = property(get_position, set_position, del_position, "position's docstring")
    power = property(get_power, set_power, del_power, "power's docstring")
    cumulative_power = property(get_cumulative_power, set_cumulative_power, del_cumulative_power, "cumulative_power's docstring")
        
    