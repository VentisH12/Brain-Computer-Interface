# Author: Anand Cheruvu
# Version: 1.5

# The workspace W is an open half-plane bounded by the line L, which represents the 
# surface of the skull.
# Assumptions: The line L is a straight line on the x-axis.
#	       The workspace W is the upper half-plane above L (y ≥ 0).


import numpy as np
from scipy.optimize import minimize

# Define the workspace W and line L. Contains the method to calculate the
# Euclidean distance between a point in W and a Sensor on line L.

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, sensor):
        return np.sqrt((self.x - sensor.x) ** 2 + (self.y - sensor.y) ** 2)

# Function to compute the reciprocal sum of distances. Calculates the sum 
# of the reciprocals of the distances from each point in the neural 
# ensemble P to a set of sensors S on the line L

def reciprocal_sum_of_distances(P, S):
    reciprocal_sums = []
    for s in S:
        total_reciprocal_sum = 0
        for p in P:
            total_reciprocal_sum += 1 / p.distance(s)
        reciprocal_sums.append(total_reciprocal_sum)
    return np.array(reciprocal_sums)

# Objective function for optimization using the minimize function from 
# scipy.optimize to find the optimal senor locations on the link L. It 
# calculates the penalty based on the difference between the reciprocal 
# sums of distances for different sensors. Minimizing this penalty ensures 
# that the reciprocal sums are as unique as possible.

def objective(S_params, P):
    # Convert flat array into sensor points on line L
    S = [Point(x, 0) for x in S_params]  # Sensors are on line L (y=0)
    
    # Compute reciprocal sum of distances
    rec_sums = reciprocal_sum_of_distances(P, S)
    
    # Minimize the difference in reciprocal sums to force uniqueness
    minimize_penalty = np.sum(np.diff(rec_sums)**2)
    
    return minimize_penalty

# Define the neural ensemble points P in the workspace. Some example points

P = [Point(1, 4), Point(2, 5), Point(8, 9)] 
 
# Initial guess for sensor locations on line L
initial_guess = [2.0, 7.0, 9.0]  # Example initial guesses for sensor positions on L

# Perform optimization to determine optimal sensor locations
result = minimize(objective, initial_guess, args=(P,), method='L-BFGS-B')

# Optimized sensor positions
optimal_sensor_positions = result.x
S_optimized = [Point(x, 0) for x in optimal_sensor_positions]

# Print results. After optimization, print out the optimized sensor 
# positions on the line L.
print("Optimized Sensor Positions on Line L:")
for i, sensor in enumerate(S_optimized):
    print(f"Sensor {i+1}: (x={sensor.x}, y={sensor.y})")
