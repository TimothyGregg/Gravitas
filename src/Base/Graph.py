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

    def __str__(self):
        out_str = ""
        for vertex_uid in self.vertices:
            out_str += str(self.vertices[vertex_uid]) + "\n"
        for edge_uid in self.edges:
            out_str += str(self.edges[edge_uid]) + "\n"
        return out_str

    # Add a vertex to the graph. Ensures that a vertex is not placed on top of a previous vertex. Return the uid of
    # the Vertex that was just created
    def add_vertex(self, location: Tuple[int, int], vertex_preset_uid: int = None):
        for vertex_uid in self.vertices:
            if self.vertices[vertex_uid].x == location[0] and self.vertices[vertex_uid].y == location[1]:
                raise RuntimeError("Vertex already at (" + str(location[0]) + ", " + str(location[1]) + ") in graph")
        # When a vertex is being added, ignorant of a UID
        if vertex_preset_uid is None:
            new_vertex = Vertex(location[0], location[1], self._vertex_uid)
            self._vertex_uid += 1
        # For when a vertex needs to be added with a specific UID
        else:
            if vertex_preset_uid in self.vertices:
                raise RuntimeError("Overlapping vertex UIDs attempted to be assigned")
            new_vertex = Vertex(location[0], location[1], vertex_preset_uid)
        self.vertices[new_vertex.uid] = new_vertex
        self.adjacency_list[new_vertex.uid] = []
        return new_vertex.uid

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

    # Return a dict, with {vertex_uid: vertex (x, y) position tuple}
    def get_vertex_position_dict(self):
        vertex_position_dict= {}
        for vertex_uid in self.vertices:
            vertex_position_dict[vertex_uid] = (self.vertices[vertex_uid].x, self.vertices[vertex_uid].y)
        return vertex_position_dict

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
        vertex_position_dict = self.get_vertex_position_dict()
        # Create this list for reference down in the translation from voronoi ridge_points to UIDs to ensure that
        # even if the UIDs aren't in order in the dict, we keep them consistent
        vertex_uid_list = [vertex_uid for vertex_uid in vertex_position_dict]
        voronoi = Voronoi(numpy.array([vertex_position_dict[vertex_uid] for vertex_uid in vertex_position_dict]))

        # Storage variable
        vertex_connections = {}
        for vertex_uid in self.vertices:
            vertex_connections[self.vertices[vertex_uid].uid] = []  # Seems redundant, but I just want to be safe here

        # Dump the ridge points array into the same format as used in the Delaunay case
        for pair in voronoi.ridge_points:
            # Use the UIDs from the vertex_position_dict just in case UIDs got scrambled and aren't in order
            # Add the UID of the second point (pair[1]) to the connections of the first UID (pair[0])
            vertex_connections[vertex_uid_list[pair[0]]].append(vertex_uid_list[pair[1]])

        # This **ISN'T** twice as large as the set of all connections. It contains only one element of each list in each
        # key for each connection.
        return vertex_connections

    def get_voronoi_regions(self):
        # Once again, someone else does all the fancy math for me
        vertex_position_dict = self.get_vertex_position_dict()
        voronoi = Voronoi(numpy.array([vertex_position_dict[vertex_uid] for vertex_uid in vertex_position_dict]))

        # Create this list for reference in the translation from voronoi ridge_points to UIDs to ensure that
        # even if the UIDs aren't in order in the dict, we keep them consistent
        vertex_uid_list = [vertex_uid for vertex_uid in vertex_position_dict]
        # Storage for the relevant [vertices of a *region*] of a given Vertex in the Graph
        vertex_voronoi_regions = {vertex_uid: set([]) for vertex_uid in vertex_uid_list}  # This contains sets of
        # vertices in the Voronoi Graph (sets will not add an element again if it already exists)

        # Create a Voronoi Graph here:
        voronoi_graph = Graph()

        # Add vertices to Voronoi Graph
        _voronoi_graph_vertex_uid = 0
        for position_tuple in voronoi.vertices:
            voronoi_graph.add_vertex((position_tuple[0], position_tuple[1]), _voronoi_graph_vertex_uid)
            _voronoi_graph_vertex_uid += 1

        # Add edges to Voronoi Graph
        for simplex, ridge_points in zip(voronoi.ridge_vertices, voronoi.ridge_points):  # These are the vertices
            # that are at the end of each ridge and the points that the ridge runs between

            if all([vertex >= 0 for vertex in simplex]):  # Internal Edge
                # If the vertices both exist (i.e., this isn't an infinite edge), connect them in the Voronoi graph
                voronoi_graph.connect_vertices(voronoi_graph.vertices[simplex[0]], voronoi_graph.vertices[simplex[1]])
                # Then, add those Voronoi edges to the graph vertex region sets. We can add them indiscriminately
                # without checking if they already exist in the set because a set auto-makes a unique list
                vertex_voronoi_regions[ridge_points[0]].add(voronoi_graph.vertices[simplex[0]])
                vertex_voronoi_regions[ridge_points[0]].add(voronoi_graph.vertices[simplex[1]])
                vertex_voronoi_regions[ridge_points[1]].add(voronoi_graph.vertices[simplex[0]])
                vertex_voronoi_regions[ridge_points[1]].add(voronoi_graph.vertices[simplex[1]])

            # If one of the vertices is -1, we need to do some line math to find the terminus of that edge
            # TODO find the minimum and maximum graph boundary intercepts and use them to define the edge regions
            else:  # Infinite Edge
                # TODO here we need to add in a formula for calculating the intercept of the line with one of the
                #  boundaries of the graph and then add that as a point to the vertex_voronoi_regions

                # The point that exists in the Voronoi Graph. There will only ever be two, so using the list
                # comprehension to grab the non-negative one works just fine
                finite_point = [simplex_value for simplex_value in simplex if simplex_value > 0]
                tangent_dx = self.vertices[vertex_uid_list[ridge_points[1]]].x \
                             - self.vertices[vertex_uid_list[ridge_points[0]]].x
                tangent_dy = self.vertices[vertex_uid_list[ridge_points[1]]].y \
                             - self.vertices[vertex_uid_list[ridge_points[0]]].y

    # The default update method. Returns a value describing if the Graph was able to update successfully.
    def update(self):
        return True
