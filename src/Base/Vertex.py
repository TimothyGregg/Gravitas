class Vertex:
    # _uid = 0    # The underscore is python's way of denoting "private" (even though private doesn't really exist)

    def __init__(self, x: int, y: int, uid: int):
        # Set member variables
        self.x = x
        self.y = y
        # Set unique ID, then increment the class-based unique ID count
        self.uid = uid

    def __str__(self):
        return "Vertex " + str(self.uid) + " @ [" + str(self.x) + ", " + str(self.y) + "]"
