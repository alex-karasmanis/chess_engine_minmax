from movesGen import gen_legal_moves
from evaluate import evaluate
import math

def minmax(board, depth):
    moves = gen_legal_moves(board)
    if depth == 0 or not moves:
        return checkmate_or_evaluate(board,moves)

    if board.moveWhite:
        best =-math.inf
        for m in moves:
            b2 = board.clone()
            b2.make_move(m)
            best = max(best, minmax(b2, depth-1))
        return best
    else:
        best =math.inf
        for m in moves:
            b2 = board.clone()
            b2.make_move(m)
            best = min(best, minmax(b2, depth-1))
        return best

#alpha beta pruning
def minimax_alpha_beta(board, depth, alpha = - math.inf, beta = math.inf):
    moves = gen_legal_moves(board)
    if depth == 0 or not moves:
        return checkmate_or_evaluate(board, moves)
    if board.moveWhite:
        value = -math.inf
        for m in moves:
            b2 = board.clone()
            b2.make_move(m)
            value = max(value, minimax_alpha_beta(b2, depth-1, alpha, beta))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = math.inf
        for m in moves:
            b2 = board.clone()
            b2.make_move(m)
            value = min(value, minimax_alpha_beta(b2, depth-1, alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def choose_best_move(board, depth, use_alpha_beta = True):
    moves = gen_legal_moves(board)

    if not moves:
        return None

    best_move = None
    if board.moveWhite:
        best_score = -math.inf
        for m in moves:
            b2 = board.clone()
            b2.make_move(m)
            score = (
                minimax_alpha_beta(b2, depth - 1, -math.inf, math.inf)
                if use_alpha_beta
                else minmax(b2, depth - 1)
            )
            if score > best_score:
                best_score = score
                best_move = m
    else:
        best_score = math.inf
        for m in moves:
            b2 = board.clone()
            b2.make_move(m)
            score = (
                minimax_alpha_beta(b2, depth - 1, -math.inf, math.inf)
                if use_alpha_beta
                else minmax(b2, depth - 1)
            )
            if score < best_score:
                best_score = score
                best_move = m
    return best_move

def checkmate_or_evaluate(board,moves):
    if not moves:
        if board.is_in_check(board.moveWhite):
            return -100000 if board.moveWhite else 100000 #checkmate
        else:
            return 0 #staleMate
    return evaluate(board)

