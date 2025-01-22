""" General Options for GA """
"""
    For parent selection : Roulette Wheel Selection
    For crossover : Blend Crossover
    For mutation : Random Value Addition Mutation

    Goal is to find the maximum value of the given function:
        f(x) = -(x^2) + 2x

        Expected solution for x = 1
        Expected maximum value of f(x) = 1
"""

# Import necessary libraries
import random
import numpy as np

class Individual:
    """
    A class to represent each individual.
    """
    def __init__(self, value: float):
        self.value = value

class GA:
    """
    A class to apply the genetic algorithm.
    """
    def __init__(self, objective_function, num_indvs: int, crossover_rate: int, mutation_rate: int):
        self.objective_function = objective_function
        self.num_indvs = num_indvs
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def initialize_generation(self) -> list[Individual]:
        """
        A function to initialize the generation.
        """
        generation = []
        for _ in range(self.num_indvs):
            random_value = random.uniform(0, 2)
            generation.append(Individual(random_value)) 
        
        return generation
    
    def calculate_fitness(self, generation: list[Individual]) -> list[float]:
        """
        A function to calculate the fitness value of each individual
        """
        fitness_values = []
        for individual in generation:
            fitness_values.append(self.objective_function(individual.value))

        min_fitness = min(fitness_values)
        if min_fitness <= 0:
            fitness_values = [fitness + abs(min_fitness) + 1e-6 for fitness in fitness_values]
        
        return fitness_values
    
    def roulette_wheel_selection(self, generation: list[Individual], fitness_values: list[float]) -> list[Individual]:
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
    
    def blend_crossover(self, selected_parents: list[Individual]) -> list[Individual]:
        """
        A function to apply blend crossover to the selected parents.
        """
        alpha = 0.5
        childrens = []
        for i in range(0, len(selected_parents) - 1, 2):
            child1_value, child2_value, parent1_value, parent2_value = 0, 0, 0, 0
            random_number = random.random()
            if random_number < self.crossover_rate:
                parent1_value = selected_parents[i].value
                parent2_value = selected_parents[i + 1].value

                child1_value = parent1_value + alpha * (parent2_value - parent1_value) * random.uniform(-1, 1)
                child2_value = parent2_value + alpha * (parent1_value - parent2_value) * random.uniform(-1, 1)
            else:
                child1_value = parent1_value
                child2_value = parent2_value

            childrens.extend([Individual(child1_value), Individual(child2_value)])

        return childrens
    
    def random_value_addition_mutation(self, childrens: list[Individual]) -> list[Individual]:
        """
        A function to apply random value addition mutation to the children.
        """
        for children in childrens:
            random_value = random.random()
            if random_value < self.mutation_rate:
                mutation_value = random.uniform(-1, 1)
                children.value += mutation_value
            
        return childrens

def objective_function(x):
    """
    The objective function.
    """
    return -(x ** 2) + 2 * x

""" Initially """
# Set the global variables
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.05
NUM_INDIVIDUALS = 6
NUM_LOOPS = 1000

# Create an instance of GA to apply genetic algorithm to objective function
ga = GA(objective_function, NUM_INDIVIDUALS, CROSSOVER_RATE, MUTATION_RATE)

# Create the initial generation
generation = ga.initialize_generation()

""" Iteration """
for epoch in range(NUM_LOOPS):
    # Calculate fitness values for each individual
    fitness_values = ga.calculate_fitness(generation)

    # Select parents using roulette wheel selection
    selected_parents = ga.roulette_wheel_selection(generation, fitness_values)

    # Get the children using blend crossover
    children = ga.blend_crossover(selected_parents)

    # Apply mutation using random value addition mutation
    children = ga.random_value_addition_mutation(children)

    # Set the new generation
    generation = children

""" Finally """
print(f"The best solution found after {NUM_LOOPS} iterations is : \n{generation[np.argmax(fitness_values)].value}")
print(f"The best value obtained after {NUM_LOOPS} iterations is : \n{objective_function(generation[np.argmax(fitness_values)].value)}")