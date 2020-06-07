import math
import random
from typing import Tuple
from typing import List


# TODO Type-hint
class PoissonGenerator:
    """
    Poisson point generator inspired by and partially adapted from: https://www.youtube.com/watch?v=7WcmyxyFO7o
    """

    def __init__(self, size_x: int, size_y: int, vertex_radius: float, spawn_tries: int = 4
                 , seed_point: Tuple[int, int] = None):
        """
        PoissonGenerator Constructor.

        Args:
            size_x: The maximum size of the AntBoard in the x-direction, positively from 0.
            size_y: The maximum size of the AntBoard in the y-direction, positively from 0.
            vertex_radius:  This is the EXCLUSION radius of a point within this graph. This is the radius of the circle
                drawn around each point in which the CENTER of another point cannot reside. The exclusion circles for
                point will overlap, but 1/2 the exclusion radius yields circles that should NEVER overlap.
            spawn_tries: Number of tries before a spawn point is removed from the spawn_points list
            seed_point: Seed point for point generation if one is given
        """

        self.size_x: int = size_x
        self.size_y: int = size_y
        self.vertex_radius: float = vertex_radius
        self.spawn_tries: int = spawn_tries
        self.seed_point: Tuple[int, int] = seed_point

        # Grid size variables
        self.cell_size: float = vertex_radius / math.sqrt(2)           # The cell size for the backing grid
        self.num_rows: int = math.ceil(size_x / self.cell_size)      # The number of rows in the backing grid
        self.column_size: int = math.ceil(size_y / self.cell_size)   # The number of elements in each column of the grid

        # The grid for smart distance checking
        self.grid: List[List[int]] = [[0 for _ in range(self.column_size)] for _ in range(self.num_rows)]    # Use "_"
        # for
        # unused
        # var
        # The grid contains all 0's by default, which indicates nothing is there. To indicate a vertex exists on the
        # grid, we add the index of the vertex within points_vector PLUS 1. Keep this in mind when indexing based on
        # values found in the grid.
        # This generates all 0's, and "[[0] * 10] * 10" will yield a list of ten references to the same list of 10 zeros

        # Flags
        self.seeded: bool = False     # Check to see if the board has been seeded.

        # Lists for tracking generated points and available spawn points
        self.points_vector: List[Tuple[int, int]] = []     # List of (x, y) coordinate tuples
        self.spawn_points: List[int] = []      # List of indices within points_vector where viable spawn points live

    def generate_point(self):
        """
        Generate a point based on the Poisson Disc algorithm.

        Returns:
            Returns a boolean indicating success (True) or failure (False).
        """

        # If the points_vector list is empty, the board has not been seeded yet.
        if not self.points_vector:
            # If there is no seed point given...
            if self.seed_point is None:
                # Add (x, y) tuple within the middle third to points_vector
                start_x: int = random.randint(int(self.size_x / 3), int(2 * self.size_x / 3))
                start_y: int = random.randint(int(self.size_y / 3), int(2 * self.size_y / 3))
            # If there IS a seed point given
            else:
                start_x: int = self.seed_point[0]
                start_y: int = self.seed_point[1]
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
            radius: float = self.vertex_radius * (1 + math.sqrt(random.random()))    # Distance in polar coordinates.
            # This is
            # specifically written to generate numbers that are evenly distributed through the area of the circle
            # drawn, not along the radius, as that would lead to a larger density at the center of the field. Read
            # more here: http://www.anderswallin.net/2009/05/uniform-random-points-in-a-circle-using-polar-coordinates/
            # The rounding is based on theta. Because the vertices are positioned at integer coordinates,
            # the floating-point distances between them can be messed up if you round them the same way every time.
            # This way, they always round to be INSIDE the bounding circle.
            theta: float = 2 * math.pi * random.random()  # Angle in polar coordinates
            x_addition: float = radius * math.cos(theta)  # The distance added in the x-direction
            y_addition: float = radius * math.sin(theta)  # The distance added in the y-direction
            if 0 <= theta < math.pi / 2:  # First quadrant rounding
                x_guess = self.points_vector[self.spawn_points[selected_spawn_point]][0] + math.floor(x_addition)
                y_guess = self.points_vector[self.spawn_points[selected_spawn_point]][1] + math.floor(y_addition)
            elif math.pi / 2 < theta < math.pi:  # Second quadrant rounding
                x_guess = self.points_vector[self.spawn_points[selected_spawn_point]][0] + math.ceil(x_addition)
                y_guess = self.points_vector[self.spawn_points[selected_spawn_point]][1] + math.floor(y_addition)
            elif math.pi < theta < 3 * math.pi / 2:  # Third quadrant rounding
                x_guess = self.points_vector[self.spawn_points[selected_spawn_point]][0] + math.ceil(x_addition)
                y_guess = self.points_vector[self.spawn_points[selected_spawn_point]][1] + math.ceil(y_addition)
            elif 3 * math.pi / 2 < theta <= 2 * math.pi:  # Fourth quadrant rounding
                x_guess = self.points_vector[self.spawn_points[selected_spawn_point]][0] + math.floor(x_addition)
                y_guess = self.points_vector[self.spawn_points[selected_spawn_point]][1] + math.ceil(y_addition)

            # Fail to generate if the point lies outside the limits of the graph
            if x_guess < 0 or x_guess > self.size_x or y_guess < 0 or y_guess > self.size_y:
                continue

            grid_x_pos = int(x_guess / self.cell_size)  # Grid x-location of the generated point
            grid_y_pos = int(y_guess / self.cell_size)  # Grid x-location of the generated point

            # Fail to generate if the grid already contains a point at the same grid location as the new point
            if bool(self.grid[grid_x_pos][grid_y_pos]):
                continue

            distance = 2 * self.vertex_radius  # A distance that is by default acceptable

            # Loop through the local x-range of the grid
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

    def get_next_point(self):
        """
        Generate an additional point.

        Returns:
            The (x, y) tuple of the new point.
        """

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

    def finished(self):
        """
        If the spawn_points list is empty, there are no more possible spots to place a new point.

        Returns:
            A boolean describing if the Generator is NO LONGER ABLE to generate points (True)
        """

        return self.seeded and not self.spawn_points

    def get_all_points(self):
        """
        Generate all possible points.

        Returns:
            A list of the (x, y) tuples of the points.
        """

        while not self.seeded or not self.finished():     # "not" of an empty list yields True
            self.generate_point()
        return self.points_vector
