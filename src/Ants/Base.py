from typing import List


# TODO Type-hint
class Base:
    """
    Core objects serve as the base from which a Team will operate on top of a Vertex. TODO: Expand on this definition when it becomes applicable.
    """

    def __init__(self, uid: int):
        """
        Constructor for the Core class.
        """

        # Permanent Core Characteristics
        self.uid: int = uid
        self.connections: List[Connection] = []

        # Mutable Core Characteristics
        self.population: int = 1

    # This has a type-hint of the same class, so we use apostrophes to made a "Forward Reference"
    # Info at https://www.youtube.com/watch?v=AJsrxBkV3kc
    def connect(self, other: 'Base'):
        """
        Build a connection FROM this Base TO another Base

        Args:
            other: The other Base to connect this one to
        """

        self.connections.append(Connection(other))

    def update(self):
        """
        Update the Core.
        """

        pass


class Connection:
    """
    Storage class for inter-node connections. These are strictly one-way (i.e. from this Base to the other Base)
    """

    def __init__(self, other: Base):
        """
        Connection Constructor

        Args:
            other: The Base that this connection leads to
        """

        self.other: Base = other
