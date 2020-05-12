from Base.Graph import Graph
from Base import Toolbox
from typing import Tuple


# Once we get the Voronoi regions figured out, we'll use that code to exclude the exterior edges on a graph that
# regenerates the Voronoi edges after adding each Vertex, hopefully making for an interesting, incremental graph
# building process that you can watch.
class IncrementalGraph(Graph):
	def __init__(self, size_x: int, size_y: int, vertex_radius: float, sparcity: float = 0.7):
		# Graph super constructor
		super().__init__()

		# Member variables TODO Set up validation for these inputs (i.e. no boards with 0 vertex radius)
		self.size_x = size_x
		self.size_y = size_y
		self.vertex_radius = vertex_radius
		self.sparcity = sparcity
		self.edge_lengths = []

		# The generator to pull each new point from
		self.generator = Toolbox.PoissonGenerator(self.size_x, self.size_y, self.vertex_radius * 2)

	# Add the next vertex that the point generator spits out
	def add_next_vertex(self):
		# Add the next Vertex
		if not self.generator:
			raise RuntimeError("The generator ran dry. Don't let it do that. Check \"not self.generator\"")
		self.add_vertex(self.generator.get_next_point())

		# Add the Edges that connect to the new Vertex
		# TODO Connections here are going to be tough. I think I can just connect them to each vertex within their
		#  possible generation range. This will require the construction of a grid perhaps? It might be able to use
		#  the same dimensions as the one in the generator. In fact, I think it should. We can use generator.grid AH
		#  but it doesn't have vertex uids stored, just their positions. Crud. Maybe we build that in this object,
		#  kind of AS A VERTEX IS ADDED THAT WAY IT'S O(N) YES THIS IS THE STRAT.

		# Ok bedtime

		# The Vertices of a graph with all the Voronoi edges will always (?) be connected to all the Vertices within
		# the Poisson generation range for that Vertex. It may also be connected to others, but I think it's ok to
		# leave those out. It'll end up with some pre-instilled sparce-ness from the connection algorithm,
		# but I don't mind that.

		# After it's completed, destroy the generator if it is finished
		if self.generator.finished():
			self.generator = None
