import Toolbox
import Node


class Edge:
    def __init__(self, node1: Node, node2: Node, uid: int):
        # Create member variables
        self.n1 = node1
        self.n2 = node2
        self.uid = uid
        self.length = Toolbox.node_distance(node1, node2)
