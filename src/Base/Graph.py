from Base.Edge import *
from Base.Vertex import *
from typing import Tuple
import numpy
from scipy.spatial import Voronoi
import math


class Graph:
    """
    A class that describes a Graph in the mathematical sense of the word. A Graph contains Vertices which connect to
    other Vertices along Edges. This class is the parent of the Boards used in the Ant game, as it provides the base
    storage of the "map" on which the game is played.
    """

    def __init__(self):
        """
        The constructor for Graph class.
        """

        # Graph Properties
        self._vertex_uid = 0
        self._edge_uid = 0

        # A dict of the Vertices of the graph, keyed by their UIDs
        # vertex.uid : Vertex
        self.vertices = {}

        # A dict of the Edges of the graph, keyed by their UIDs
        # edge.uid : Edge
        self.edges = {}

        # A dict of lists of the adjacent vertex UIDs of each Vertex, keyed by the vertex UID
        # vertex.uid : [adjacent vertex UIDs]
        self.adjacency_list = {}  # A classic graph adjacency list for easy connectivity checks

        # Things to help out the Voronoi Generation
        self.center = Vertex(0, 0, -1)  # The average of all vertices x and y values, UID of -1

        # TODO We'll come back to this later perhaps. This would make looking for edge overlaps much easier and
        #  faster, but would require a dynamic resizing of the backing grid AND determining how granular we want to
        #  be with it.
        # # Backing class for objects within the Graph storage grid
        # class GridSquare:
        #     def __init__(self):
        #         self.edge_uids = []
        #         self.node_uids = []
        #
        # # Backing grid for storing locations of Graph elements in a more easily-searchable location
        # self.grid = [[GridSquare() for _ in range(10)] for _ in range(10)]  # Initialize to 10x10 grid.

    def __str__(self):
        """
        The tostring method of the Graph class.

        Returns:
            A sting representation of the Graph object.
        """

        out_str = ""
        for vertex_uid in self.vertices:
            out_str += str(self.vertices[vertex_uid]) + "\n"
        for edge_uid in self.edges:
            out_str += str(self.edges[edge_uid]) + "\n"
        return out_str

    def add_vertex(self, location: Tuple[int, int], vertex_preset_uid: int = None):
        """
        Adds a Vertex to the Graph. Ensures that a Vertex is not placed on top of an already-existing Vertex.

        Args:
            location: A two-value Tuple containing the X- and Y-coordinates of the Vertex to be added.
            vertex_preset_uid: An optional argument for when the Vertex UID is known. Use sparingly; this is
            probably best used when a Vertex has just been removed and is being re-added

        Returns:
            The UID of the Vertex that was just added to the Graph.
        """

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

        # Add the vertex to the graph
        self.vertices[new_vertex.uid] = new_vertex
        self.adjacency_list[new_vertex.uid] = []

        # Update the center of the graph
        self.center.x += (new_vertex.x - self.center.x) / len(self.vertices)
        self.center.y += (new_vertex.y - self.center.y) / len(self.vertices)

        return new_vertex.uid

    def connect_vertices(self, vertex1: Vertex, vertex2: Vertex, edge_uid: int = None):
        """
        Connects two Vertices in the Graph with an Edge. The order of the Vertices has been designed to not matter.

        Args:
            vertex1: One of the Vertices to be connected.
            vertex2: The other Vertex to be connected.
            edge_uid: An optional argument for when the Edge UID is known. Use sparingly; this is probably best used
            when a Vertex has just been removed and is being re-added.

        Returns:
            The UID of the newly-created Edge object connecting the two specified Vertices.
        """

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

    def disconnect_edge(self, edge_uid: int):
        """
        Disconnects an Edge on the graph, removing all references of the connection from the Graph, including the
        Edge object itself and the entries in the Graph adjacency list.

        Args:
            edge_uid: The UID of the Edge to be removed.

        Returns:
            A boolean indicating that the execution succeeded.
        """

        edge = self.edges[edge_uid]
        vertex1 = edge.v1
        vertex2 = edge.v2
        self.adjacency_list[vertex1.uid].remove(vertex2.uid)
        self.adjacency_list[vertex2.uid].remove(vertex1.uid)
        if edge_uid in self.edges:
            del self.edges[edge_uid]
            return True
        else:
            raise RuntimeError("You goofed on the key for an Edge removal.")

    def get_vertex_position_dict(self):
        """
        Generates and returns a dict of the vertex positions within the Graph.

        Returns:
            A vertex position dict with the format {vertex_uid: vertex (x, y) position tuple}
        """

        vertex_position_dict= {}
        for vertex_uid in self.vertices:
            vertex_position_dict[vertex_uid] = (self.vertices[vertex_uid].x, self.vertices[vertex_uid].y)
        return vertex_position_dict

    def get_boundary_points(self):
        """
        Returns the outer-most X- and Y-coordinates of the graph in the form of a bottom-left and a top-right
        position tuple. These positions do not represent the outermost Vertices, but instead describe the smallest
        bounding box that can be drawn around the Graph.

        Returns:
            A tuple of two tuples, the first containing the (x, y)-coordinates of the bottom-left point of the
            bounding box of the Graph and the second containing the (x, y)-coordinates of the top-left point of the
            same box.
        """

        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        for vertex_uid in self.vertices:
            # Adjust x-values
            if self.vertices[vertex_uid].x > x_max:
                x_max = self.vertices[vertex_uid].x
            elif self.vertices[vertex_uid].x < x_min:
                x_min = self.vertices[vertex_uid].x

            # Adjust y-values
            if self.vertices[vertex_uid].y > y_max:
                y_max = self.vertices[vertex_uid].y
            elif self.vertices[vertex_uid].y < y_min:
                y_min = self.vertices[vertex_uid].y

        return (x_min, y_min), (x_max, y_max)

    def is_connected(self):
        """
        Determines if the Graph is connected, i.e. if all points within the Graph can be reached from all other points.
        Reference: https://www.geeksforgeeks.org/check-removing-given-edge-disconnects-given-graph/

        Returns:
            A boolean value describing if the Graph is connected (True) or not (False).
        """

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

    def is_bridge(self, edge_uid):
        """
        Determines is an Edge is a "bridge"; that is, if removing the Edge would cause the Graph to become disconnected.

        Args:
            edge_uid: The UID of the Edge to be evaluated for bridge-status.

        Returns:
            A boolean describing if the Edge is a bridge (True) or not (False).
        """

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

    def get_voronoi_diagram_ridge_lines(self):
        """
            Return a list of all vertex connections to be made as a pseudo-adjacency list, but with each connection
            appearing only once (i.e. if Vertex 1 is connected to Vertex 2, Vertex 2 won't show as also being
            connected to Vertex 1)

        Returns:
            A list of all Vertex connections to be made to
        """

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
        """
        This is... mayhem. TODO All of it.

        Returns:
            Something. I'm not sure yet. Something describing the Voronoi regions of the Graph.
        """

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
        for position_tuple in voronoi.vertices:
            voronoi_graph.add_vertex((position_tuple[0], position_tuple[1]))

        # Add edges to Voronoi Graph
        # TODO This adds duplicate vertices at the edge when creating infinite vertices IF two of the lines WOULD
        #  meet at an edge. Maybe I need to make a look-up for that.
        # TODO This also goofs and always assumes that the midpoint will be between the finite vertex and the
        #  infinite one, which is not always the case. I think this is a situation where I compare the angles between
        #  the line from midpoint to vertex and the opposite of that angle to the angle to the center of mass and
        #  pick the lesser one.
        # TODO This doesn't address the situation where the angle is perfectly straight between them; for
        #  example, when you only have two points. Hmmmmm. NO WAIT in that case they're BOTH infinite yikes.
        # TODO I should really write my own Voronoi algorithm, but that will take SO LONG.
        for simplex, ridge_points in zip(voronoi.ridge_vertices, voronoi.ridge_points):  # These are the vertices
            # that are at the end of each ridge and the points that the ridge runs between

            if all([vertex >= 0 for vertex in simplex]):  # Internal Edge
                # If the vertices both exist (i.e., this isn't an infinite edge), connect them in the Voronoi graph
                voronoi_graph.connect_vertices(voronoi_graph.vertices[simplex[0]], voronoi_graph.vertices[simplex[1]])
                # Then, add those Voronoi edges to the graph vertex region sets. We can add them indiscriminately
                # without checking if they already exist in the set because a set is by definition a unique list
                vertex_voronoi_regions[ridge_points[0]].add(voronoi_graph.vertices[simplex[0]])
                vertex_voronoi_regions[ridge_points[0]].add(voronoi_graph.vertices[simplex[1]])
                vertex_voronoi_regions[ridge_points[1]].add(voronoi_graph.vertices[simplex[0]])
                vertex_voronoi_regions[ridge_points[1]].add(voronoi_graph.vertices[simplex[1]])

            # If one of the vertices is -1, we need to do some line math to find the terminus of that edge
            else:  # Infinite Edge
                # Get Voronoi Graph boundaries
                voronoi_boundaries = voronoi_graph.get_boundary_points()

                # The point that exists in the Voronoi Graph. There will only ever be two, so using the list
                # comprehension to grab the non-negative one works just fine
                finite_point_voronoi_vertex_uid = [simplex_value for simplex_value in simplex if simplex_value >= 0][0]
                finite_vertex = voronoi_graph.vertices[finite_point_voronoi_vertex_uid]

                # Definitely bad, can't account for infinity
                # tangent_dx = self.vertices[vertex_uid_list[ridge_points[1]]].x \
                #              - self.vertices[vertex_uid_list[ridge_points[0]]].x
                # tangent_dy = self.vertices[vertex_uid_list[ridge_points[1]]].y \
                #              - self.vertices[vertex_uid_list[ridge_points[0]]].y
                # tangent_slope = tangent_dy / tangent_dx
                # if tangent_slope == 0:
                #     normal_slope = "infinity"
                # else:
                #     normal_slope = -1 / tangent_slope

                # Get the mid-point of the two ridge points
                midpoint_x = (self.vertices[vertex_uid_list[ridge_points[1]]].x + self.vertices[vertex_uid_list[
                    ridge_points[0]]].x) / 2
                midpoint_y = (self.vertices[vertex_uid_list[ridge_points[1]]].y + self.vertices[vertex_uid_list[
                    ridge_points[0]]].y) / 2

                # This is self-documenting, but it serves as our way of determining which case we need to use to find
                # the edge of the voronoi region
                # Account for infinite slopes
                if finite_vertex.x - midpoint_x == 0:
                    # Upward line from the midpoint to the Voronoi vertex
                    if finite_vertex.y - midpoint_y > 0:
                        theta_from_x_axis_to_real_vertex_from_midpoint = math.pi / 2
                    # Downward line from the midpoint to the Voronoi vertex
                    else:
                        theta_from_x_axis_to_real_vertex_from_midpoint = 3 * math.pi / 2
                else:
                    theta_from_x_axis_to_real_vertex_from_midpoint = math.atan((finite_vertex.y - midpoint_y)
                                                                               / (finite_vertex.x - midpoint_x))
                theta_from_x_to_inf_point = 2 * math.pi - theta_from_x_axis_to_real_vertex_from_midpoint

                # Handle lines with no angle
                # Case for a straight line leading to the right from the finite vertex
                if theta_from_x_to_inf_point == 0:
                    end_point = (voronoi_boundaries[1][0], finite_vertex.y)  # The x-value of the top-right of the
                    # bounds
                # Case for a straight line leading to the left from the finite vertex
                elif theta_from_x_to_inf_point == math.pi:
                    end_point = (voronoi_boundaries[0][0], finite_vertex.y)  # The x-value of the bottom-left of the
                    # bounds
                # Case for a straight line leading up from the finite vertex
                elif theta_from_x_to_inf_point == math.pi / 2:
                    end_point = (finite_vertex.x, voronoi_boundaries[1][1])  # The y-value of the top-right of the
                    # bounds
                # Case for a straight line leading down from the finite vertex
                elif theta_from_x_to_inf_point == 3 * math.pi / 2:
                    end_point = (finite_vertex.x, voronoi_boundaries[0][1])  # The y-value of the bottom left of the
                    # bounds

                # Handle lines with an angle
                # These lines will hit either the top or the right of the Voronoi region
                if 0 < theta_from_x_to_inf_point < math.pi / 2:
                    # Intersection with the right
                    if theta_from_x_to_inf_point < math.atan((voronoi_boundaries[1][1] - finite_vertex.y) /
                                                             (voronoi_boundaries[1][0] - finite_vertex.x)):
                        dx = voronoi_boundaries[1][0] - finite_vertex.x
                        dy = dx * math.sin(theta_from_x_to_inf_point)
                        end_point = (voronoi_boundaries[1][0], finite_vertex.y + dy)
                    # Intersection with the top
                    elif theta_from_x_to_inf_point > math.atan((voronoi_boundaries[1][1] - finite_vertex.y) /
                                                               (voronoi_boundaries[1][0] - finite_vertex.x)):
                        dy = voronoi_boundaries[1][1] - finite_vertex.y
                        dx = dy / math.sin(theta_from_x_to_inf_point)
                        end_point = (finite_vertex.x + dx, voronoi_boundaries[1][1])
                    # Intersection with the top right point
                    else:
                        end_point = voronoi_boundaries[1]

                # These lines will hit either the top or the left
                elif math.pi / 2 < theta_from_x_to_inf_point < math.pi:
                    # Intersection with the top
                    if theta_from_x_to_inf_point < math.atan((voronoi_boundaries[1][1] - finite_vertex.y) /
                                                             (voronoi_boundaries[0][0] - finite_vertex.x)):
                        dy = voronoi_boundaries[1][1] - finite_vertex.y
                        dx = dy / math.sin(math.pi - theta_from_x_to_inf_point)
                        end_point = (finite_vertex.x - dx, voronoi_boundaries[1][1])
                    # Intersection with the left
                    elif theta_from_x_to_inf_point > math.atan((voronoi_boundaries[1][1] - finite_vertex.y) /
                                                               (voronoi_boundaries[0][0] - finite_vertex.x)):
                        dx = finite_vertex.x - voronoi_boundaries[0][0]
                        dy = dx * math.sin(math.pi - theta_from_x_to_inf_point)
                        end_point = (voronoi_boundaries[0][0], finite_vertex.y + dy)
                    # Intersection with the top left point
                    else:
                        end_point = (voronoi_boundaries[0][0], voronoi_boundaries[1][1])

                # These lines will hit either the left or the bottom
                elif math.pi < theta_from_x_to_inf_point < 3 * math.pi / 2:
                    # Intersection with the left
                    if theta_from_x_to_inf_point < math.atan((voronoi_boundaries[0][1] - finite_vertex.y) /
                                                             (voronoi_boundaries[0][0] - finite_vertex.x)):
                        dx = finite_vertex.x - voronoi_boundaries[0][0]
                        dy = dx * math.sin(theta_from_x_to_inf_point - math.pi)
                        end_point = (voronoi_boundaries[0][0], finite_vertex.y - dy)
                    # Intersection with the bottom
                    elif theta_from_x_to_inf_point > math.atan((voronoi_boundaries[0][1] - finite_vertex.y) /
                                                               (voronoi_boundaries[0][0] - finite_vertex.x)):
                        dy = finite_vertex.y - voronoi_boundaries[0][1]
                        dx = dy / math.sin(3 * math.pi / 2 - theta_from_x_to_inf_point)
                        end_point = (finite_vertex.x - dx, voronoi_boundaries[0][1])
                    # Intersection with the bottom left point
                    else:
                        end_point = voronoi_boundaries[0]

                # These lines will hit either the bottom or the right
                elif 3 * math.pi / 2 < theta_from_x_to_inf_point < 2 * math.pi:
                    # Intersection with the bottom
                    if theta_from_x_to_inf_point < math.atan((voronoi_boundaries[0][1] - finite_vertex.y) /
                                                             (voronoi_boundaries[1][0] - finite_vertex.x)):
                        dy = finite_vertex.y - voronoi_boundaries[0][1]
                        dx = dy / math.sin(theta_from_x_to_inf_point - 3 * math.pi / 2)
                        end_point = (finite_vertex.x + dx, voronoi_boundaries[0][1])
                    # Intersection with the right
                    elif theta_from_x_to_inf_point > math.atan((voronoi_boundaries[0][1] - finite_vertex.y) /
                                                               (voronoi_boundaries[1][0] - finite_vertex.x)):
                        dx = voronoi_boundaries[1][0] - finite_vertex.x
                        dy = dx * math.sin(2 * math.pi - theta_from_x_to_inf_point)
                        end_point = (voronoi_boundaries[1][0], finite_vertex.y - dy)
                    # Intersection with the bottom right point
                    else:
                        end_point = (voronoi_boundaries[1][0], voronoi_boundaries[0][1])

                else:
                    print("Dude what")
                    end_point = ("holy", "Crap")  # I'm tired, forgive me.
                    raise RuntimeError("What")

                # Create the vertex
                new_vertex_uid = voronoi_graph.add_vertex(end_point)

                # Connect the vertex to the finite vertex
                voronoi_graph.connect_vertices(finite_vertex, voronoi_graph.vertices[new_vertex_uid])

                # Add each vertex to the regions
                vertex_voronoi_regions[ridge_points[0]].add(finite_vertex)
                vertex_voronoi_regions[ridge_points[0]].add(voronoi_graph.vertices[new_vertex_uid])
                vertex_voronoi_regions[ridge_points[1]].add(finite_vertex)
                vertex_voronoi_regions[ridge_points[1]].add(voronoi_graph.vertices[new_vertex_uid])

        # Close off the regions on the edge of the Voronoi regions TODO <-- that
