from Base.Edge import *
from Base.Vertex import *
from typing import Tuple
import numpy
from scipy.spatial import Voronoi


class Graph:
    def __init__(self):
        self._vertex_uid = 0
        self._edge_uid = 0
        self.vertices = {}
        self.edges = {}
        self.adjacency_list = {}  # A classic graph adjacency list for easy connectivity checks

    # Add a vertex to the graph. Ensures that a vertex is not placed on top of a previous vertex
    def add_vertex(self, location: Tuple[int, int]):
        for vertex_uid in self.vertices:
            if self.vertices[vertex_uid].x == location[0] and self.vertices[vertex_uid].y == location[1]:
                raise RuntimeError("Vertex already at (" + str(location[0]) + ", " + str(location[1]) + ") in graph")
        new_vertex = Vertex(location[0], location[1], self._vertex_uid)
        self._vertex_uid += 1
        self.vertices[new_vertex.uid] = new_vertex
        self.adjacency_list[new_vertex.uid] = []

    # Create an Edge connecting two vertices and note the connection in the adjacency list. Return the uid of the
    # Edge that was just created
    def connect_vertices(self, vertex1: Vertex, vertex2: Vertex, edge_uid: int = None):
        if edge_uid is None:
            new_edge = Edge(vertex1, vertex2, self._edge_uid)
            self._edge_uid += 1
        # For when an Edge is being replaced (like after removal in is_bridge()
        else:
            new_edge = Edge(vertex1, vertex2, edge_uid)
        self.edges[new_edge.uid] = new_edge
        self.adjacency_list[vertex1.uid].append(vertex2.uid)
        self.adjacency_list[vertex2.uid].append(vertex1.uid)
        return new_edge.uid

    # delete the Edge connecting two vertices
    def disconnect_edge(self, edge_uid: int):
        edge = self.edges[edge_uid]
        vertex1 = edge.v1
        vertex2 = edge.v2
        self.adjacency_list[vertex1.uid].remove(vertex2.uid)
        self.adjacency_list[vertex2.uid].remove(vertex1.uid)
        if edge_uid in self.edges:
            del self.edges[edge_uid]
        else:
            raise RuntimeError("You goofed on the key for an Edge removal.")

    # Return a list of tuples, with (vertex_uid, vertex_position)
    def get_vertex_position_list(self):
        vertex_uid_list = []
        vertex_position_list = []
        for vertex_uid in self.vertices:
            vertex_uid_list.append(vertex_uid)
            vertex_position_list.append((self.vertices[vertex_uid].x, self.vertices[vertex_uid].y))
        return [(vertex_uid_list[it], vertex_position_list[it]) for it in range(0, len(vertex_uid_list))]

    # Reference: https://www.geeksforgeeks.org/check-removing-given-edge-disconnects-given-graph/
    # Return True if the graph is connected; otherwise, False
    def is_connected(self):
        # Make the visited list and do a DFS
        visited = {}
        stack = [self.vertices[0].uid]
        for vertex_uid in self.vertices:
            visited[vertex_uid] = False
        # vertices to (but not including) 0 (step by -1
        while stack:
            vertex_uid = stack[-1]
            if not visited[vertex_uid]:
                visited[vertex_uid] = True
                stack.pop()
                for connected_vertex_uid in self.adjacency_list[vertex_uid]:
                    stack.append(connected_vertex_uid)
            else:
                stack.pop()

        # True if all vertices reachable from the first, otherwise False
        return all(list(visited[vertex_uid] for vertex_uid in visited))

    # Indicates is an edge_uid describes an edge that, when removed, will make the board unconnected
    def is_bridge(self, edge_uid):
        # Remove the Edge
        n1 = self.edges[edge_uid].v1
        n2 = self.edges[edge_uid].v2
        self.disconnect_edge(edge_uid)

        # Check if the graph is still connected
        connected = self.is_connected()

        # Put the Edge back
        self.connect_vertices(n1, n2, edge_uid)

        # Indicate if that Edge removal led to an unconnected board
        return not connected

    # Return a list of all vertex connections to be made as a pseudo-adjacency list, but with each connection appearing
    # only once (i.e. if Vertex 1 is connected to Vertex 2, Vertex 2 won't show as also being connected to Vertex 1)
    def get_voronoi_diagram_ridge_lines(self):
        # Someone else does all the fancy math for me
        vertex_position_list = self.get_vertex_position_list()
        voronoi = Voronoi(numpy.array([vertex_tuple[1] for vertex_tuple in self.get_vertex_position_list()]))

        # Storage variable
        vertex_connections = {}
        for vertex_uid in self.vertices:
            vertex_connections[self.vertices[vertex_uid].uid] = []  # Seems redundant, but I just want to be safe here

        # Dump the ridge points array into the same format as used in the Delaunay case
        for pair in voronoi.ridge_points:
            # Use the UIDs from the vertex_position_dict just in case UIDs got scrambled and aren't in order
            vertex_connections[vertex_position_list[pair[0]][0]].append(vertex_position_list[pair[1]][0])

        # This **ISN'T** twice as large as the set of all connections. It contains only one element of each list in each
        # key for each connection.
        return vertex_connections
