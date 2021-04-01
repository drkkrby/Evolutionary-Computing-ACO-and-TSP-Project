import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import random
from src.Route import Route
from src.Direction import Direction
from src.SurroundingPheromone import SurroundingPheromone
from Coordinate import Coordinate

#Class that represents the ants functionality.
class Ant:

    # Constructor for ant taking a Maze and PathSpecification.
    # @param maze Maze the ant will be running in.
    # @param spec The path specification consisting of a start coordinate and an end coordinate.
    def __init__(self, maze, path_specification):
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
        self.rand = random

    # function to check if a point is a dead end
    def dead_end(self, curr_pos, prev_direction):
        if not prev_direction is None:
            surrounding_pheromones = self.maze.get_surrounding_pheromone(curr_pos)
            total = surrounding_pheromones.get_total_surrounding_pheromone()
            pheromone_prev = surrounding_pheromones.get(self.opposite_direction(prev_direction))
            return total - pheromone_prev == 0
        else:
            return False

    # function to get the opposite direction of a direction
    def opposite_direction(self, dir):
        if dir == Direction.north:
            return Direction.south
        elif dir == Direction.south:
            return Direction.north
        elif dir == Direction.east:
            return Direction.west
        elif dir == Direction.west:
            return Direction.east

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self):
        # Add start position to the route
        route = Route(self.start)
        # get the current position
        curr_pos = Coordinate(self.start.get_x(), self.start.get_y())
        # list of coordinates the ant goes through
        coords = [curr_pos]
        # initialize previous_direction variable
        prev_direction = None

        # loop until end position is found
        while not curr_pos.__eq__(self.end):
            # Get the surrounding pheromones of the current position
            surrounding_pheromones = self.maze.get_surrounding_pheromone(curr_pos)
            total = surrounding_pheromones.get_total_surrounding_pheromone()

            # Get the weights of each direction by getting the ratio of the pheromones
            weights = [surrounding_pheromones.get(Direction.north)/total,
                       surrounding_pheromones.get(Direction.south)/total,
                       surrounding_pheromones.get(Direction.east)/total,
                       surrounding_pheromones.get(Direction.west)/total]

            # if the current position isn't a dead end, make the weight of the direction the ant just came from equal
            # to 0 to prevent the ant from going backwards when it's not necessary
            if not self.dead_end(curr_pos, prev_direction):
                if prev_direction == Direction.north:
                    total -= surrounding_pheromones.get(Direction.south)
                    weights = [surrounding_pheromones.get(Direction.north) / total,
                               0,
                               surrounding_pheromones.get(Direction.east) / total,
                               surrounding_pheromones.get(Direction.west) / total]
                elif prev_direction == Direction.south:
                    total -= surrounding_pheromones.get(Direction.north)
                    weights = [0,
                               surrounding_pheromones.get(Direction.south) / total,
                               surrounding_pheromones.get(Direction.east) / total,
                               surrounding_pheromones.get(Direction.west) / total]
                elif prev_direction == Direction.east:
                    total -= surrounding_pheromones.get(Direction.west)
                    weights = [surrounding_pheromones.get(Direction.north) / total,
                               surrounding_pheromones.get(Direction.south) / total,
                               surrounding_pheromones.get(Direction.east) / total,
                               0]
                elif prev_direction == Direction.west:
                    total -= surrounding_pheromones.get(Direction.east)
                    weights = [surrounding_pheromones.get(Direction.north) / total,
                               surrounding_pheromones.get(Direction.south) / total,
                               0,
                               surrounding_pheromones.get(Direction.west) / total]

            # Randomly choose a direction based on the weights of the pheromones
            direction = self.rand.choices([Direction.north, Direction.south, Direction.east, Direction.west], weights, k=1)

            # Update the position and direction
            prev_direction = direction[0]
            curr_pos = curr_pos.add_direction(direction[0])
            # add coordinate to list of coordinates
            coords.append(curr_pos)
            # add direction to route
            route.add(direction[0])

        # Looping and back-tracking elimination: done by going over the route the ant made from teh start and making
        # sure no coordinates are repeated. If there is a repeat, delete all coordinates between the 2 repetitions.

        # create a new route
        final_route = Route(self.start)
        # save the old route
        saved_route = route.get_route()
        # initialize index at 0
        curr_index = 0
        # initialize coordinates
        curr_pos = coords[curr_index]

        # loop until end position is found
        while not curr_pos.__eq__(self.end):
            # start at the end of the list of coordinates to search for repetitions of current position
            for j in range(len(coords)-1, curr_index, -1):
                # if a repetition is found, move to that index
                if curr_pos.__eq__(coords[j]):
                    curr_index = j
                    break

            # add the current route direction to the final_route
            final_route.add(saved_route[curr_index])
            # increment index
            curr_index+=1
            # increment position
            curr_pos = coords[curr_index]

        return final_route

