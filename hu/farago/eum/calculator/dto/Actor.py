'''
Created on 2016 máj. 12

@author: Balázs
'''

class Actor():
    '''
    Actor
    '''
    
    _name = None
    _risk = None
    _resources = None
    _salience = None
    _position = None

    def __init__(self, resources, salience, position, risk, name):
        '''
        Constructor
        '''
        self._resources = resources
        self._salience = salience
        self._position = position
        self._risk = risk
        self._name = name

    def get_name(self):
        return self.__name


    def set_name(self, value):
        self.__name = value


    def del_name(self):
        del self.__name


    def get_risk(self):
        return self.__risk


    def set_risk(self, value):
        self.__risk = value


    def del_risk(self):
        del self.__risk


    def get_position(self):
        return self.__position


    def set_position(self, value):
        self.__position = value


    def get_resources(self):
        return self.__resources


    def get_salience(self):
        return self.__salience


    def set_resources(self, value):
        self.__resources = value


    def set_salience(self, value):
        self.__salience = value


    def del_resources(self):
        del self.__resources


    def del_salience(self):
        del self.__salience
        
    def del_position(self):
        del self.__position

    resources = property(get_resources, set_resources, del_resources, "resources's docstring")
    salience = property(get_salience, set_salience, del_salience, "salience's docstring")
    position = property(get_position, set_position, del_position, "position's docstring")
    risk = property(get_risk, set_risk, del_risk, "risk's docstring")
    name = property(get_name, set_name, del_name, "name's docstring")
    
    