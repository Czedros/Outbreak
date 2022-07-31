
class Play:
    """
    a class to descripe a Play (a move) for either a player or zombie
    zombie has extra paraemters for its movement
    """
    def __init__(self, row, col, player, ZId = None, Zmove = None ):
        self.row = row
        self.col = col
        self.player = player
        self.ZId = ZId
        self.Zmove = Zmove
    def __hash__(self):
       return hash(str(self.row) + "," + str(self.col))