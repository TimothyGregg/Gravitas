from Base.Edge import *
from Base.Node import *
from typing import Tuple
import numpy
from scipy.spatial import Voronoi


class Graph:
    def __init__(self):
        self._node_uid = 0
        self._edge_uid = 0
        self.nodes = {}
        self.edges = {}
        self.adjacency_list = {}  # A classic graph adjacency list for easy connectivity checks

    # Add a node to the graph. Ensures that a node is not placed on top of a previous node
    def add_node(self, location: Tuple[int, int]):
        for node_uid in self.nodes:
            if self.nodes[node_uid].x == location[0] and self.nodes[node_uid].y == location[1]:
                raise RuntimeError("Node already at (" + str(location[0]) + ", " + str(location[1]) + ") in graph")
        new_node = Node(location[0], location[1], self._node_uid)
        self._node_uid += 1
        self.nodes[new_node.uid] = new_node
        self.adjacency_list[new_node.uid] = []

    # Create an Edge connecting two Nodes. Also make a node that each node is connected to the other. Return the uid
    # of the Edge that was just created
    def connect_nodes(self, node1: Node, node2: Node, edge_uid: int = None):
        if edge_uid is None:
            new_edge = Edge(node1, node2, self._edge_uid)
            self._edge_uid += 1
        # For when an Edge is being replaced
        else:
            new_edge = Edge(node1, node2, edge_uid)
        self.edges[new_edge.uid] = new_edge
        self.adjacency_list[node1.uid].append(node2.uid)
        self.adjacency_list[node2.uid].append(node1.uid)
        return new_edge.uid

    # delete the Edge connecting two nodes
    def disconnect_edge(self, edge_uid: int):
        edge = self.edges[edge_uid]
        node1 = edge.n1
        node2 = edge.n2
        self.adjacency_list[node1.uid].remove(node2.uid)
        self.adjacency_list[node2.uid].remove(node1.uid)
        if edge_uid in self.edges:
            del self.edges[edge_uid]
        else:
            raise RuntimeError("You goofed on the key for an Edge removal.")

    # Return a list of tuples, with (node_uid, node_position)
    def get_node_position_list(self):
        node_uid_list = []
        node_position_list = []
        for node_uid in self.nodes:
            node_uid_list.append(node_uid)
            node_position_list.append((self.nodes[node_uid].x, self.nodes[node_uid].y))
        return [(node_uid_list[it], node_position_list[it]) for it in range(0, len(node_uid_list))]

    # Reference: https://www.geeksforgeeks.org/check-removing-given-edge-disconnects-given-graph/
    # Return True if the graph is connected; otherwise, False
    def is_connected(self):
        # Make the visited list and do a DFS
        visited = {}
        stack = [self.nodes[0].uid]
        for node_uid in self.nodes:
            visited[node_uid] = False
        # nodes to (but not including) 0 (step by -1
        while stack:
            node_uid = stack[-1]
            if not visited[node_uid]:
                visited[node_uid] = True
                stack.pop()
                for connected_node_uid in self.adjacency_list[node_uid]:
                    stack.append(connected_node_uid)
            else:
                stack.pop()

        # True if all nodes reachable from the first, otherwise False
        return all(list(visited[node_uid] for node_uid in visited))

    # Indicates is an edge_uid describes an edge that, when removed, will make the board unconnected
    def is_bridge(self, edge_uid):
        # Remove the Edge
        n1 = self.edges[edge_uid].n1
        n2 = self.edges[edge_uid].n2
        self.disconnect_edge(edge_uid)

        # Check if the graph is still connected
        connected = self.is_connected()

        # Put the Edge back
        self.connect_nodes(n1, n2, edge_uid)

        # Indicate if that Edge removal led to an unconnected board
        return not connected

    # Return a list of all node connections to be made as a pseudo-adjacency list, but with each connection appearing
    # only once (i.e. if Node 1 is connected to Node 2, Node 2 won't show as also being connected to Node 1)
    def get_voronoi_diagram_ridge_lines(self):
        # Someone else does all the fancy math for me
        node_position_list = self.get_node_position_list()
        voronoi = Voronoi(numpy.array([node_tuple[1] for node_tuple in self.get_node_position_list()]))

        # Storage variable
        node_connections = {}
        for node_uid in self.nodes:
            node_connections[self.nodes[node_uid].uid] = []  # Seems redundant, but I just want to be safe here

        # Dump the ridge points array into the same format as used in the Delaunay case
        for pair in voronoi.ridge_points:
            # Use the UIDs from the node_position_dict just in case UIDs got scrambled and aren't in order
            node_connections[node_position_list[pair[0]][0]].append(node_position_list[pair[1]][0])

        # This **ISN'T** twice as large as the set of all connections. It contains only one element of each list in each
        # key for each connection.
        return node_connections
