class Move:
    def __init__(self, sr, sc, er, ec, promotion=None, castle = False):
        self.sr = sr
        self.sc = sc
        self.er = er
        self.ec = ec
        self.promotion = promotion
        self.castle = castle