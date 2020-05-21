from Base import Vertex
from Toolbox.GraphMath import vertex_distance


class Edge:
    def __init__(self, vertex1: Vertex, vertex2: Vertex, uid: int):
        # Create member variables
        self.v1 = vertex1
        self.v2 = vertex2
        self.uid = uid
        self.length = vertex_distance(vertex1, vertex2)

    def __str__(self):
        return "Edge " + str(self.uid) + " [" + str(round(self.length)) + "]; Connecting Vertices " + str(
            self.v1.uid) + " and " + str(self.v2.uid)
