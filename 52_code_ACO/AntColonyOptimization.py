import copy
import os, sys

import numpy as np

from src.Ant import Ant

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
from src.Maze import Maze
from src.PathSpecification import PathSpecification
from src.Coordinate import Coordinate
from src.Route import Route

# Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
# path specification.
class AntColonyOptimization:

    # Constructs a new optimization object using ants.
    # @param maze the maze .
    # @param antsPerGen the amount of ants per generation.
    # @param generations the amount of generations.
    # @param Q normalization factor for the amount of dropped pheromone
    # @param evaporation the evaporation factor.
    def __init__(self, maze, ants_per_gen, generations, q, evaporation):
        self.maze = maze
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.evaporation = evaporation
        self.shortest_distance = sys.maxsize
        self.best_route = None

     # Loop that starts the shortest path process
     # @param spec Spefication of the route we wish to optimize
     # @return ACO optimized route
    def find_shortest_route(self, path_specification):
        self.maze.reset()

        self.best_route = None
        self.shortest_distance = sys.maxsize

        # list of routes for each generation
        routes = []

        # formatting the way numpy prints tables
        large_width = 400
        np.set_printoptions(linewidth=large_width)

        # loop for a certain number of generations
        for gen in range(self.generations):
            print("GENERATION: ", gen)

            # list of ants
            ants = []
            routes = []

            # add ants to the list
            for i in range(self.ants_per_gen):
                ants.append(Ant(self.maze, path_specification))

            # make each ant search for the finish
            for i in range(self.ants_per_gen):
                r = ants[i].find_route()
                print("done ant: ", i)
                routes.append(r)
                if r.size() < self.shortest_distance:
                    self.shortest_distance = r.size()
                    self.best_route = r

            # evaporate pheromones in the maze
            self.maze.evaporate(self.evaporation)
            # update pheromones based on the routes of the ants
            self.maze.add_pheromone_routes(routes, self.q)

        print("Shortest length: ", self.shortest_distance)
        return self.best_route

# Driver function for Assignment 1
if __name__ == "__main__":
    #parameters
    ants_per_gen = 5
    no_gen = 10
    q = 100
    evap = 0.1

    #construct the optimization objects
    maze = Maze.create_maze("./../data/hard maze.txt")
    spec = PathSpecification.read_coordinates("./../data/hard coordinates.txt")
    aco = AntColonyOptimization(maze, ants_per_gen, no_gen, q, evap)

    #save starting time
    start_time = int(round(time.time() * 1000))

    #run optimization
    shortest_route = aco.find_shortest_route(spec)

    #print time taken
    print("Time taken: " + str((int(round(time.time() * 1000)) - start_time) / 1000.0))

    #save solutiond
    shortest_route.write_to_file("./../data/test_solution.txt")

    #print route size
    print("Route size: " + str(shortest_route.size()))