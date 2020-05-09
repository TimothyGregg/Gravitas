from Edge import *
from Node import *
from typing import Tuple
import numpy
from scipy.spatial import Delaunay


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

    # Return a list of tuples with each node position
    def get_node_position_list(self):
        node_position_list = []
        for node_uid in self.nodes:
            node_position_list.append((self.nodes[node_uid].x, self.nodes[node_uid].y))
        return node_position_list

    # Checks if the second node is in the list of connected nodes for the first node. Should work either direction.
    # Maybe make this check for errors? I dunno. If you get this far and it's messed up, you've goofed.
    def connected(self, node1_uid: int, node2_uid: int):
        return node2_uid in self.node_edges[node1_uid]

    # Generates a dict of the Delauney edges of the graph. This dict has keys equal to a Node's uid and the value is a
    # list of other Node uids that the key node is connected to
    def generate_delauney_edges(self):
        # Generate the Delauney triangles
        triangles = Delaunay(numpy.array(self.get_node_position_list()))

        # Storage variable
        node_connections = {}
        for node_uid in self.nodes:
            node_connections[self.nodes[node_uid].uid] = []  # Seems redundant, but I just want to be safe here
        # Turn the Delauney triangles into edges for the graph
        for tri in triangles.simplices:
            # Grab each node in the triangle
            try:
                node1 = self.nodes[tri[0]]
                node2 = self.nodes[tri[1]]
                node3 = self.nodes[tri[2]]
            except KeyError:
                print("tri[0]: " + str(tri[0]) + "\ntri[1]: " + str(tri[1]) + "\ntri[2]: " + str(tri[2]))
                print(self.nodes.keys())
                raise RuntimeError("This goofed.")

            # Nodes 2 and 3 should be connected to node 1
            if node2.uid not in node_connections[node1.uid]:
                node_connections[node1.uid].append(node2.uid)
            if node3.uid not in node_connections[node1.uid]:
                node_connections[node1.uid].append(node3.uid)

            # Nodes 1 and 3 should be connected to node 2
            if node1.uid not in node_connections[node2.uid]:
                node_connections[node2.uid].append(node1.uid)
            if node3.uid not in node_connections[node2.uid]:
                node_connections[node2.uid].append(node3.uid)

            # Nodes 1 and 2 should be connected to node 3
            if node1.uid not in node_connections[node3.uid]:
                node_connections[node3.uid].append(node1.uid)
            if node2.uid not in node_connections[node3.uid]:
                node_connections[node3.uid].append(node2.uid)

        # This is a dict, where each key is the uid of a node, and each value is a list of all nodes' uids that are
        # connected to that node
        return node_connections
