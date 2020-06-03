from Core import Vertex
from Toolbox.GraphMath import vertex_distance


class Edge:
    """
    An Edge class for use in Graph objects.
    """

    def __init__(self, vertex1: Vertex, vertex2: Vertex, uid: int):
        """
        Constructor for Edge class.

        Args:
            vertex1: One of the two Vertices that describes the Edge
            vertex2: The other Vertex that describes the Edge
            uid: The UID of the Edge to be created
        """

        # Create member variables
        self.v1: Vertex = vertex1
        self.v2: Vertex = vertex2
        self.uid: int = uid
        self.length: float = vertex_distance(vertex1, vertex2)

    def __str__(self):
        """
        A to_string method for the Edge class.

        Returns:
            A string representation of the Edge object.
        """

        return "Edge " + str(self.uid) + " [" + str(round(self.length)) + "]; Connecting Vertices " + str(
            self.v1.uid) + " and " + str(self.v2.uid)
