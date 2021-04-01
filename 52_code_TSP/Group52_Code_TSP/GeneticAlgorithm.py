import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import numpy as np
import random
from src.TSPData import TSPData

# TSP problem solver using genetic algorithms.
class GeneticAlgorithm:

    # Constructs a new 'genetic algorithm' object.
    # @param generations the amount of generations.
    # @param popSize the population size.
    # @param num_points number of points to vist
    # @param num_elite number of chromosomes that make up the elite
    def __init__(self, generations, pop_size, num_points, num_elite):
        self.generations = generations
        self.pop_size = pop_size
        self.best_fit = sys.maxsize
        self.best_path = np.empty(num_points)
        self.num_elite = num_elite

     # Knuth-Yates shuffle, reordering a array randomly
     # @param chromosome array to shuffle.
    def shuffle(self, chromosome):
        n = len(chromosome)
        for i in range(n):
            r = i + int(random.uniform(0, 1) * (n - i))
            swap = chromosome[r]
            chromosome[r] = chromosome[i]
            chromosome[i] = swap
        return chromosome

    # This method should solve the TSP.
    # @param pd the TSP data.
    # @return the optimized product sequence.
    def solve_tsp(self, tsp_data):
        # List out all the points
        bist = list(range(0, len(tsp_data)))

        # Make initial population
        population = np.empty((self.pop_size, len(bist)))
        # Each chromosome is the list of all the points shuffled
        for i in range ((self.pop_size)):
            chromosome = self.shuffle(bist)
            population[i] = chromosome

        count = 0
        # Loop over all the generations
        while count < self.generations:
            count += 1

            # Calculate the fitness for all the chromosomes in the population
            fitness = np.zeros(self.pop_size)
            for (i, p) in enumerate(population):
                fitness[i] = self.fitness(p, tsp_data)

            # Normalize the fitness so that it is a probability of picking a chromosome
            normalized_fitness = self.normalize(fitness)
            #print(normalized_fitness, np.sum(normalized_fitness))

            # Get the elite of the population
            elite_indices = normalized_fitness.argsort()[-self.num_elite:][::-1]
            elite = population[elite_indices]

            # Next generation
            new_population = np.empty((self.pop_size - self.num_elite, len(bist)))
            # Loop to find the next generation that isn't the elite
            for i in range(self.pop_size - self.num_elite):
                # Get index of both parents according to their probabilities
                i1 = self.pick(normalized_fitness) - 1
                i2 = self.pick(normalized_fitness) - 1
                # Get the two parent chromosomes (can be the same chromosome)
                p1 = population[i1]
                p2 = population[i2]
                #print("p1: {} p2: {}".format(p1, p2))

                # Crossover between both parents
                child_cross = self.cross_over(p1, p2)
                #print("After crossover: {}".format(child_cross))

                # Mutation with rate 0.01
                mutation_rate = 0.01
                child = self.mutation(child_cross, mutation_rate)
                #print("After mutation: {}".format(child))

                # Add result to the new population
                new_population[i] = child

            # Population is now new_population concatenated with the elite from the previous gen
            population = np.concatenate((new_population, elite), axis=0)

            print("GENERATION: {}".format(count))
            print("Best path cost: {}, Best path: {}".format(self.best_fit, self.best_path))

        # Return the best path we have found
        return self.best_path

    # Helper to pick an index according to their probabilities
    def pick(self, probabilities):
        # Initialize the index as 0
        i = 0
        # Choose a random number between 0 and 1
        p = random.uniform(0, 1)
        # Remove probabilities at index until p <= 0 and then return that index
        while(p > 0):
            p -= probabilities[i]
            i += 1
        # Return chosen index
        return i

    # Helper to make fitness a probability
    def normalize(self, fitness):
        # Get the sum of all the fitnesses
        sum = np.sum(fitness)
        # Initialize the resulting array
        normalized_fitness = np.empty(len(fitness))
        # For each fitness normalize it and store it in the normalized_fitness array
        for i in range(len(fitness)):
            normalized_fitness[i] = fitness[i]/sum

        # Return the normalized_fitness array
        return normalized_fitness

    # Helper to calculate the fitness of a path
    def fitness(self, chromosome, matrix):
        # Initially distance is 0
        d = 0
        # If there are N points in a path, there are N-1 edges
        for i in range(len(chromosome)-1):
            # Index of first point in weight matrix
            c1 = int(chromosome[i])
            # Index of second point in weight matrix
            c2 = int(chromosome[i+1])
            # Get the weight between these two points and add it to the weight of the path
            d += matrix[c1, c2]

        # If the weight of the path is the best we've seen so far store it along with the path
        if(d < self.best_fit):
            self.best_fit = d
            self.best_path = chromosome

        # Return fitness value according to our fitness function 1/d^3
        return 1/d**2


    # Helper to perform cross over between two chromosomes
    def cross_over(self, c1, c2):
        # Pick the random section to take from c1
        start = random.randint(0, len(c1))
        end = random.randint(start, len(c1))
        #print("start: {} end: {}".format(start, end))
        # Start of the chromosome is the slice from c1
        new_chromosome = c1[start:end]
        #print("split: {}".format(new_chromosome))
        index = 0
        leftovers = np.empty(len(c1)-len(new_chromosome))
        # Make an array of the points not in the slice
        for c in c2:
            if(c not in new_chromosome):
                leftovers[index] = c
                index += 1
        # Concatenate the slice and the leftovers
        bromosome = np.concatenate((new_chromosome, leftovers), axis=0)
        #print("leftovers: {}".format(leftovers))
        #print("final new chromosome: {}".format(bromosome))
        # Return resulting path
        return bromosome

    # Helper to perform mutation on a chromosome
    def mutation(self, chromosome, mutation_rate):
        # For each of the points(genes) there is a chance of mutation
        for n in range(len(chromosome)):
            i = random.uniform(0,1)
            # Mutate with a certain probability
            if(i < mutation_rate):
                # First random point to swap
                rand_index = random.randint(0, len(chromosome)-1)
                #next_index = (rand_index + 1) % len(chromosome) # Mutation where only neighbours switch
                next_index = random.randint(0, len(chromosome) -1) # If we don't just want to swap neighbours
                # Swap the two points
                self.swap(chromosome, rand_index, next_index)
        # Return chromosome after being mutated
        return chromosome

    # Helper to swap two elements in an array
    def swap(self, chromosome, indexA, indexB):
        temp = chromosome[indexA]
        chromosome[indexA] = chromosome[indexB]
        chromosome[indexB] = temp
        return chromosome

# Assignment 2.b
if __name__ == "__main__":
    #parameters
    population_size = 1000
    generations = 100
    #num_points = 18
    elite_percentage = 0.01
    elite_number = int(elite_percentage * population_size)
    #persistFile = "./../data/productMatrixDist_1"
    #persistFile = "./../data/productMatrixDist_2"
    persistFile = "./../data/productMatrixDist_3"
        
    #setup optimization
    tsp_data = TSPData.read_from_file(persistFile)
    #print(tsp_data.distances)
    bsp = np.array(tsp_data.distances)
    # formatting the way numpy prints tables
    large_width = 400
    np.set_printoptions(linewidth=large_width)

    print(bsp)
    num_points = len(bsp)
    #tsp_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17]
    ga = GeneticAlgorithm(generations, population_size, num_points, elite_number)

    #run optimzation and write to file
    #solution = ga.solve_tsp(tsp_data)
    solution = ga.solve_tsp(bsp)
    bolution = [round(solution) for solution in solution]
    print(bolution)
    tsp_data.write_action_file(bolution, "./../data/TSP solution.txt")