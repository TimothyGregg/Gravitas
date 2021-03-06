from Core.Graph import *
from Ants.Team import *
from Ants.Board import *
from Ants.Base import Base
from Toolbox.PoissonGenerator import PoissonGenerator
from Toolbox.ColorGenerator import ColorGenerator
import random
import statistics
from typing import Dict
from typing import Set
from typing import List


class AntBoard(Board):
	"""
	A type of Board on which the Ant game is played. It contains all of the elements required to operate an instance
	of an Ant game.
	"""

	def __init__(self, size_x: int, size_y: int, vertex_radius: float, sparcity: float = 0.7,
														seed_point: Tuple[int, int] = None):
		"""
		The constructor of the AntBoard class.

		Args:
			sparcity: A fractional value describing the chance that, after fully generating, any given Edge will be
				deleted (assuming the Edge itself is not a bridge).
			seed_point: A tuple describing the initial point placed on the Board.
		"""

		# Graph super constructor
		super().__init__(size_x, size_y, vertex_radius)

		# Member variables for Graph generation
		self.sparcity: float = sparcity
		self.seed_point: Tuple[int, int] = seed_point

		# Member variables for gameplay
		# A dict containing the teams, keyed by team UID
		# team.uid : Team
		self.teams: Dict[int, Team] = {}

		# Generate the actual Graph elements
		self.add_vertices()
		self.add_edges()

		# A dict of Bases, keyed by corresponding vertex UID
		self.bases: Dict[int, Base] = {}

		# Generate the ant game elements
		self.add_bases()
		self.add_teams(1)

	def add_vertices(self):
		"""
		Grab all the points for the graph from a Poisson-Disc point generator
		"""

		all_points: List[Tuple[int, int]] = []
		default_radius: float = self.vertex_radius
		tries: int = 20
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
		"""
		Add all Delauney edges to the Board based on the position of the Vertices.
		"""

		# Generate the Delauney edges using the Voronoi method and connect them
		edge_dict = self.get_voronoi_diagram_ridge_lines()  # TODO Type hint
		edge_lengths: List[float] = []
		for vertex1_uid in edge_dict:
			for vertex2_uid in edge_dict[vertex1_uid]:
				new_edge_uid: int = self.connect_vertices(self.vertices[vertex1_uid], self.vertices[vertex2_uid])
				edge_lengths.append(self.edges[new_edge_uid].length)

		# Cull edges that are too long (typically along the edges, with crazy-big circles
		# TODO this may be able to be rolled in to part of the computation of the Voronoi regions (i.e. the regions
		#  that extent to infinity are probably those with long edges spanning the exterior of the graph)
		average: float = sum(edge_lengths) / len(edge_lengths)
		st_dev: float = statistics.stdev(edge_lengths)
		all_edge_keys: List[int] = list(self.edges.keys())
		for edge_uid in all_edge_keys:

			if self.edges[edge_uid].length > average + st_dev:
				self.disconnect_edge(edge_uid)

		# remove random edges to generate edge sparcity
		all_edge_keys: List[int] = list(self.edges.keys())
		to_remove: List[int] = []
		for edge_uid in all_edge_keys:
			# Ignore the potential to remove an edge if the edge is the only edge connecting that vertex
			n1_uid: int = self.edges[edge_uid].v1.uid
			n2_uid: int = self.edges[edge_uid].v2.uid
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

	def add_bases(self):
		"""
		Add a Core object on top of each Vertex. These Bases are the real meat of the game board.
		"""

		# Add a standard Core on top of each Vertex
		for vertex_uid in self.vertices:
			self.bases[vertex_uid] = Base(vertex_uid)

	def add_teams(self, num_teams: int):
		"""
		Add the Teams to the Board. TODO Currently a naive implementation
		Args:
			num_teams: The number of Teams to attempt to add to the Board.
		"""

		def select_a_starting_position(all_bases: Set[int], used_bases: Set[int]):
			"""
			Method to pick a starting location for a Team within the graph.
			TODO determine spacing between teams so that they do not start too close together.

			Args:
				all_bases: The set of all Bases in the Graph.
				used_bases: The set of all Bases that have already been chosen as a starting point in the Graph.

			Returns:
				The Vertex that has been picked as a valid starting position.
			"""

			available_bases = all_bases.difference(used_bases)
			if len(available_bases) > 0:
				base_uid_choice = random.choice(list(available_bases))
				return self.bases[base_uid_choice]
			return None

		c: ColorGenerator = ColorGenerator()
		used_bases: Set[int] = set()
		all_bases: Set[int] = set(self.bases.keys())
		# Generate the teams
		for team_uid in range(num_teams):
			# If the color generator has a unique color available for the new team to be generated, continue. If not,
			# we're done making teams.
			# Also, if we've added as many teams as we have vertices, we cannot possibly add any more, and we're done
			# making teams
			if c.has_more() and len(used_bases) < len(self.bases):
				self.teams[team_uid] = Team(team_uid, c.request(), self)
				base_choice: Base = select_a_starting_position(all_bases, used_bases)
				self.teams[team_uid].add_base(base_choice)
				used_bases.add(base_choice.uid)
