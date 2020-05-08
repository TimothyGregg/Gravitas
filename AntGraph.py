from Graph import *
import random
import Toolbox


class AntGraph(Graph):
	def __init__(self, size_x: int, size_y: int, node_radius: float):
		super().__init__()
		self.size_x = size_x
		self.size_y = size_y
		self.node_radius = node_radius
		point_generator = Toolbox.PoissonGenerator(self.size_x, self.size_y, self.node_radius * 2)
		while not point_generator.finished():
			self.add_node(point_generator.get_next_point())

	def desmos_dump(self):
		for node in self.nodes:
			print("(" + str(node.x) + ", " + str(node.y) + ")")
			print("(x-" + str(node.x) + ")^2 + (y-" + str(node.y) + ")^2 = " + str(self.node_radius) + "^2")
