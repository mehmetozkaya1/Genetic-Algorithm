""" General Options for GA """
"""
    For parent selection : Roulette Wheel Selection
    For crossover : Single Point Crossover
    For mutation : Bit Flip Mutation

    Goal is to find the maximum value with the given bags:

    Maximum bag capacity is 15.

        BAG NAME - VALUE - WEIGHT
    1-     1         10      2
    2-     2         5       3  
    3-     3         15      5
    4-     4         7       7
    5-     5         6       1
    6-     6         18      4
    7-     7         3       1
"""

# Import necessary libraries
import random
import numpy as np

bag_values_weights = [
    {"value": 10, "weight": 2},
    {"value": 5, "weight": 3},
    {"value": 15, "weight": 5},
    {"value": 7, "weight": 7},
    {"value": 6, "weight": 1},
    {"value": 18, "weight": 4},
    {"value": 3, "weight": 1},
]

class Bag:
    """
    A class to represent each individual.
    """
    def __init__(self, value: int, weight: int):
        self.value = value
        self.weight = weight

bags_list = []
for bag_dict in bag_values_weights:
    bag_value = bag_dict["value"]
    bag_weight = bag_dict["weight"]
    bags_list.append(Bag(bag_value, bag_weight))

class GA:
    """
    A class to apply the genetic algorithm.
    """
    def __init__(self, weight_limit: int, num_indvs: int, crossover_rate: int, mutation_rate: int, crossover_single_point: int):
        self.weight_limit = weight_limit
        self.num_indvs = num_indvs
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.crossover_single_point = crossover_single_point

    def initialize_generation(self) -> list[Bag]:
        """
        A function to initialize the generation.
        """
        generation = []
        for _ in range(self.num_indvs):
            individual = []
            for i in range(len(bag_values_weights)):
                individual.append(random.choice([0, 1]))
            generation.append(individual)
        
        return generation
    
    def calculate_fitness(self, generation: list[list]) -> list[float]:
        """
        A function to calculate the fitness value of each individual
        """
        fitness_values = []
        for individual in generation:
            total_weight = 0
            fitness_value = 0 
            for idx, is_added in enumerate(individual):
                if is_added == 1:
                    total_weight += bags_list[idx].weight
                    fitness_value += bags_list[idx].value
            
            if total_weight > self.weight_limit:
                fitness_value *= 0.5
            
            fitness_values.append(fitness_value)

        return fitness_values
    
    def roulette_wheel_selection(self, generation: list[list], fitness_values: list[int]) -> list[list]:
        """
        A function to apply roulette wheel selection.
        """
        probs = []
        total_fitness = sum(fitness_values)

        if total_fitness == 0:
            total_fitness = min(fitness_values)

        for idx, individual in enumerate(generation):
            prob = fitness_values[idx] / total_fitness
            probs.append(prob)

        cum_probs = []
        for i, prob in enumerate(probs):
            prob_sum = 0
            for j in range(i + 1):
                prob_sum += probs[j]
            cum_probs.append(prob_sum)

        selected_parents_indexes = []
        for i in range(self.num_indvs):
            random_number = random.random()
            for idx in range(len(cum_probs) - 1):
                if random_number <= cum_probs[0]:
                    selected_parents_indexes.append(0)
                    break
                elif random_number > cum_probs[idx] and random_number < cum_probs[idx + 1]:
                    selected_parents_indexes.append(idx + 1)
                    break
        selected_parents = [generation[idx] for idx in selected_parents_indexes]

        return selected_parents
    
    def single_point_crossover(self, selected_parents: list[list], random_point: bool = False) -> list[list]:
        """
        A function to apply blend crossover to the selected parents.
        """
        if random_point:
            point = random.randint(1, len(selected_parents[0]) - 1)
        else:
            point = self.crossover_single_point

        if point < 0 or point > len(selected_parents):
            print(f"Given parameter 'point' should be in between 0 and {len(selected_parents) - 1}")
            raise ValueError
        
        childrens = []
        for i in range(0, len(selected_parents) - 1, 2):
            random_number = random.random()
            parent_1 = selected_parents[i]
            parent_2 = selected_parents[i + 1]

            if random_number <= self.crossover_rate:
                parent_1_first, parent_1_last = parent_1[: point], parent_1[point:]
                parent_2_first, parent_2_last = parent_2[: point], parent_2[point:]

                child_1 = parent_1_first + parent_2_last
                child_2 = parent_2_first + parent_1_last
            else:
                child_1 = parent_1
                child_2 = parent_2

            childrens.extend([child_1, child_2])

        return childrens            
    
    def bit_flip_mutation(self, childrens: list[list]) -> list[list]:
        """
        A function to apply random value addition mutation to the children.
        """
        for children in childrens:
            for idx, bit in enumerate(children):
                random_number = random.random()
                if random_number < self.mutation_rate:
                    children[idx] = 1 if bit == 0 else 0

        return childrens

""" Initially """
# Set the global variables
WEIGHT_LIMIT = 15
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1
NUM_INDIVIDUALS = 50
CROSSOVER_SINGLE_POINT = 3
NUM_LOOPS = 1000

# Create an instance of GA to apply genetic algorithm to objective function
ga = GA(WEIGHT_LIMIT, NUM_INDIVIDUALS, CROSSOVER_RATE, MUTATION_RATE, CROSSOVER_SINGLE_POINT)

# Create the initial generation
generation = ga.initialize_generation()

""" Iteration """
for epoch in range(NUM_LOOPS):
    # Calculate fitness values for each individual
    fitness_values = ga.calculate_fitness(generation)

    # Select parents using roulette wheel selection
    selected_parents = ga.roulette_wheel_selection(generation, fitness_values)

    # Get the children using blend crossover
    children = ga.single_point_crossover(selected_parents, True)

    # Apply mutation using random value addition mutation
    children = ga.bit_flip_mutation(children)

    # Set the new generation
    generation = children

""" Finally """
print(f"The best solution found after {NUM_LOOPS} iterations is : \n{generation[np.argmax(fitness_values)]}")
print(f"The best value obtained after {NUM_LOOPS} iterations is : \n{max(fitness_values)}")