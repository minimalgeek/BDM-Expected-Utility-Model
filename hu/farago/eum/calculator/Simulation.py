'''
Created on 2016 máj. 18

@author: Balázs
'''

class Simulation():
    
    def __init__(self, params):
        '''
        Constructor
        '''
        
    def perceptualFocalVote(self, position_i, position_j, risk, resources, salience, slope):
        distance_ii = abs(slope * position_i - slope * position_i)
        if distance_ii == 0:
            utility_ii = 1
        else:
            utility_ii = 'echo "1 - (e(risk * l(distance_ii)))" | bc -l'
       
        distance_ij = abs(slope * position_i - slope * position_j)
        if distance_ij == 0:
            utility_ij = 1
        else:
            utility_ij = 'echo "1 - (e(risk * l(distance_ij)))" | bc -l'
       
        intensity_ij = utility_ii - utility_ij
        vote_ij = resources * salience * intensity_ij
        return vote_ij
   
    def perceptualRivalVote(self, position_i, position_j, risk, resources, salience, slope):
        distance_ji = abs(slope * position_j - slope * position_i)
        if distance_ji == 0:
            utility_ji = 1
        else:
            utility_ji = 'echo "1 - (e(risk * l(distance_ji)))" | bc -l'
       
        distance_jj = abs(slope * position_j - slope * position_j)
        if distance_jj == 0:
            utility_jj = 1
        else:
            utility_jj = 'echo "1 - (e(risk * l(distance_jj)))" | bc -l'
       
        intensity_ij = utility_ji - utility_jj
        vote_ij = resources * salience * intensity_ij
        return vote_ij
    
    def perceptualThirdVote(self, position_i, position_j, position_k, risk, resources, salience, slope):
        distance_ki = abs(slope * position_k - slope * position_i)
        if distance_ki == 0:
            utility_ki = 1
        else:
            utility_ki = 'echo "1 - (e(risk * l(distance_ki)))" | bc -l'
       
        distance_kj = abs(slope * position_k - slope * position_j)
        if distance_kj == 0:
            utility_kj = 1
        else:
            utility_kj = 'echo "1 - (e(risk * l(distance_kj)))" | bc -l'
       
        intensity_ij = utility_ki - utility_kj
        vote_ij = resources * salience * intensity_ij
        return vote_ij
    
    def perceptualUtility(self, position_i, position_j, risk, slope):
        distance_ij = abs(slope * position_i - slope * position_j)
        if distance_ij == 0:
            utility_ij = 1
        else:
            utility_ij = 'echo "1 - (e(risk * l(distance_ij)))" | bc -l'
       
        return utility_ij
    
    