from Base.Graph import *
from Ants.Team import *
from Ants.Board import *
from Toolbox.PoissonGenerator import PoissonGenerator
from Toolbox.ColorGenerator import ColorGenerator
import random
import statistics
from typing import Dict


class AntBoard(Board):
	def __init__(self, size_x: int, size_y: int, vertex_radius: float, sparcity: float = 0.7,
														seed_point: Tuple[int, int] = None):
		# Graph super constructor
		super().__init__()

		# Member variables for Graph generation
		# TODO Set up validation for these inputs (i.e. no boards with 0 vertex radius)
		self.size_x = size_x
		self.size_y = size_y
		self.vertex_radius = vertex_radius
		self.sparcity = sparcity
		self.seed_point = seed_point

		# Member variables for gameplay
		# A dict containing the teams, keyed by team UID
		# team.uid : Team
		self.teams: Dict[int, Team] = {}

		# Generate the actual Graph elements
		self.add_vertices()
		self.add_edges()
		self.add_teams(7)

	# Grab all the points for the graph from a Poisson-Disc point generator
	def add_vertices(self):
		all_points = []
		# TODO Shrinking them here messes up the rendering on really small boards. This seems like such a minor issue
		#  that I'm going to ignore it until later.
		default_radius = self.vertex_radius
		tries = 20
		while len(all_points) < 4:  # 4 is the minimum for Delaunay Triangulation
			if self.seed_point is None:
				all_points = PoissonGenerator(self.size_x, self.size_y, self.vertex_radius * 2).get_all_points()
			else:
				all_points = PoissonGenerator(self.size_x, self.size_y, self.vertex_radius * 2,
											  seed_point=self.seed_point).get_all_points()
			tries -= 1
			if tries == 0:
				self.vertex_radius -= 1
				tries = 20
		self.vertex_radius = default_radius  # Reset the default vertex_radius of the board after shrinking to fit the
		# game board
		for point_tuple in all_points:
			self.add_vertex(point_tuple)

	def add_edges(self):
		# Generate the Delauney edges using the Voronoi method and connect them
		edge_dict = self.get_voronoi_diagram_ridge_lines()
		edge_lengths = []
		for vertex1_uid in edge_dict:
			for vertex2_uid in edge_dict[vertex1_uid]:
				new_edge_uid = self.connect_vertices(self.vertices[vertex1_uid], self.vertices[vertex2_uid])
				edge_lengths.append(self.edges[new_edge_uid].length)

		# Cull edges that are too long (typically along the edges, with crazy-big circles
		# TODO this may be able to be rolled in to part of the computation of the Voronoi regions (i.e. the regions
		#  that extent to infinity are probably those with long edges spanning the exterior of the graph)
		average = sum(edge_lengths) / len(edge_lengths)
		st_dev = statistics.stdev(edge_lengths)
		all_edge_keys = list(self.edges.keys())
		for edge_uid in all_edge_keys:

			if self.edges[edge_uid].length > average + st_dev:
				self.disconnect_edge(edge_uid)

		# remove random edges to generate edge sparcity
		all_edge_keys = list(self.edges.keys())
		to_remove = []
		for edge_uid in all_edge_keys:
			# Ignore the potential to remove an edge if the edge is the only edge connecting that vertex
			n1_uid = self.edges[edge_uid].v1.uid
			n2_uid = self.edges[edge_uid].v2.uid
			if len(self.adjacency_list[n1_uid]) < 2:
				continue
			if len(self.adjacency_list[n2_uid]) < 2:
				continue

			# Randomly remove edges based on sparcity
			if random.random() > self.sparcity:
				to_remove.append(edge_uid)
		for edge_uid in to_remove:
			if not self.is_bridge(edge_uid):
				self.disconnect_edge(edge_uid)

	# Add teams to the board
	def add_teams(self, num_teams: int):
		# Method to pick a starting location within the graph ot place the team.
		# TODO determine spacing between teams so that they do not start too close together
		def select_starting_position():
			# Try to pick a vertex until all are determined to be bad
			tries = []
			while len(tries) < len(self.vertices):
				# Pick a random vertex to check if it has been used already
				picked_uid = random.choice(list(self.vertices.keys()))
				good = True
				# Check if the picked vertex uid is in any of the teams vertices dicts
				for team_uid_it in self.teams:
					if picked_uid in self.teams[team_uid_it].controlled_vertices:
						# If the vertex is already controlled by a team, flag it as no good and add it to the
						# already-tried uid list
						good = False
						tries.append(picked_uid)
						break
				# If the vertex uid wasn't in use, return the vertex itself
				if good:
					return self.vertices[picked_uid]
			# If a good vertex cannot be found, return None
			return None

		c = ColorGenerator()
		# Generate the teams
		for team_uid in range(num_teams):
			# If the color generator has a unique color available for the new team to be generated, continue. If not,
			# we're done making teams.
			# Also, if we've added as many teams as we have vertices, we cannot possibly add any more, and we're done
			# making teams
			if c.has_more() and len(self.teams) < len(self.vertices):
				self.teams[team_uid] = Team(team_uid, c.request(), self)
				self.teams[team_uid].add_vertex(select_starting_position())

	# This is for use at https://www.desmos.com/calculator for easy, copy-paste graphing
	def desmos_dump(self):
		for vertex_uid in self.vertices:
			vertex = self.vertices[vertex_uid]
			print("(" + str(vertex.x) + ", " + str(vertex.y) + ")")
			print("(x-" + str(vertex.x) + ")^2 + (y-" + str(vertex.y) + ")^2 = " + str(self.vertex_radius) + "^2")
		for edge in self.edges:
			print("((1-t)" + str(edge.v1.x) + "+t*" + str(edge.v2.x) + ",(1-t)" + str(edge.v1.y) + "+t*" + str(
				edge.v2.y) + ")")
