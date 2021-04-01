import os, sys
import numpy as np

from src.Direction import Direction
from src.SurroundingPheromone import SurroundingPheromone

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import traceback

# from src.Direction import Direction

# Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
# well as the starting and end coordinates.
class Maze:

    # Constructor of a maze
    # @param walls int array of tiles accessible (1) and non-accessible (0)
    # @param width width of Maze (horizontal)
    # @param length length of Maze (vertical)
    def __init__(self, walls, width, length):
        self.walls = walls
        self.length = length
        self.width = width
        self.start = None
        self.end = None
        self.initialize_pheromones()

        self.pheromones = None

    # Initialize pheromones to a start value.
    def initialize_pheromones(self):
        self.pheromones = np.zeros((len(self.walls), len(self.walls[0])))
        wall = np.copy(self.walls)
        paths = wall > 0
        self.pheromones[paths] = 1.0
        return

    # Reset the maze for a new shortest path problem.
    def reset(self):
        self.initialize_pheromones()

    # Update the pheromones along a certain route according to a certain Q
    # @param r The route of the ants
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_route(self, route, q):
        # Get the list of directions
        r = route.get_route()
        # Get the amount to add by
        amount = 0
        if len(r) > 0:
            amount = q/len(r)

        print(len(r))

        # coordinates start
        coords = route.start

        # trace through the path and update the pheromones by the amount
        for dir in r:
            coords = coords.add_direction(dir)
            # print(coords)
            self.pheromones[coords.get_x(), coords.get_y()] += amount

        return

     # Update pheromones for a list of routes
     # @param routes A list of routes
     # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_routes(self, routes, q):
        for r in routes:
            self.add_pheromone_route(r, q)

    # Evaporate pheromone
    # @param rho evaporation factor
    def evaporate(self, rho):
        self.pheromones *= (1 - rho)
        return

    # Width getter
    # @return width of the maze
    def get_width(self):
        return self.width

    # Length getter
    # @return length of the maze
    def get_length(self):
        return self.length

    # Returns a the amount of pheromones on the neighbouring positions (N/S/E/W).
    # @param position The position to check the neighbours of.
    # @return the pheromones of the neighbouring positions.
    def get_surrounding_pheromone(self, position):
        # initialize pheromones to 0
        north = south = east = west = 0

        # for each direction, check if it is in bounds, if so, get the value in pheromone table
        north_pos = position.add_direction(Direction.north)
        if self.in_bounds(north_pos):
            north = self.pheromones[north_pos.get_x(), north_pos.get_y()]

        east_pos = position.add_direction(Direction.east)
        if self.in_bounds(east_pos):
            east = self.pheromones[east_pos.get_x(), east_pos.get_y()]

        south_pos = position.add_direction(Direction.south)
        if self.in_bounds(south_pos):
            south = self.pheromones[south_pos.get_x(), south_pos.get_y()]

        west_pos = position.add_direction(Direction.west)
        if self.in_bounds(west_pos):
            west = self.pheromones[west_pos.get_x(), west_pos.get_y()]

        sf = SurroundingPheromone(north, east, south, west)
        return sf

    # Pheromone getter for a specific position. If the position is not in bounds returns 0
    # @param pos Position coordinate
    # @return pheromone at point
    def get_pheromone(self, pos):
        return 0

    # Check whether a coordinate lies in the current maze.
    # @param position The position to be checked
    # @return Whether the position is in the current maze
    def in_bounds(self, position):
        return position.x_between(0, self.width) and position.y_between(0, self.length)

    # Representation of Maze as defined by the input file format.
    # @return String representation
    def __str__(self):
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.length)
        string += " \n"
        for y in range(self.length):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    # Method that builds a mze from a file
    # @param filePath Path to the file
    # @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
    @staticmethod
    def create_maze(file_path):
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])
            
            #make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])
            
            for y in range(length):
                line = lines[y+1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Maze(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()