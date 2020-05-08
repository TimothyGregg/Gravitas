class Node:
    _uid = 0    # The underscore is python's way of denoting "private" (even though private doesn't really exist)

    def __init__(self, x: int, y: int):
        # Set member variables
        self.x = x
        self.y = y
        self.edges = []
        # Set unique ID, then increment the class-based unique ID count
        self.uid = Node._uid
        Node._uid += 1

    def __str__(self):
        return "Node " + str(self.uid) + " @ [" + str(self.x) + ", " + str(self.y) + "]"
