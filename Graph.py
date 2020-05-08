from Edge import *
from Node import *
from typing import Tuple


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.node_edges = []    # Maybe make this a map with the node uid

    def num_nodes(self):
        return len(self.nodes)

    def add_node(self, location: Tuple[int, int]):
        for node in self.nodes:
            if node.x == location[0] and node.y == location[1]:
                raise RuntimeError("Node already at (" + str(location[0]) + ", " + str(location[1]) + ") in graph")
        self.nodes.append(Node(location[0], location[1]))

    def connect_nodes(self, node1: Node, node2: Node):
        new_edge = Edge(node1, node2)
        self.node_edges[node1.uid].append(new_edge)
        self.node_edges[node2.uid].append(new_edge)
