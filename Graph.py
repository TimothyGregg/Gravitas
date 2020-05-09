from Edge import *
from Node import *
from typing import Tuple
import numpy
from scipy.spatial import Voronoi


class Graph:
    def __init__(self):
        self._node_uid = 0
        self._edge_uid = 0
        self.nodes = {}
        self.edges = {}
        self.node_edges = {}    # Maybe make this a map with the node uid

    # Add a node to the graph. Ensures that a node is not placed on top of a previous node
    def add_node(self, location: Tuple[int, int]):
        for node_uid in self.nodes:
            if self.nodes[node_uid].x == location[0] and self.nodes[node_uid].y == location[1]:
                raise RuntimeError("Node already at (" + str(location[0]) + ", " + str(location[1]) + ") in graph")
        new_node = Node(location[0], location[1], self._node_uid)
        self._node_uid += 1
        self.nodes[new_node.uid] = new_node
        self.node_edges[new_node.uid] = []

    # Create an Edge connecting two Nodes. Also make a node that each node is connected to the other. Return the uid
    # of the Edge that was just created
    def connect_nodes(self, node1: Node, node2: Node):
        new_edge = Edge(node1, node2, self._edge_uid)
        self._edge_uid += 1
        self.edges[new_edge.uid] = new_edge
        self.node_edges[node1.uid].append(node2.uid)
        self.node_edges[node2.uid].append(node1.uid)
        return new_edge.uid

    # delete the Edge connecting two nodes
    def disconnect_edge(self, edge_uid: int):
        edge = self.edges[edge_uid]
        node1 = edge.n1
        node2 = edge.n2
        self.node_edges[node1.uid].remove(node2.uid)
        self.node_edges[node2.uid].remove(node1.uid)
        if edge_uid in self.edges:
            del self.edges[edge_uid]
        else:
            raise RuntimeError("You goofed on the key for an Edge removal.")

    # Return a tuple of (list of UIDs corresponding to..., list of tuples with each node position)
    def get_node_position_list(self):
        node_uid_list = []
        node_position_list = []
        for node_uid in self.nodes:
            node_uid_list.append(node_uid)
            node_position_list.append((self.nodes[node_uid].x, self.nodes[node_uid].y))
        return {"UIDs": node_uid_list, "Positions": node_position_list}

    # Checks if the second node is in the list of connected nodes for the first node. Should work either direction.
    # Maybe make this check for errors? I dunno. If you get this far and it's messed up, you've goofed.
    def connected(self, node1_uid: int, node2_uid: int):
        return node2_uid in self.node_edges[node1_uid]

    def get_voronoi_diagram_ridge_lines(self):
        # Someone else does all the fancy math for me
        node_position_dict = self.get_node_position_list()
        voronoi = Voronoi(numpy.array(node_position_dict["Positions"]))

        # Storage variable
        node_connections = {}
        for node_uid in self.nodes:
            node_connections[self.nodes[node_uid].uid] = []  # Seems redundant, but I just want to be safe here

        # Dump the ridge points array into the same format as used in the Delaunay case
        for pair in voronoi.ridge_points:
            # Use the UIDs from the node_position_dict just in case UIDs got scrambled and aren't in order
            node_connections[node_position_dict["UIDs"][pair[0]]].append(node_position_dict["UIDs"][pair[1]])

        # This **ISN'T** twice as large as the set of all connections. It contains only one element of each list in each
        # key for each connection.
        return node_connections
