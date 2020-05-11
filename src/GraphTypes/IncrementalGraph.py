from Base.Graph import Graph


# Once we get the Voronoi regions figured out, we'll use that code to exclude the exterior edges on a graph that
# regenerates the Voronoi edges after adding each Node, hopefully making for an interesting, incremental graph
# building process that you can watch.
class IncrementalGraph(Graph):
	def __init__(self, size_x: int, size_y: int, node_radius: float, sparcity: float = 0.7):
		# Graph super constructor
		super().__init__()

		# Member variables TODO Set up validation for these inputs (i.e. no boards with 0 node radius)
		self.size_x = size_x
		self.size_y = size_y
		self.node_radius = node_radius
		self.sparcity = sparcity
		self.edge_lengths = []
