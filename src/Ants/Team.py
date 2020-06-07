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

        # A dict of the Bases controlled by the Team
        self.controlled_bases: Dict[int, Base] = {}

    def add_base(self, base: Base):
        """
        Add a Base to the dict of controlled Bases of this Team

        Args:
            base: The Base to be added to the dict of controlled Bases
        """

        if base.uid in self.controlled_bases:
            raise RuntimeError("add_base Error: Base " + str(base.uid) + " already controlled by Team " + str(
                self.uid))

        # Add the Base to the list of controlled Bases for the Team
        self.controlled_bases[base.uid] = base

    def remove_base(self, base: Base):
        """
        Remove a Base fom the dict of the controlled Bases of this Team

        Args:
            base: The Base to remove from the dict of controlled Bases
        """

        # When given the Base to remove directly
        if type(base) == Base:
            # Remove the Base from controlled_bertices
            try:
                del self.controlled_bases[base.uid]
            except KeyError:
                print("remove_base Error: Base " + str(base.uid) + " not controlled by Team " + str(self.uid))

        # When given the Base to remove by it's uid
        elif type(base) == int:
            # Remove the Base from controlled_bertices
            try:
                del self.controlled_bases[base]
            except KeyError:
                print("remove_base Error: Base " + str(base) + " not controlled by Team " + str(self.uid))

        # When we're handed junk
        else:
            raise RuntimeError("Base to remove not given as a Base object or as a Base uid [int]")

    def update(self):
        """
        Updates the Team by updating all elements thereof.
        """

        # Update each Base in the Team
        for base_id in self.controlled_bases:
            self.controlled_bases[base_id].update()
