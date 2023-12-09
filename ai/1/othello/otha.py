import sys; args = sys.argv[1:]

# Othello A

def main():
    moves = []
    board = "...........................ox......xo..........................."
    plr = ""

    for arg in args:
        if len(arg) == 64:
            board = arg.lower()
        elif arg.lower() == "x" or arg.lower() == "o":
            plr = arg.lower()
        elif arg:
            if not arg[0] in {'0','1','2','3','4','5','6','7','8','9'}:
                arg = (int(arg[1])-1)*8+(ord(arg[0].lower())-97)
            moves.append(int(arg))
    
    tokens = (board.count("x"), board.count("o"))
    if not plr:
        if (tokens[0]+tokens[1])%2 == 0:
            plr = "x"
        else:
            plr = "o"

    sequence(board, plr, moves, tokens)

def sequence(board, plr, moves, tokens):
    starting_moves = possible_moves(board, plr)

    possible_board = board
    for move in starting_moves:
        possible_board = possible_board[:move] + "*" + possible_board[move+1:]

    snapshot(board, possible_board, tokens, starting_moves)
    print(f"Possible moves for {plr}: {', '.join(str(move) for move in starting_moves)}")
    print()
    
    for move in moves:
        if move < 0:
            continue
        new_board, num_removed = play(board, plr, move)
        
        if plr == "x":
            tokens = (tokens[0]+num_removed+1, tokens[1]-num_removed)
        else:
            tokens = (tokens[0]-num_removed, tokens[1]+num_removed+1)
        other = "x" if plr == "o" else "o"
        
        next_moves = possible_moves(new_board, other)
        passing = False
        if not next_moves:
            # passing
            passing = True
            next_moves = possible_moves(new_board, plr)
        possible_board = new_board
        for nmove in next_moves:
            possible_board = possible_board[:nmove] + "*" + possible_board[nmove+1:]
        
        board = new_board 
        snapshot(board, possible_board, tokens, next_moves, plr, move)
        print()
        if not passing:
            plr = other


def play(board, plr, move):
    num_removed = 0 
    other = "x" if plr == "o" else "o"
    complete_to_replace = []

    i = move-1
    if i // 8 == move // 8 and i >= 0:
        to_replace = []
    
        while board[i] == other:
            to_replace.append(i)
            i -= 1
            if i // 8 != move // 8:
                i+=1
                break
        if i < 64 and i >= 0:
            if board[i] == plr and board[i+1] == other:
                # for tile in to_replace:
                #     board = board[:tile] + plr + board[tile+1:]
                complete_to_replace.extend(to_replace)
                num_removed += len(to_replace)

    i = move+1
    if i // 8 == move // 8 and i < 64:
        to_replace = []
    
        while board[i] == other:
            to_replace.append(i)
            i += 1
            if i // 8 != move // 8:
                i-=1
                break
        if i < 64 and i >= 0:
            if board[i] == plr and board[i-1] == other:
                # for tile in to_replace:
                #     board = board[:tile] + plr + board[tile+1:]
                complete_to_replace.extend(to_replace)
                num_removed += len(to_replace)

    i = move-8
    if i >= 0:
        to_replace = []
    
        while board[i] == other:
            to_replace.append(i)
            i -= 8
            if i < 0:
                i+=8
                break
        if i < 64 and i >= 0:
            if board[i] == plr and board[i+8] == other:
                # for tile in to_replace:
                #     board = board[:tile] + plr + board[tile+1:]
                complete_to_replace.extend(to_replace)
                num_removed += len(to_replace)
    
    i = move+8
    if i < 64:
        to_replace = []
    
        while board[i] == other:
            to_replace.append(i)
            i += 8
            if i >= 64:
                i-=8
                break
        if i < 64 and i >= 0:
            if board[i] == plr and board[i-8] == other:
                # for tile in to_replace:
                #     board = board[:tile] + plr + board[tile+1:]
                complete_to_replace.extend(to_replace)
                num_removed += len(to_replace)
    
    i = move-8-1
    if i >= 0:
        to_replace = []
    
        while board[i] == other:
            to_replace.append(i)
            i = i-8-1
            if i < 0 or move % 8 < i % 8:
                i = i+8+1
                break
        if i < 64 and i >= 0:
            if board[i] == plr and board[i+8+1] == other:
                # for tile in to_replace:
                #     board = board[:tile] + plr + board[tile+1:]
                complete_to_replace.extend(to_replace)
                num_removed += len(to_replace)
    
    i = move+8+1
    if i < 64:
        to_replace = []
    
        while board[i] == other:
            to_replace.append(i)
            i = i+8+1
            if i >= 64 or move % 8 > i % 8:
                i = i-8-1
                break
        if i < 64 and i >= 0:
            if board[i] == plr and board[i-8-1] == other:
                # for tile in to_replace:
                #     board = board[:tile] + plr + board[tile+1:]
                complete_to_replace.extend(to_replace)
                num_removed += len(to_replace)
    
    i = move+8-1
    if i >= 0 and i < 64:
        to_replace = []
        
        while board[i] == other:
            to_replace.append(i)
            i = i+8-1
            if i < 0 or i >= 64 or move % 8 < i % 8:
                i = i-8+1
                break
        if i < 64 and i >= 0:
            if board[i] == plr and board[i-8+1] == other:
                # for tile in to_replace:
                #     board = board[:tile] + plr + board[tile+1:]
                complete_to_replace.extend(to_replace)
                num_removed += len(to_replace)

    i = move-8+1
    if i >= 0 and i < 64:
        to_replace = []
        
        while board[i] == other:
            to_replace.append(i)
            i = i-8+1
            if i < 0 and i >= 64 or move % 8 > i % 8:
                i = i+8-1
                break
        if i < 64 and i >= 0:
            if board[i] == plr and board[i+8-1] == other:
                # for tile in to_replace:
                #     board = board[:tile] + plr + board[tile+1:]
                complete_to_replace.extend(to_replace)
                num_removed += len(to_replace)

    for tile in complete_to_replace:
        board = board[:tile] + plr + board[tile+1:]

    board = board[:move] + plr + board[move+1:]

    return (board, num_removed)


def possible_moves(board, plr):
    moves = set()
    other = "x" if plr == "o" else "o"

    for i in range(len(board)):
        if board[i] == "." or board[i] == other: continue
        
        # row backward
        j = i-1
        bailout = False
        if i // 8 == j // 8 and j >= 0:
            while board[j] == other:
                j -= 1
                if i // 8 != j // 8:
                    bailout = True
                    break
            if j < 64 and j >= 0:
                if board[j] == "." and board[j+1] == other and not bailout:
                    moves.add(j)
                    
        # row forward
        j = i+1
        bailout = False
        if i // 8 == j // 8 and j < 64:
            while board[j] == other:
                j += 1
                if i // 8 != j // 8:
                    bailout = True
                    break
            if j < 64 and j >= 0:
                if board[j] == "." and board[j-1] == other and not bailout:
                    moves.add(j)
                    
        # col backward
        j = i-8
        bailout = False
        if j >= 0:
            while board[j] == other:
                j -= 8
                if j < 0:
                    bailout = True
                    break
            if j < 64 and j >= 0:
                if board[j] == "." and board[j+8] == other and not bailout:
                    moves.add(j)
        
        # col foward
        j = i+8
        bailout = False
        if j < 64:
            while board[j] == other:
                j += 8
                if j >= 64:
                    bailout = True
                    break
            if j < 64 and j >= 0:
                if board[j] == "." and board[j-8] == other and not bailout:
                    moves.add(j)
                    
        # diag left
        j = i-8-1 # obviously -8-1 = -9 but it's easier to understand what's happening
        bailout = False
        if j >= 0:
            while board[j] == other:
                j = j-8-1
                if j < 0 or i % 8 < j % 8:
                    bailout = True
                    break
            if j < 64 and j >= 0:
                if board[j] == "." and board[j+8+1] == other and not bailout:
                    moves.add(j)
                    
        j = i+8-1
        bailout = False
        if j >= 0 and j < 64:
            while board[j] == other:
                j = j+8-1
                if j < 0 or j >= 64 or i % 8 < j % 8:
                    bailout = True
                    break
            if j < 64 and j >= 0:
                if board[j] == "." and board[j-8+1] == other and not bailout:
                    moves.add(j)

        # diag right
        j = i+8+1
        bailout = False
        if j < 64:
            while board[j] == other:
                j = j+8+1
                if j >= 64 or i % 8 > j % 8:
                    bailout = True
                    break
            if j < 64 and j >= 0:
                if board[j] == "." and board[j-8-1] == other and not bailout:
                    moves.add(j)
        
        j = i-8+1
        bailout = False
        if j >= 0 and j < 64:
            while board[j] == other:
                j = j-8+1
                if j < 0 or j >= 64 or i % 8 > j % 8:
                    bailout = True
                    break
            if j < 64 and j >= 0:
                if board[j] == "." and board[j+8-1] == other and not bailout:
                    moves.add(j)
    
    return moves
        

def snapshot(board, possible_board, tokens, possible_moves, plr="NO_PLR", move="NO_MOVE"):
    if move != "NO_MOVE":
        print(f"{plr} plays to {move}")
    display(possible_board)
    print(f"{board} {tokens[0]}/{tokens[1]}")
    if plr != "NO_PLR":
        print(f"Possible moves for {'x' if plr == 'o' else 'o'}: {', '.join(str(move) for move in possible_moves)}")

def display(board):
    formatted = ""

    for r in range(0, len(board), 8):
        formatted += board[r:r+8] + "\n"
    
    print(formatted)

if __name__ == "__main__":
    main()

