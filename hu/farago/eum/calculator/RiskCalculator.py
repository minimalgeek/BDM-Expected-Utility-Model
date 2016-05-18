'''
Created on 2016 máj. 17

@author: Balázs
'''
from hu.farago.eum.calculator.MedianVoterCalculator import MedianVoterCalculator

class RiskCalculator():
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def nonperceptualFocalVote(self, position_i, position_j, resources, salience, slope):
        utility_ii = 1 - abs(slope * position_i - slope * position_i)
        utility_ij = 1 - abs(slope * position_i - slope * position_j)
        return resources*salience*(utility_ii - utility_ij)
    
    def nonperceptualRivalVote(self, position_i, position_j, resources, salience, slope):
        utility_ji = 1 - abs(slope * position_j - slope * position_i)
        utility_jj = 1 - abs(slope * position_j - slope * position_j)
        return resources*salience*(utility_ji - utility_jj)
    
    def nonperceptualThirdVote(self, position_i, position_j, position_k, resources, salience, slope):
        utility_ki = 1 - abs(slope * position_k - slope * position_i)
        utility_kj = 1 - abs(slope * position_k - slope * position_j)
        return resources*salience*(utility_ki - utility_kj)
    
    def calculateRisk(self, data, hypothetical_precision, utility_interval):
        min_position = min(data, key=lambda x: x.get_position())
        max_position = max(data, key=lambda x: x.get_position())
        
        games = [[0 for i in range(len(data))] for j in range(len(data))]

        for i, rival_actor in data:
            for j, focal_actor in data:
                if focal_actor.get_name() != rival_actor.get_name():
                    games[i][j] = [data[i], data[j]]
                    for k, third_actor in data:
                        if third_actor.get_name() != rival_actor.get_name() and third_actor.get_name() != focal_actor.get_name():
                            games[i][j].append(data[k])
        
        security_index = -1
        expected_utility = 0
        security, data_security_profiles = [], []
        for rival_game in games:
            security_index += 1
            for hypothetical_position in range(min_position, max_position):
                for game in rival_game:
                    actual_position = game[1].get_position()
                    game[1].set_position(hypothetical_position)
                    
                    current_positions = []
                    for actor in game:
                        current_positions.append(actor.get_position())
                    
                    slope = 0
                    if utility_interval == "zero_one":
                        slope = 1 / (max_position - min_position)
                    if utility_interval == "negative_one_one":
                        slope = 2 / (max_position - min_position)
                    
                    votes = []
                    for index in range(len(game)):
                        if index == 0:
                            votes.append(self.nonperceptualFocalVote(
                                game[0].get_position(), 
                                game[1].get_position(), 
                                game[0].get_resources(), 
                                game[0].get_salience(), 
                                slope))
                        if index == 1:
                            votes.append(self.nonperceptualRivalVote(
                                game[0].get_position(),
                                game[1].get_position(),
                                game[1].get_resources(),
                                game[1].get_salience(),
                                slope))
                        if index > 1:
                            votes.append(self.nonperceptualThirdVote(
                                game[0].get_position(),
                                game[1].get_position(),
                                game[index].get_position(), 
                                game[index].get_resources(), 
                                game[index].get_salience(), 
                                slope))
    
                    probability_resistance = game[1].get_salience()
                    probability_no_resistance = 1 - probability_resistance
    
                    absolute_vote_sum = 0
                    vote_sum = 0
                    for vote in votes:
                        absolute_vote_sum += abs(vote)
                        if vote > 0:
                            vote_sum += vote

                    probability_winning, probability_losing = 0,0
                    if absolute_vote_sum != 0: 
                        probability_winning = vote_sum / absolute_vote_sum
                        probability_losing = 1 - probability_winning
                    
                    utility_ij = 1 - abs(slope * game[0].get_position() - slope * game[1].get_position())
                    utility_success = 1 - utility_ij
                    utility_failure = utility_ij - 1
    
                    expected_utility_winning = probability_winning * utility_success
                    expected_utility_losing = probability_losing * utility_failure
                    expected_utility_resistance = probability_resistance * (expected_utility_winning + expected_utility_losing)
    
                    expected_utility_no_resistance = probability_no_resistance * utility_success
                    expected_utility_challenging = expected_utility_resistance + expected_utility_no_resistance
    
                    probability_sq_remaining = 0.5
                    probability_sq_changing = 1 - probability_sq_remaining
                    probability_sq_improving = 0.5
                    probability_sq_worsening = 1 - probability_sq_improving
    
                    calc = MedianVoterCalculator()
                    current_median_voter_position = calc.currentMedianVoterPosition(game)
                    worsened_median_voter_position = calc.worsenedMedianVoterPosition(game, game[0], game[1])
                        
                    utility_im_current  = 1 - abs(slope * game[0].get_position() - slope * current_median_voter_position)
                    utility_im_worsened = 1 - abs(slope * game[0].get_position() - slope * worsened_median_voter_position)
                    utility_im_improved = utility_im_worsened
                    utility_sq_remaining = 0
                    utility_sq_improving = utility_im_improved - utility_im_current
                    utility_sq_worsening = utility_im_worsened - utility_im_current
    
                    expected_utility_sq_improving = probability_sq_improving * utility_sq_improving
                    expected_utility_sq_worsening = probability_sq_worsening * utility_sq_worsening
                    expected_utility_sq_changing = probability_sq_changing * (expected_utility_sq_improving + expected_utility_sq_worsening)
                    expected_utility_sq_remaining = probability_sq_remaining * utility_sq_remaining
                    expected_utility_not_challenging = expected_utility_sq_changing + expected_utility_sq_remaining
    
                    expected_utility += expected_utility_challenging - expected_utility_not_challenging
                    
                    name = game[1].get_name()
                    resources = game[1].get_resources()
                    salience = game[1].get_salience()
                security.append({"position" : game[1]['position'], "expected utility" : expected_utility})
                data_security_profiles.append({
                    "name" : name, 
                    "resources" : resources, 
                    "salience" : salience, 
                    "position" : actual_position, 
                    "security" : security})
                expected_utility = 0
            actual_position = None
            security = None
    
        security_profile, computed_data = [], []
        for actor in data_security_profiles:
            
            for security in actor['security']:
                security_profile.append(security['expected utility'])
                if security['position'] == actor['position']:
                    current_security = security['expected utility']
                    
            max_security = max(security_profile)
            min_security = min(security_profile)
            raw_risk = ((2 * current_security - max_security) - min_security) / (max_security - min_security)
            risk = (1 - raw_risk / 3) / (1 + raw_risk / 3)
            computed_data.append({
                "name" : actor['name'], 
                "resources" : actor['resources'], 
                "salience" : actor['salience'], 
                "position" : actor['position'], 
                "risk" : risk})
            security_profile = None
        return computed_data