'''
Created on 2016 máj. 12

@author: Balázs
'''
from hu.farago.eum.calculator.dto.Actor import Actor
from typing import Iterable
from hu.farago.eum.calculator.dto.PowerDistribution import PowerDistribution
from hu.farago.eum.calculator.dto.VoterPositionDistance import VoterPositionDistance

class MedianVoterCalculator():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def calculateMedianVoterPosition(self, data: Iterable[Actor]):
        '''
        Calculate Weighted Median Position
        data: list of Actors
        '''
        
        power_distributions = []
        
        for actor in data:
            power = actor.get_resources() * actor.get_salience()
            power_distributions.append(PowerDistribution(actor.get_position(), power))
        
        if (len(power_distributions) > 0):
            power_distributions.sort() # key=lambda x: x.get_position(), reverse=False
        
        unique_power_distributions = set(power_distributions)
        
        cumulative_power = 0
        for unique_position in unique_power_distributions:
            for actor in power_distributions:
                if actor.get_position() == unique_position.get_position():
                    unique_position.add_power(actor.get_power())
            cumulative_power = sum(int(c.get_power()) for c in unique_power_distributions)
            unique_position.set_cumulative_power(cumulative_power)
            
        # now, the cumulative_power is the total sum of power
        distribution_midpoint = cumulative_power / 2
        
        first_position_after_midpoint = None
        for actor in unique_power_distributions:
            if actor.get_cumulative_power() > distribution_midpoint:
                first_position_after_midpoint = actor
        
        actor_before_midpoint = None
        actor_after_midpoint = None
        power_after_midpoint = 0
        for actor in unique_power_distributions:
            if actor.get_cumulative_power() < distribution_midpoint:
                actor_before_midpoint = actor
            if actor.get_cumulative_power() > distribution_midpoint:
                if first_position_after_midpoint.get_position() == actor.get_position():
                    actor_after_midpoint = actor
                    power_after_midpoint += actor.get_power()
                  
        weighted_median_position = 0
        if actor_before_midpoint == None:
            weighted_median_position = unique_power_distributions[0].get_position()
        else :
            if actor_after_midpoint == None:
                weighted_median_position = unique_power_distributions[-1].get_position()
            else:
                weighted_median_position = ((distribution_midpoint - actor_before_midpoint.get_cumulative_power())/actor_after_midpoint.get_power()) \
                    *(actor_after_midpoint.get_position() \
                    -actor_before_midpoint.get_position()) + actor_before_midpoint.get_position()
        
        position_distance = 0
        voter_position_distances = []
        for voter in unique_power_distributions:
            if voter.get_position() < weighted_median_position:
                position_distance = weighted_median_position - voter.get_position()
            else:
                position_distance = voter.get_position() - weighted_median_position
            voter_position_distances.add(VoterPositionDistance(voter.get_position(), position_distance))
        
        smallest_voter = min(voter_position_distances, key=lambda x: x.get_distance())
        
        return smallest_voter.get_position()
    
    def currentMedianVoterPosition(self, data):
        return self.calculateMedianVoterPosition(data)
    
    def worsenedMedianVoterPosition(self, data: Iterable[Actor], focal_data: Actor, rival_data: Actor):
        focal_actor = None
        for actor in data:
            if actor.get_name() == focal_data.get_name():
                focal_actor = actor
                break
        
        focal_actor.set_position(rival_data.get_position())
        return self.calculateMedianVoterPosition(data)