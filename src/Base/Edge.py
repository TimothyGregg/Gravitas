from Base import Vertex, Toolbox


class Edge:
    def __init__(self, vertex1: Vertex, vertex2: Vertex, uid: int):
        # Create member variables
        self.v1 = vertex1
        self.v2 = vertex2
        self.uid = uid
        self.length = Toolbox.vertex_distance(vertex1, vertex2)
