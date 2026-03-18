class Board:
    def __init__(self):
        self.moveWhite = True
        self.en_passant = None
        self.wck = False
        self.wcq = False
        self.bck = False
        self.bcq = False #castle states

        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]  

    def clone(self):
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        new_board.moveWhite = self.moveWhite
        new_board.en_passant = self.en_passant
        return new_board

    def castle(self, move):
        if self.moveWhite:
            if move.ec == 6: #white king side castle
                self.board[7][6] = 'K'
                self.board[7][5] = 'R'
                self.board[7][4] = '-'
                self.board[7][7] = '-'
            elif move.ec == 2:
                self.board[7][2] = 'K'
                self.board[7][3] = 'R'
                self.board[7][0] = '-'
                self.board[7][4] = '-'
            self.wck = False
            self.wcq = False #White can not castle after castling
        else:
            if move.ec == 6:  # Black king side castle
                self.board[0][6] = 'k'
                self.board[0][5] = 'r'
                self.board[0][4] = '-'
                self.board[0][7] = '-'
            elif move.ec == 2:
                self.board[0][2] = 'k'
                self.board[0][3] = 'r'
                self.board[0][4] = '-'
                self.board[0][0] = '-'
            self.bck = False
            self.bcq = False  # Black can not castle after castling

    def stop_castle(self, move):
        piece = self.board[move.sr][move.sc]
        if (self.wck or self.wcq) and piece == 'K':
            self.wck = False
            self.wcq = False
        elif (self.bck or self.bcq) and piece == 'k':
            self.bck = False
            self.bcq = False #if king moves the color can no longer castle
        elif piece == 'R' and move.sr == 7 and move.sc == 0:
            self.wcq = False
        elif piece == 'r' and move.sr == 0 and move.sc == 0:
            self.bcq = False
        elif piece == 'R' and move.sr == 7 and move.sc == 7:
            self.wck = False
        elif piece == 'r' and move.sr == 0 and move.sc == 7:
            self.bck = False #if we move a rook and we can castle for said side we cant castle anymore
        #if a rook gets captued we can't castle on said side
        if self.bcq and (move.er == 0 and move.ec == 0):
            self.bcq = False
        elif self.bck and (move.er == 0 and move.ec == 7):
            self.bck = False
        elif self.wck and (move.er == 7 and move.ec == 7):
            self.wck = False
        elif self.wcq and (move.er == 7 and move.ec == 0):
            self.wcq = False


    def make_move(self, move):
        if move.castle:
            self.castle(move)
            self.moveWhite = not self.moveWhite
            return
        self.stop_castle(move)
        piece = self.board[move.sr][move.sc]
        old_ep = self.en_passant
        self.en_passant = None
        if piece.lower() == 'p' and old_ep is not None:
            if (move.er, move.ec) == old_ep and move.sc != move.ec:
                captured_row = move.sr
                captured_col = move.ec
                self.board[captured_row][captured_col] = '-'

        self.board[move.sr][move.sc] = '-'
        updated_piece = piece
        if piece.lower() == 'p' and move.promotion is not None:
            updated_piece = move.promotion if piece.islower() else move.promotion.upper()

        self.board[move.er][move.ec] = updated_piece


        if piece.lower() == 'p' and abs(move.er - move.sr) == 2:
            en_p_row = (move.sr + move.er) // 2
            self.en_passant =(en_p_row, move.sc)

        self.moveWhite = not self.moveWhite
    def print_board(self):
        print("  a b c d e f g h")
        for row in range(8):
            print(8 - row, end=" ")
            for col in range(8):
                print(self.board[row][col], end=" ")
            print(8 - row)
        print("  a b c d e f g h")

    def locate_king(self, white = True):
        king_char = 'K' if white else 'k'
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king_char:
                    return row, col
        return None #no king

    def is_in_check(self, white):
        kr, kc = self.locate_king(white) #King row and king colum
        return self.is_square_attacked(kr, kc, not white)

    def is_square_attacked(self, r, c, attacker_white):
        if attacker_white:
            pawn_sources = [(r + 1, c - 1), (r + 1, c + 1)]
            for pr, pc in pawn_sources:
                if 0 <= pr < 8 and 0 <= pc < 8 and self.board[pr][pc] == 'P':
                    return True
        else:
            pawn_sources = [(r - 1, c - 1), (r - 1, c + 1)]
            for pr, pc in pawn_sources:
                if 0 <= pr < 8 and 0 <= pc < 8 and self.board[pr][pc] == 'p':
                    return True
        knight_jumps = [(-2, -1), (-2, 1),(-1, -2), (-1, 2),(1, -2), (1, 2),(2, -1), (2, 1)]
        for dr, dc in knight_jumps:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                p = self.board[nr][nc]
                if attacker_white and p == 'N':
                    return True
                if not attacker_white and p == 'n':
                    return True

        king_moves = [(-1, -1), (-1,  0), (-1,  1),( 0, -1), ( 0,  1),( 1, -1), ( 1,  0), ( 1,  1)]
        for dr, dc in king_moves:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                p = self.board[nr][nc]
                if attacker_white and p == 'K':
                    return True
                if not attacker_white and p == 'k':
                    return True

        rook_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in rook_moves:
            nr = r + dr
            nc = c + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                p = self.board[nr][nc]
                if p!='-':
                    if attacker_white:
                        if p in ('R', 'Q'):
                            return True
                    else:
                        if p in ('r', 'q'):
                            return True
                    break
                nr += dr
                nc += dc

        bishop_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in bishop_moves:
            nr = r + dr
            nc = c + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                p = self.board[nr][nc]
                if p != '-':
                    if attacker_white and p in ('B', 'Q'):
                        return True
                    if not attacker_white and p in ('b', 'q'):
                        return True
                    break  # blocked
                nr += dr
                nc += dc
        return False
