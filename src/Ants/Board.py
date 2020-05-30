from Base.Graph import Graph


class Board(Graph):
	"""
	A Board for Ant games. This is a child class of Base.Graph.
	"""

	def __init__(self):
		"""
		Constructor for Board class.
		"""

		# Super Init call
		super().__init__()

	def update(self):
		"""
		A default update method for a Board.

		Returns:
			A boolean describing is the Board updated successfully.
		"""

		return True