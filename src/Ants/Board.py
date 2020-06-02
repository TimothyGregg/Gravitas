from Base.Graph import Graph


class Board(Graph):
	"""
	A Board for Ant games. This is a child class of Base.Graph.
	"""

	def __init__(self,  size_x: int, size_y: int, vertex_radius: float):
		"""
		Constructor for Board class.

		Args:
			size_x: The maximum size of the AntBoard in the x-direction, positively from 0.
			size_y: The maximum size of the AntBoard in the y-direction, positively from 0.
			vertex_radius: The VISUAL radius of a vertex within the Board. Twice this value is the minimum distance
				between two Vertices
		"""

		# Super Init call
		super().__init__()

		# Member variables
		self.size_x = size_x
		self.size_y = size_y
		self.vertex_radius = vertex_radius

	def update(self):
		"""
		A default update method for a Board.

		Returns:
			A boolean describing is the Board updated successfully.
		"""

		return True

	def desmos_dump(self):
		"""
		This is for use at https://www.desmos.com/calculator for easy, copy-paste graphing.
		Somewhat deprecated now that I have a visualization tool, but sometimes helpful for sneaky-small math problems.

		Returns:
			A string representation of the Board that can be copy-and-pasted into the calculator.
		"""

		out_str = ""
		for vertex_uid in self.vertices:
			vertex = self.vertices[vertex_uid]
			out_str += "(" + str(vertex.x) + ", " + str(vertex.y) + ")"
			out_str += "(x-" + str(vertex.x) + ")^2 + (y-" + str(vertex.y) + ")^2 = " + str(self.vertex_radius) + "^2"
		for edge in self.edges:
			out_str += "((1-t)" + str(edge.v1.x) + "+t*" + str(edge.v2.x) + ",(1-t)" + str(edge.v1.y) + "+t*" + str(
				edge.v2.y) + ")"
		return out_str