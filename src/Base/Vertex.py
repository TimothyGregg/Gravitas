class Vertex:
    """
    A Vertex class for use in Graph objects to store positions within the Graph.
    """

    def __init__(self, x, y, uid: int):
        """
        The constructor for the Vertex class.

        Args:
            x: The x-coordinate of the Vertex
            y: The y-coordinate of the Vertex
            uid: The UID of the Vertex
        """

        # Set member variables
        self.x = x
        self.y = y
        # Set unique ID
        self.uid = uid

    def __str__(self):
        """
        A to_string method for the Vertex class.

        Returns:
            A string representation of the Vertex.
        """

        return "Vertex " + str(self.uid) + " @ [" + str(self.x) + ", " + str(self.y) + "]"
