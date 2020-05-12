import math
import random


def vertex_distance(vertex1, vertex2):
    dx = vertex1.x - vertex2.x
    dy = vertex1.y - vertex2.y
    return math.sqrt(dx ** 2 + dy ** 2)


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


# Inspired by and partially adapted from: https://www.youtube.com/watch?v=7WcmyxyFO7o
class PoissonGenerator:
    def __init__(self, size_x: int, size_y: int, vertex_radius: float, spawn_tries: int = 4):
        # Number of tries before a spawn point is removed from the spawn_points list
        self.spawn_tries = spawn_tries
        # General size variables
        self.size_x = size_x            # Size of the graph in the x-dimension
        self.size_y = size_y            # Size of the graph in the y-dimension
        self.vertex_radius = vertex_radius  # This is the exclusion radius of a point within this graph. This is the
        # radius of the circle drawn around each point in which the CENTER of another point cannot reside. The
        # exclusion circles for point will overlap, but 1/2 the exclusion radius yields circles that should NEVER
        # overlap.

        # Grid size variables
        self.cell_size = vertex_radius / math.sqrt(2)             # The cell size for the backing grid
        self.num_rows = math.ceil(size_x / self.cell_size)      # The number of rows in the backing grid
        self.column_size = math.ceil(size_y / self.cell_size)   # The number of elements in each column of the grid

        # The grid for smart distance checking
        self.grid = [[0 for _ in range(self.column_size)] for _ in range(self.num_rows)]    # Use "_" for unused var
        # The grid contains all 0's by default, which indicates nothing is there. To indicate a vertex exists on the
        # grid, we add the index of the vertex within points_vector PLUS 1. Keep this in mind when indexing based on
        # values found in the grid.
        # This generates all 0's, and "[[0] * 10] * 10" will yield a list of ten references to the same list of 10 zeros

        # Flags
        self.seeded = False     # Check to see if the board has been seeded.

        # Lists for tracking generated points and available spawn points
        self.points_vector = []     # List of (x, y) coordinate tuples
        self.spawn_points = []      # List of indices within points_vector where viable spawn points live

    # Generate a point based on the Poisson Disc algorithm. Returns a boolean indicating success.
    def generate_point(self):
        # If the points_vector list is empty, the board has not been seeded yet.
        if not self.points_vector:
            # Add (x, y) tuple within the middle third to points_vector
            start_x = random.randint(int(self.size_x / 3), int(2 * self.size_x / 3))
            start_y = random.randint(int(self.size_y / 3), int(2 * self.size_y / 3))
            self.points_vector.append((start_x, start_y))
            # Index 0 of points_vector is a viable spawn point
            self.spawn_points.append(0)
            # Place a marker in the grid for the seeded point
            grid_x_pos = int(self.points_vector[0][0] / self.cell_size)  # Grid x-location of the generated point
            grid_y_pos = int(self.points_vector[0][1] / self.cell_size)  # Grid x-location of the generated point
            self.grid[grid_x_pos][grid_y_pos] = 1
            self.seeded = True
            return True

        # If there are no available spawn points, the generator cannot generate more points
        if not self.spawn_points:
            return False

        selected_spawn_point = random.randint(0, len(self.spawn_points) - 1)    # This is the index in spawn_points
        # that will point to an index in the points vector that we will use to try and generate a new point on the
        # graph

        # We will try to find a valid point as many times as we choose, then if no good point was found, remove that
        # point from spawn_points
        for it in range(self.spawn_tries):
            # Generate new point first in polar coordinates, then convert to rectangular
            radius = self.vertex_radius * (1 + math.sqrt(random.random()))    # Distance in polar coordinates. This is
            # specifically written to generate numbers that are evenly distributed through the area of the circle
            # drawn, not along the radius, as that would lead to a larger density at the center of the field. Read
            # more here: http://www.anderswallin.net/2009/05/uniform-random-points-in-a-circle-using-polar-coordinates/
            theta = 2 * math.pi * random.random()                           # Angle in polar coordinates
            x_guess = self.points_vector[self.spawn_points[selected_spawn_point]][0] + round(radius * math.cos(theta))
            y_guess = self.points_vector[self.spawn_points[selected_spawn_point]][1] + round(radius * math.sin(theta))

            # Fail to generate if the point lies outside the limits of the graph
            if x_guess < 0 or x_guess > self.size_x or y_guess < 0 or y_guess > self.size_y:
                continue

            grid_x_pos = int(x_guess / self.cell_size)  # Grid x-location of the generated point
            grid_y_pos = int(y_guess / self.cell_size)  # Grid x-location of the generated point

            # Fail to generate if the grid already contains a point at the same grid location as the new point
            if bool(self.grid[grid_x_pos][grid_y_pos]):
                continue

            distance = 2 * self.vertex_radius     # A distance that is by default acceptable

            # Loop through the local x-range of the gird
            for x_it in range(grid_x_pos - 2, grid_x_pos + 3):  # Runs 5 times
                # Check if outside the x-bounds of the grid
                if x_it < 0 or x_it > len(self.grid) - 1:
                    continue

                # loop through the local y-range of the grid
                for y_it in range(grid_y_pos - 2, grid_y_pos + 3):  # Runs 5 times
                    # Check if outside the y-bounds of the grid
                    if y_it < 0 or y_it > len(self.grid[x_it]) - 1:
                        continue

                    # modify the distance to be the distance from the point guess to the point in this grid square
                    if self.grid[x_it][y_it]:   # returns True if the value is > 0, i.e. there is a point
                        dx = x_guess - self.points_vector[self.grid[x_it][y_it] - 1][0]
                        dy = y_guess - self.points_vector[self.grid[x_it][y_it] - 1][1]
                        distance = math.sqrt(dx ** 2 + dy ** 2)

                    # If the point is no good, we break out of both loops and throw out the guess
                    if distance < self.vertex_radius:
                        break

                # If the point is no good, we break out of both loops and throw out the guess
                if distance < self.vertex_radius:
                    break

            # If after checking all local grid squares and no points were found that exclude the point from existing...
            if distance > self.vertex_radius:
                # Add the point to the points_vector
                self.points_vector.append((x_guess, y_guess))
                # Add the point as a new available spawn point
                self.spawn_points.append(len(self.points_vector) - 1)
                # Add the point index within points_vector to the grid.
                self.grid[grid_x_pos][grid_y_pos] = len(self.points_vector)     # Don't add one, size already increased
                return True

        # If no point was created after all those tries, remove that spawn point from the list
        self.spawn_points.remove(self.spawn_points[selected_spawn_point])
        return False

    # Generate an additional point and return the (x, y) tuple
    def get_next_point(self):
        # If the board has not been seeded, the first point must be generated
        if not self.seeded:
            self.generate_point()

        while not self.finished():
            # Attempt to generate another point. If this returns false, no point was generated and the generator is
            # finished
            if self.generate_point():
                # If there are still more potential points to be generated, the element BEFORE the last should be
                # returned
                return self.points_vector[len(self.points_vector) - 2]
        # If the generator is finished, the last element in the array should be returned
        return self.points_vector[len(self.points_vector) - 1]

    # If the spawn_points list is empty, there are no more possible spots to place a new point.
    def finished(self):
        return self.seeded and not self.spawn_points

    # Generate all possible points, then return the list of (x, y) tuples
    def get_all_points(self):
        while not self.seeded or not self.finished():     # "not" of an empty list yields True
            self.generate_point()
        return self.points_vector
