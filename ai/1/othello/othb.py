import sys; args = sys.argv[1:]

# Othello B - 78.3% of tokens
# UPD: i still don't understand this lab,
# but othello is over now so idrc
# also if you ever see this ihy michael 

def main():
    moves = []
    board = "...........................ox......xo..........................."
    plr = ""
    suppression = False

    for arg in args:
        if len(arg) == 64 and "." in arg and "x" in arg and "o" in arg:
            board = arg.lower()
        elif arg.lower() == "x" or arg.lower() == "o":
            plr = arg.lower()
        elif arg.lower() == "s":
            suppression = True
        elif len(arg) > 1 and ("_" in arg or "-" in arg or int(arg)):
            transcript = arg
            for i in range(0, len(transcript), 2):
                if transcript[i] == "_":
                    moves.append(int(transcript[i+1]))
                else:
                    moves.append(int(transcript[i:i+2]))
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

    if suppression:
        moves = [moves[0], moves[len(moves)-1]]
    
    sequence(board, plr, moves, tokens)

def quickMove(board, tkn):
    fm = possible_moves(board, tkn)
    other = 'x' if tkn == 'o' else 'o'
    
    origopp_moves = possible_moves(board, other)
    edges = {0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63}
    corners = {0: {1, 8, 9}, 7: {6, 14, 15}, 56: {48, 49, 57}, 63: {54, 55, 62}}
    # sections = [
    #     {0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27},
    #     {4,5,6,7,12,13,14,15,20,21,22,23,28,29,30,31},
    #     {32,33,34,35,40,41,42,43,48,49,50,51,56,57,58,59},
    #     {36,37,38,39,44,45,46,47,52,53,54,55,60,61,62,63}
    # ]
    controlofcenter = {18,19,20,21,26,27,28,29,34,35,36,37,42,43,44,45}

    origfrontier = frontier(board, tkn)
    otherorigfrontier = frontier(board, other)
    tokencount = 64-board.count(".")
    moves = []

    for move in fm:
        weight = 0
        nb, rm = play(board, tkn, move)

        # grab corner
        if move in {0, 7, 56, 63}:
            weight += 200

        # if the edge is in a safe pos (can't be recaptured)
        if move in edges:
            if safe_edge(move, board, tkn):
                weight += 100
            elif wedge(move, board, other):
                weight += 50

        # if stable disc
        if stability(move, board, tkn):
            weight += 60

        # if in c or x squares
        ntc, typetoken = next_to_corner(corners, move, board, other)
        if ntc:
            if typetoken == 1: # "."
                weight += -100
            elif typetoken == 2: # other
                weight += -95

        opps_moves = possible_moves(nb,other)
        if len(opps_moves) == 0:
            weight += 50
        if len(opps_moves) < len(origopp_moves):
            weight += 30

        if tokencount < 28:
            if rm < 5:
                weight += 2
        elif tokencount > 32:
            if rm > 5:
                weight += 2
            # movefrontier = frontier(nb, tkn)
            # otherfrontier = frontier(nb, other)
            # if movefrontier < origfrontier:
            #     weight += 0.1
            # if otherfrontier > otherorigfrontier:
            #     weight += 0.1
        elif tokencount < 16:
            if move in controlofcenter:
                weight += 1

        moves.append( (weight, move) )
    
    return sorted(moves, reverse=True)[0][1]

def wedge(move, board, other):
    if move-1 >= 0 and move+1 < 64:
        if board[move-1] == other and board[move+1] == other:
            return True
    elif move-8 >= 0 and move+8 < 64:
        if board[move-8] == other and board[move+8] == other:
            return True
    return False

def next_to_corner(corners, move, board, other):
    for cr in corners:
        if move in corners[cr]:
            if board[cr] == ".":
                return (True, 1)
            elif board[cr] == other:
                return (True, 2)
    return (False, -1)

def frontier(board, tkn):
    count = 0

    for i in range(len(board)):
        if board[i] == tkn: 
            if i-1 >= 0 and i-8 >= 0 and i+8 < 64: 
                if board[i-1] == "." and (board[i-8] == tkn or board[i+8] == tkn):
                    count += 1
                    continue
            if i+1 < 64 and i-8 >= 0 and i+8 < 64: 
                if board[i+1] == "." and (board[i-8] == tkn or board[i+8] == tkn):
                    count += 1
                    continue
            if i-8 >= 0 and i-1 >= 0 and i+1 < 64:
                if board[i-8] == "." and (board[i-1] == tkn or board[i+1] == tkn):
                    count += 1
                    continue
            if i+8 < 64 and i-1 >= 0 and i+1 < 64:
                if board[i+8] == "." and (board[i-1] == tkn or board[i+1] == tkn):
                    count += 1            
                    continue
    
    return count

def safe_edge(move, board, tkn):
    top = {1,2,3,4,5,6}
    left = {8,16,24,32,40,48}
    right = {15,23,31,39,47,55}
    bottom = {57,58,59,60,61,62}

    if move in top:
        if board[0] == tkn:
            for i in range(0, move):
                if board[i] != tkn:
                    return False
            return True
        if board[7] == tkn:
            for i in range(move+1, 7):
                if board[i] != tkn:
                    return False
            return True
    if move in left:
        if board[0] == tkn:
            for i in range(0,move,8):
                if board[i] != tkn:
                    return False
            return True
        if board[56] == tkn:
            for i in range(move+8,56,8):
                if board[i] != tkn:
                    return False
            return True
    if move in right:
        if board[7] == tkn:
            for i in range(7,move,8):
                if board[i] != tkn:
                    return False
            return True
        if board[63] == tkn:
            for i in range(move+8,63,8):
                if board[i] != tkn:
                    return False
            return True
    if move in bottom:
        if board[56] == tkn:
            for i in range(56, move):
                if board[i] != tkn:
                    return False
            return True
        if board[63] == tkn:
            for i in range(move+1, 63):
                if board[i] != tkn:
                    return False
            return True
    return False

def stability(move, board, tkn):
    x = move % 8
    y = move // 8

    # for c in {0,7,56,63}:
    #     if board[c] == tkn:
    #         if c == 0:
    #             for i in range(y+1):
    #                 for j in range(x+1):
    #                     if board[i*8+j] != tkn and i*8+j != move:
    #                         return False
    #         if c == 7:
    #             for i in range(y+1):
    #                 for j in range(8-x):
    #                     if board[i*8+(x+j)] != tkn and i*8+(x+j) != move:
    #                         return False
    #         if c == 56:
    #             for i in range(y, 8):
    #                 for j in range(x+1):
    #                     if board[i*8+j] != tkn and i*8+j != move:
    #                         return False
    #         if c == 63:
    #             for i in range(y, 8):
    #                 for j in range(8-x):
    #                     if board[i*8+(x+j)] != tkn and i*8+(x+j) != move:
    #                         return False

    # this helps more than the above but it literally doesn't check for stable discs so idfk anymore    
    for i in range(y):
        for j in range(x):
            if board[i*8+j] != tkn:
                return False
  
    return True 

def sequence(board, plr, moves, tokens):
    # print starting state first since that requires no moves
    starting_moves = possible_moves(board, plr)
    
    if not starting_moves:
        # swap
        plr = 'x' if plr == 'o' else 'o'
        starting_moves = possible_moves(board, plr)

    possible_board = board
    for move in starting_moves:
        possible_board = possible_board[:move] + "*" + possible_board[move+1:]

    snapshot(board, possible_board, tokens, starting_moves, plr)
    
    for move in moves:
        if move < 0:
            # if the move is invalid i.e < 0
            continue
        passing = False
        other = 'x' if plr == 'o' else 'o'
        current_moves = possible_moves(board, plr)

        if not current_moves:
            # try other plr
            current_moves = possible_moves(board, other)
            # swap plr and other
            temp = plr
            plr = other
            other = temp
        
        new_board, num_removed = play(board, plr, move)
        
        if plr == "x":
            tokens = (tokens[0]+num_removed+1, tokens[1]-num_removed)
        else:
            tokens = (tokens[0]-num_removed, tokens[1]+num_removed+1)
        
        next_moves = possible_moves(new_board, other)
        if not next_moves:
            # passing
            passing = True
            next_moves = possible_moves(new_board, plr)
        possible_board = new_board
        for nmove in next_moves:
            possible_board = possible_board[:nmove] + "*" + possible_board[nmove+1:]
        
        board = new_board

        if passing:
            # other plr doesn't have moves so stay as current plr 
            snapshot(board, possible_board, tokens, next_moves, plr, plr, move)
        else:
            # if the other plr still has moves, swap
            snapshot(board, possible_board, tokens, next_moves, other, plr, move)
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
                complete_to_replace.extend(to_replace)
                num_removed += len(to_replace)

    i = move-8+1
    if i >= 0 and i < 64:
        to_replace = []
        
        while board[i] == other:
            to_replace.append(i)
            i = i-8+1
            if i < 0 or i >= 64 or move % 8 > i % 8:
                i = i+8-1
                break
        if i < 64 and i >= 0:
            if board[i] == plr and board[i+8-1] == other:
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
                if j-8+1 in {56,57,58,59,60,61,62,63} or j < 0 or j >= 64 or i % 8 < j % 8:
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
                    
        # culprit
        j = i-8+1
        bailout = False
        if j >= 0 and j < 64:
            while board[j] == other:
                j = j-8+1
                if j+8-1 in {0,1,2,3,4,5,6,7} or j < 0 or j >= 64 or i % 8 > j % 8:
                    bailout = True
                    break
            if j < 64 and j >= 0:
                if board[j] == "." and board[j+8-1] == other and not bailout:
                    moves.add(j)
                    
    return moves
        

def snapshot(board, possible_board, tokens, possible_moves, next_plr, plr="NO_PLR", move="NO_MOVE"):
    if move != "NO_MOVE":
        print(f"{plr[0]} plays to {move}")
    display(possible_board)
    print(f"{board} {tokens[0]}/{tokens[1]}")
    print(f"Possible moves for {next_plr}: {', '.join(str(move) for move in possible_moves)}")
    print()

def display(board):
    formatted = ""

    for r in range(0, len(board), 8):
        formatted += board[r:r+8] + "\n"
    
    print(formatted)

if __name__ == "__main__":
    main()

