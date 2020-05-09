from Graph import *
import Toolbox
import statistics


class AntGraph(Graph):
	def __init__(self, size_x: int, size_y: int, node_radius: float):
		# Graph super constructor
		super().__init__()

		# Member variables TODO Set up validation for these inputs (i.e. no boards with 0 node radius)
		self.size_x = size_x
		self.size_y = size_y
		self.node_radius = node_radius
		self.edge_lengths = []

		# Grab all the points for the graph from a Poisson-Disc point generator
		all_points = []
		while len(all_points) < 4:  # 4 is the minimum for Delaunay Triangulation
			all_points = Toolbox.PoissonGenerator(self.size_x, self.size_y, self.node_radius * 2).get_all_points()
		for point_tuple in all_points:
			self.add_node(point_tuple)

		# Generate and create edges
		edge_dict = self.generate_delauney_edges()
		for node1_uid in edge_dict:
			for node2_uid in edge_dict[node1_uid]:
				if not self.connected(node1_uid, node2_uid):
					new_edge_uid = self.connect_nodes(self.nodes[node1_uid], self.nodes[node2_uid])
					self.edge_lengths.append(self.edges[new_edge_uid].length)

		# Cull edges that are too long (typically along the edges, with crazy-big circles
		average = sum(self.edge_lengths) / len(self.edge_lengths)
		st_dev = statistics.stdev(self.edge_lengths)
		all_edge_keys = list(self.edges.keys())
		for edge_uid in all_edge_keys:
			if self.edges[edge_uid].length > average + st_dev:
				self.disconnect_edge(edge_uid)

		# Print the graph-able text to the console.
		# self.desmos_dump()

	# This is for use at https://www.desmos.com/calculator for easy, copy-paste graphing
	def desmos_dump(self):
		for node_uid in self.nodes:
			node = self.nodes[node_uid]
			print("(" + str(node.x) + ", " + str(node.y) + ")")
			print("(x-" + str(node.x) + ")^2 + (y-" + str(node.y) + ")^2 = " + str(self.node_radius) + "^2")
		for edge in self.edges:
			print("((1-t)" + str(edge.n1.x) + "+t*" + str(edge.n2.x) + ",(1-t)" + str(edge.n1.y) + "+t*" + str(
				edge.n2.y) + ")")
