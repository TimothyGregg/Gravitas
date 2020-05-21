from Base.Graph import Graph
from Toolbox.PoissonGenerator import PoissonGenerator
import math
from Toolbox.LineSegmentOverlap import do_intersect
from typing import Tuple
# import time


# Once we get the Voronoi regions figured out, we'll use that code to exclude the exterior edges on a graph that
# regenerates the Voronoi edges after adding each Vertex, hopefully making for an interesting, incremental graph
# building process that you can watch.
class IncrementalGraph(Graph):
	def __init__(self, size_x: int, size_y: int, vertex_radius: float, sparcity: float = 0.7
				 , seed_point: Tuple[int, int] = None):
		# Graph super constructor
		super().__init__()

		# Member variables TODO Set up validation for these inputs (i.e. no boards with 0 vertex radius)
		self.size_x = size_x
		self.size_y = size_y
		self.vertex_radius = vertex_radius
		self.sparcity = sparcity
		self.edge_lengths = []

		# The generator to pull each new point from
		if seed_point is None:
			self.generator = PoissonGenerator(self.size_x, self.size_y, self.vertex_radius * 2)
		else:
			self.generator = PoissonGenerator(self.size_x, self.size_y, self.vertex_radius * 2, seed_point=seed_point)
		self.vertex_positions = {}  # To store vertex positions for easy lookup in add_next_vertex

	# TODO This sometimes generates unconnected vertices AND sometimes generates edges that overlap, like when you
	#  have 4 vertices that arrange in a square, it connects across both diagonals. This might require logic
	#  regarding the Voronoi diagram infinite edge exclusion thing I was going to add to the
	#  Graph.get_voronoi-ridge_lines() method. That's probably a good place to play around next.
	# Add the next vertex that the point generator spits out AND connect it to all vertices that fall outside it's
	# exclusion radius but inside it's spawn radius
	def add_next_vertex(self):
		# Add the next Vertex
		if not self.generator:
			raise RuntimeError("The generator ran dry. Don't let it do that. Check \"not self.generator\"")
		new_point_position = self.generator.get_next_point()
		new_vertex_uid = self.add_vertex(new_point_position)
		self.vertex_positions[new_point_position] = new_vertex_uid  # Store the uid as a function of its position,
		# for fast lookup

		# Stolen code from the Poisson Generator. Yeah, we're hacking our own class here but it'll work and doesn't
		# add any real time or memory to the program.
		grid_x_pos = int(new_point_position[0] / self.generator.cell_size)  # Grid x-location of the generated point
		grid_y_pos = int(new_point_position[1] / self.generator.cell_size)  # Grid x-location of the generated point

		grid_scan_size = 7  # Should be odd, but modifying this will adjust how far a node looks to connect
		# Loop through the local x-range of the grid in self.generator
		for x_it in range(grid_x_pos - int(grid_scan_size / 2), grid_x_pos + (int(grid_scan_size / 2) + 1)):
			# Check if outside the x-bounds of the grid
			if x_it < 0 or x_it > len(self.generator.grid) - 1:
				continue

			# loop through the local y-range of the grid
			for y_it in range(grid_y_pos - int(grid_scan_size / 2), grid_y_pos + (int(grid_scan_size / 2) + 1)):
				# Check if outside the y-bounds of the grid
				if y_it < 0 or y_it > len(self.generator.grid[x_it]) - 1:
					continue

				# Skip ya' self
				if y_it == grid_y_pos and x_it == grid_x_pos:
					continue

				# If the generator has a point in the grid near the new point AND it isn't the newest point the
				# generator made (because it makes one ahead of time), connect the new node to the one found in the grid
				# TODO: Check for overlaps, perhaps using an edge graph. This maybe should go in Graph.py
				if self.generator.grid[x_it][y_it] and self.generator.grid[x_it][y_it] < \
					len(self.generator.points_vector):  # returns True if the value is > 0, i.e. there is a point

					other_point_position = self.generator.points_vector[self.generator.grid[x_it][y_it] - 1]
					dx = new_point_position[0] - other_point_position[0]
					dy = new_point_position[1] - other_point_position[1]
					distance = math.sqrt(dx ** 2 + dy ** 2)

					# If the point that we found is inside the spawn radius of the point (note: it should ALWAYS be
					# outside the exclusion radius (self.vertex_radius * 2) by virtue of how the points are generated in
					# the Poisson Generator), we should connect them.
					if distance <= self.vertex_radius * 4:
						# Connect the new vertex to its neighbor
						self.connect_vertices(self.vertices[self.vertex_positions[new_point_position]],
											  self.vertices[self.vertex_positions[other_point_position]])

		#################################################
		# Here starts mayhem
		# All this code exists solely to prevent overlapping edges in the graph. This can be simplified to an
		# unbelievable degree I am sure

		# start = time.perf_counter()

		# self.desmos_dump()
		# print("-------------------------")

		to_remove = []
		# For each vertex connected to the one just added...
		for other_vertex_uid in self.adjacency_list[new_vertex_uid]:
			# For each of that vertex's connected vertices...
			for connected_to_other_vertex_uid in self.adjacency_list[other_vertex_uid]:
				# Ensure that the vertices of the connections of the just-added vertex do not overlap. If they do,
				# remove them.
				for connected_vertex_uid in self.adjacency_list[new_vertex_uid]:
					# Continue when the connection we're checking on is the same as the one we are looking at in this
					# inner-most loop
					if other_vertex_uid == connected_vertex_uid:
						continue

					# Continue when we're looking at the reverse of the current connection
					elif new_vertex_uid == connected_to_other_vertex_uid:
						continue

					# Continue when the other point is connected to the same one we're looking at (or something. I'm
					# just going by similarity here. This is hurting my brain.)
					elif connected_to_other_vertex_uid == connected_vertex_uid:
						continue

					# Otherwise, check if they're overlapping. If they are, remove the connection
					else:
						if do_intersect(new_point_position, (self.vertices[connected_vertex_uid].x, self.vertices[
							connected_vertex_uid].y), (self.vertices[other_vertex_uid].x, self.vertices[
							other_vertex_uid].y), (self.vertices[connected_to_other_vertex_uid].x, self.vertices[
							connected_to_other_vertex_uid].y)):
							to_remove.append(connected_vertex_uid)  # The vertex_uid to remove the connection
						# to new_vertex_uid from

		# TODO there has to be a better way to do this; it's terrible. I may set up a whole internal class for Edges in
		#  Graph.py and make them more easily searchable by uid or by either of their vertices
		for other_vertex_uid in to_remove:
			for edge_uid in self.edges:
				# If the vertex that this vertex is connected to is the second vertex in an edge containing this new
				# vertex, remove the edge.
				if self.edges[edge_uid].v1.uid == other_vertex_uid and self.edges[edge_uid].v2.uid == new_vertex_uid \
						or self.edges[edge_uid].v2.uid == other_vertex_uid and self.edges[edge_uid].v1.uid == \
						new_vertex_uid:
					self.disconnect_edge(edge_uid)
					# Break, because it should only be true for one edge, and we don't want to concurently modify
					break

		# print(time.perf_counter() - start)

		# Here ends mayhem
		#################################################

		# This should NEVER trip, after I messed with the rounding errors in the Poisson Generator.
		if (len(self.vertices) > 1) & (len((self.adjacency_list[len(self.vertices) - 1])) == 0):
			raise RuntimeError("Vertex not connected in generation: " + str(self.vertices[len(self.vertices) - 1]))

		# After it's completed, destroy the generator if it is finished
		if self.generator.finished():
			self.generator = None

	# Define an update to an incremental graph as just being the addition of a vertex
	def update(self):
		if self.generator:
			self.add_next_vertex()
			return True
		return False

	# This is for use at https://www.desmos.com/calculator for easy, copy-paste graphing
	def desmos_dump(self):
		for vertex_uid in self.vertices:
			vertex = self.vertices[vertex_uid]
			print("(" + str(vertex.x) + ", " + str(vertex.y) + ")")
			print("(x-" + str(vertex.x) + ")^2 + (y-" + str(vertex.y) + ")^2 = " + str(self.vertex_radius) + "^2")
			print("(x-" + str(vertex.x) + ")^2 + (y-" + str(vertex.y) + ")^2 = " + str(self.vertex_radius * 4) + "^2")
		for edge_uid in self.edges:
			print("((1-t)" + str(self.edges[edge_uid].v1.x) + "+t*" + str(self.edges[edge_uid].v2.x) + ",(1-t)" +
				  str(self.edges[edge_uid].v1.y) + "+t*" + str(self.edges[edge_uid].v2.y) + ")")
