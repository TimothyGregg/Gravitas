from Base.Vertex import Vertex
from Ants.Node import Node
from typing import Tuple
from GraphTypes import AntGraph


# This is a team that will exist on an AntGraph. It manages the positions and decisions of a playable set of elements
# in an ant game.
class Team:
    def __init__(self, uid: int, color: Tuple[int, int, int], graph: AntGraph):
        # Team UID
        self.uid = uid

        # Team color, represented as a tuple of 0-255 RGB values
        self.color = color

        # The game Graph
        self.graph = graph

        # A dict of the vertices controlled by the Team
        # vertex.uid : Vertex
        self.controlled_vertices = {}

        # A dict of the vertices adjacent to those controlled by the team
        # vertex.uid : adjacency list for that vertex
        self.adjacent_vertices = {}

        # A dict of the Nodes that the Team operates on top of each controlled Vertex
        # vertex.uid: Base
        self.nodes = {}

    # Add a Vertex to the dict of controlled vertices of this Team
    def add_vertex(self, vertex: Vertex):
        if vertex.uid in self.controlled_vertices:
            raise RuntimeError("add_vertex Error: Vertex " + str(vertex.uid) + " already controlled by Team " + str(
                self.uid))

        # Add the vertex to the list of controlled vertices for the Team
        self.controlled_vertices[vertex.uid] = vertex

        # Add the adjacency list of the new vertex to the dict of adjacent vertices
        self.adjacent_vertices[vertex.uid] = self.graph.adjacency_list[vertex.uid]

        # Add a new Node at the vertex
        self.nodes[vertex.uid] = Node()

    # Remove a Vertex fom the dict of the controlled vertices of this Team
    # This also removes the Node from self.nodes indiscriminately. Use with caution, as the Node will be removed
    # completely and left to garbage collection (boy howdy, unless I goof on references somewhere).
    def remove_vertex(self, vertex):
        # When given the vertex to remove directly
        if type(vertex) == Vertex:
            # Remove the vertex from controlled_vertices
            try:
                del self.controlled_vertices[vertex.uid]
            except KeyError:
                print("remove_vertex Error: Vertex " + str(vertex.uid) + " not controlled by Team " + str(self.uid))
            # Remove the vertex from adjacent_vertices
            try:
                del self.adjacent_vertices[vertex.uid]
            except KeyError:
                print("remove_vertex Error: Vertex " + str(vertex.uid) + " not found in adjacency lists of Team " +
                      str(self.uid))
            # remove the Node from nodes
            try:
                del self.nodes[vertex.uid]
            except KeyError:
                print("No Node found in Team " + str(self.uid) + " for vertex " + str(vertex.uid))

        # When given the vertex to remove by it's uid
        elif type(vertex) == int:
            # Remove the vertex from controlled_vertices
            try:
                del self.controlled_vertices[vertex]
            except KeyError:
                print("remove_vertex Error: Vertex " + str(vertex.uid) + " not controlled by Team " + str(self.uid))
            try:
                del self.adjacent_vertices[vertex]
            except KeyError:
                print("remove_vertex Error: Vertex " + str(vertex) + " not found in adjacency lists of Team " +
                      str(self.uid))
            # Remove the Node from nodes
            try:
                del self.nodes[vertex]
            except KeyError:
                print("No Node found in Team " + str(self.uid) + " for vertex " + str(vertex))
        else:
            raise RuntimeError("Vertex to remove not given as a Vertex object or as a Vertex uid [int]")

