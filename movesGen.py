from Move import Move
def gen_all_moves(board):
    moves = []
    white = board.moveWhite
    for r in range(8):
        for c in range(8):
            piece = board.board[r][c]
            if piece == '-':
                continue
            if white and piece.islower():
                continue
            if not white and piece.isupper():
                continue #skip opponents pieces and no piece
            p = piece.lower()
            if p == 'p':
                pawn_moves(board, r, c, moves)
            elif p == 'n':
                knight_moves(board,r,c,moves)
            elif p == 'b':
                bishop_moves(board,r,c,moves)
            elif p == 'r':
                rook_moves(board,r,c,moves)
            elif p == 'q':
                queen_moves(board,r,c,moves)
            elif p == 'k':
                king_moves(board,r,c,moves)
    return moves

def gen_legal_moves(board):
    legal_moves = []
    castle_moves = gen_castle_moves(board)
    mover_white = board.moveWhite
    legal_moves.extend(castle_moves)#All castle moves generated are legal
    for move in gen_all_moves(board):
        board2 = board.clone()
        board2.make_move(move)

        if not board2.is_in_check(mover_white):
            legal_moves.append(move)
    return legal_moves

def pawn_moves(board, r, c, moves):
    piece = board.board[r][c]
    white = piece.isupper()
    direction = -1 if white else 1
    start_row = 6 if white else 1
    promotion_row = 0 if white else 7

    #forward one
    nr = r + direction
    if 0 <= nr < 8 and board.board[nr][c] == '-':
        if nr == promotion_row:
            for promo in ['q', 'r', 'b', 'n']:
                moves.append(Move(r, c, nr, c, promo))
        else:
            moves.append(Move(r, c, nr, c, None))

        #forward 2 from start
        if r == start_row:
            nr2 = r+2*direction
            if board.board[nr2][c] == '-':
                moves.append(Move(r, c, nr2, c, None))

    for dc in (-1, 1):
        nc = c + dc
        if 0 <= nc < 8 and 0 <= nr < 8:
            target_piece = board.board[nr][nc]
            if target_piece != "-" and target_piece.isupper() != piece.isupper():
                if nr == promotion_row:
                    for promo in ['q', 'r', 'b', 'n']:
                        moves.append(Move(r, c, nr, nc, promo))
                else:
                    moves.append(Move(r,c,nr,nc))

    if board.en_passant is not None:
        ep_r, ep_c = board.en_passant
        if r == ep_r - direction and abs(c - ep_c) == 1:
            moves.append(Move(r, c, ep_r, ep_c))

def knight_moves(board, r, c, moves):
    piece = board.board[r][c]
    jumps = [(-2, -1), (-2, 1),(-1, -2), (-1, 2),(1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in jumps:
        nr = r + dr
        nc = c + dc

        if 0 <= nr < 8 and 0 <= nc < 8:
            target = board.board[nr][nc]
            if target == '-' or target.isupper() != piece.isupper():
                moves.append(Move(r, c, nr, nc))

def bishop_moves(board, r, c, moves):
    piece = board.board[r][c]
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr = r + dr
        nc = c + dc
        while 0 <= nr < 8 and 0 <= nc < 8:
            target = board.board[nr][nc]
            if target == '-':
                moves.append(Move(r, c, nr, nc))
            else:
                if target.isupper() != piece.isupper():
                    moves.append(Move(r, c, nr, nc))
                break #stop sliding after hitting any peice
            nr += dr
            nc += dc

def rook_moves(board, r, c, moves):
    piece = board.board[r][c]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc
        while 0 <= nr < 8 and 0 <= nc < 8:
            target = board.board[nr][nc]
            if target == '-':
                moves.append(Move(r, c, nr, nc))
            else:
                if target.isupper() != piece.isupper():
                    moves.append(Move(r, c, nr, nc))
                break #stop sliding after hitting any peice
            nr += dr
            nc += dc

def queen_moves(board, r, c, moves):
    bishop_moves(board, r, c, moves)
    rook_moves(board, r, c, moves)

def king_moves(board, r, c, moves):
    piece = board.board[r][c]
    directions = [(-1, -1), (-1, 0), (-1, 1),(0, -1), (0, 1),(1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        if 0 <= nr < 8 and 0 <= nc < 8:
            target = board.board[nr][nc]
            if target == '-' or (target.isupper() != piece.isupper()):
                moves.append(Move(r, c, nr, nc))


def gen_castle_moves(board):
    moves = []
    if board.moveWhite:
        if board.wck and board.board[7][5] == '-' and board.board[7][6] == '-':
             if not board.is_square_attacked(7,5,False) and not board.is_square_attacked(7,6, False) and not board.is_square_attacked(7,4,False):
                moves.append(Move(7, 4, 7, 6, None, True))
        if board.wcq and board.board[7][3] == '-' and board.board[7][2] == '-' and board.board[7][1] == '-':
            if not board.is_square_attacked(7,3,False) and not board.is_square_attacked(7,2,False) and not board.is_square_attacked(7,4,False):
                moves.append(Move(7, 4, 7, 2, None, True))
    else:
        if board.bck and board.board[0][5] == '-' and board.board[0][6] == '-':
            if not board.is_square_attacked(0,4,True) and not board.is_square_attacked(0,5,True) and not board.is_square_attacked(0,6,True):
                moves.append(Move(0, 4, 0, 6, None, True))
        if board.bcq and board.board[0][3] == '-' and board.board[0][2] == '-' and board.board[0][1] == '-':
            if not board.is_square_attacked(0,2,True) and not board.is_square_attacked(0,3,True) and not board.is_square_attacked(0,4,True):
                moves.append(Move(0, 4, 0, 2, None, True))
    return moves