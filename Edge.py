import Toolbox


class Edge:
    def __init__(self, node1, node2):
        # Create member variables
        self.n1 = node1
        self.n2 = node2
        self.length = Toolbox.node_distance(node1, node2)
