from Core.Vertex import Vertex
from Ants.Base import Base
from typing import Tuple
from typing import Dict
from typing import List
from Ants.BoardTypes import AntBoard


class Team:
    """
        This is a team that will exist on an AntBoard. It manages the positions and decisions of a playable set of
        elements in an ant game.
    """

    def __init__(self, uid: int, color: Tuple[int, int, int], board: AntBoard):
        """
        Constructor for Team class.

        Args:
            uid: Team UID
            color: A 3-int tuple that describes the color of the team as RGB values
            board: The board on which the Team exists
        """

        # Team UID
        self.uid: int = uid

        # Team color, represented as a tuple of 0-255 RGB values
        self.color: Tuple[int, int, int] = color

        # The game Graph
        self.board: AntBoard = board

        # A dict of the vertices controlled by the Team
        self.controlled_vertices: Dict[int, Vertex] = {}

        # A dict of the vertex UIDs adjacent to those controlled by the team
        self.adjacent_vertices: Dict[int, List[int]] = {}

        # A dict of the Bases that the Team operates on top of each controlled Vertex
        self.bases: Dict[int, Base] = {}

    def add_vertex(self, vertex: Vertex):
        """
        Add a Vertex to the dict of controlled vertices of this Team

        Args:
            vertex: The Vertex to be added to the dict of controlled Vertices
        """

        if vertex.uid in self.controlled_vertices:
            raise RuntimeError("add_vertex Error: Vertex " + str(vertex.uid) + " already controlled by Team " + str(
                self.uid))

        # Add the vertex to the list of controlled vertices for the Team
        self.controlled_vertices[vertex.uid] = vertex

        # Add the adjacency list of the new vertex to the dict of adjacent vertices
        self.adjacent_vertices[vertex.uid] = self.board.adjacency_list[vertex.uid]

        # Add a new Core at the vertex
        self.bases[vertex.uid] = Base()

    def remove_vertex(self, vertex):
        """
        Remove a Vertex fom the dict of the controlled vertices of this Team
        This also removes the Core from self.bases indiscriminately. Use with caution, as the Core will be removed
        completely and left to garbage collection (boy howdy, unless I goof on references somewhere).

        Args:
            vertex: The Vertex to remove from the dict of controlled Vertices
        """

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
            # remove the Core from bases
            try:
                del self.bases[vertex.uid]
            except KeyError:
                print("No Core found in Team " + str(self.uid) + " for vertex " + str(vertex.uid))

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
            # Remove the Core from bases
            try:
                del self.bases[vertex]
            except KeyError:
                print("No Core found in Team " + str(self.uid) + " for vertex " + str(vertex))
        else:
            raise RuntimeError("Vertex to remove not given as a Vertex object or as a Vertex uid [int]")

    def update(self):
        """
        Updates the Team by updating all elements thereof.
        """

        # Update each Core in the Team
        for vertex_id in self.bases:
            self.bases[vertex_id].update()
