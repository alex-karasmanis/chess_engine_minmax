from board import Board
from engine import choose_best_move
from movesGen import gen_legal_moves
import time

def input_to_move(move):
    col = ord(move[0]) - ord('a')
    row = 8 - int(move[1])
    return row, col

def col_to_letter(col):
    return chr(ord('a') + col)

def row_to_rank(row):
    return str(8 - row)

def hint(board, depth):
    move = choose_best_move(board, depth, True)
    print("Your hint is: " + col_to_letter(move.sc) + row_to_rank(move.sr) + col_to_letter(move.ec) + row_to_rank(move.er))




def main():
    board = Board()

    print("Chess\n0. Help\n1. Two humans play\n2. Play against engine\n3. Two Engines")
    choice = input("Select Option: ")
    if choice == '0':
        print("Welcome to chess!")
        print("Supports Player vs Player, Player vs Engin, and Engine vs Engine")
        print("When playing againsed chess engine, choose what color you want, how deep you want the ending to search")
        print("eg. depth 3 is 3 moves lookahead, and if you want the engine to apply alpha-beta pruning when searching")
        print("When entering a move, enter the formate letter, number for the starting pos, followed by letter number for the end")
        print("If you need to promote enter an additional letter (n, b, q, r) of the piece you want to promote to")
        print("To castle, move the king to the new position it will be after the castle.")
        print("Example notations: piece goes from e2 to e4 e2e4: pawn goes from a7 to a8 and promotes to a queen a7a8q")
        print("Castle king side as white e1f1")
    elif choice == "1":
        print("Chess Two Humans")
        while True:
            board.print_board()
            moves = gen_legal_moves(board)
            if not moves:
                turn_white = board.moveWhite
                if board.is_in_check(turn_white):
                    if turn_white:
                        print("Checkmate Black Wins")
                    else:
                        print("Checkmate White Wins")
                else:
                    print("Stalemate")
                break
            print("White" if board.moveWhite else "Black", "to move")
            move_str = input("Enter your move (e.g. e2e4) ").strip().lower()
            if move_str == "q":
                break
            elif move_str == "hint":
                hint_depth=int(input("Enter depth for hint: "))
                hint(board, hint_depth)
                continue
            if len(move_str) not in (4, 5):
                print("Invalid format")
                continue
            sr, sc = input_to_move(move_str[0:2])
            er,ec = input_to_move(move_str[2:4])
            promotion = None
            if len(move_str) == 5:
                promotion = move_str[4]
            chosen = None
            for m in moves:
                m_promo = getattr(m, "promotion", None)
                if m.sr == sr and m.sc == sc and m.er == er and m.ec == ec and m_promo == promotion:
                    chosen = m
                    print("Move: " + col_to_letter(sc) + row_to_rank(sr) + col_to_letter(ec)+row_to_rank(er))
                    break
            if chosen is None:
                print("Invalid move")
                continue
            board.make_move(chosen)

    elif choice == "2":
        print("Chess Play Against Engine")
        choice = int(input("Choose color. 1. White 2. Black: "))
        depth = int(input("Enter Depth: "))
        human_is_white = True if choice == 1 else False
        choice2 = input("Use Alpha-Beta Pruning? 1. Yes. 2. No: ").strip()
        use_alpha_beta = True if choice2 == "1" else False
        print("You are", "White" if human_is_white else "Black")
        print("Depth:", depth)
        print("Alpha-Beta Pruning", "On" if use_alpha_beta else "On")
        while True:
            board.print_board()
            moves = gen_legal_moves(board)
            if not moves:
                if board.is_in_check(board.moveWhite):
                    winner = 'Black' if board.moveWhite else 'White'
                    print(f"Checkmate {winner} wins")
                else:
                    print("Stale Mate")
                break

            #humans turn
            if board.moveWhite == human_is_white:
                move_str = input("Enter your move (e2e4) ").strip().lower()
                if move_str == "q":
                    break
                elif move_str == "hint":
                    hint_depth = int(input("Enter depth for hint: "))
                    hint(board, hint_depth)
                    continue
                if len(move_str) not in (4, 5):
                    print("Invalid format.")
                    continue
                sr, sc = input_to_move(move_str[0:2])
                er, ec = input_to_move(move_str[2:4])
                promotion = None
                if len(move_str) == 5:
                    promotion = move_str[4]
                chosen = None
                for m in moves:
                    m_promo = getattr(m, "promotion", None)
                    if m.sr == sr and m.sc == sc and m.er == er and m.ec == ec and m_promo == promotion:
                        chosen = m
                        print("Move: " + col_to_letter(sc) + row_to_rank(sr) + col_to_letter(ec) + row_to_rank(er))
                        break
                if chosen is None:
                    print("Invalid move")
                    continue
                board.make_move(chosen)
            else:
                #engins turn
                move = choose_best_move(board, depth, use_alpha_beta)
                print("Engin Plays: " + col_to_letter(move.sc) + row_to_rank(move.sr) + col_to_letter(move.ec)+row_to_rank(move.er))
                board.make_move(move)
    elif choice == "3":
        print("Two engines with set parameters")
        t_white_total = 0.0
        t_black_total = 0.0
        n_white_moves = 0
        n_black_moves =0
        plies = 0
        while True:
            board.print_board()
            moves = gen_legal_moves(board)
            if not moves:
                if board.is_in_check(board.moveWhite):
                    winner = 'Black' if board.moveWhite else 'White'
                    print(f"Checkmate {winner} wins")
                else:
                    print("Stale Mate")
                break
            if plies >= 10:
                print("Draw by ply limit.")
                break
            if board.moveWhite:
                use_ab = True
            else:
                use_ab = True

            side_to_move = board.moveWhite
            start = time.perf_counter()
            move = choose_best_move(board, 3, use_ab)
            elapsed = time.perf_counter() - start

            if side_to_move:
                n_white_moves += 1
                t_white_total += elapsed
            else:
                n_black_moves += 1
                t_black_total += elapsed
            print("White Total: " + str(t_white_total) + " Black Total: " + str(t_black_total))
            board.make_move(move)
            plies+=1

if __name__ == "__main__":
    main()
