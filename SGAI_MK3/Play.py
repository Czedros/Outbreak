
class Play:
    """
    this is literally the coords of the move but it just needs to be hashable
    """
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __hash__(self):
       return str(self.row) + "," + str(self.col)