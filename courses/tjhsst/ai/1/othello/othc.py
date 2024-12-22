import sys; args = sys.argv[1:]

# Othello C - Negamax - 100%

flips = {
    # * this is not what you should do, but it works 
    # index: [[right], [left], [down], [up], [leftdowndiag], [leftupdiag], [rightdowndiag], [rightupdiag]]		
    0: [[1, 2, 3, 4, 5, 6, 7], [], [8, 16, 24, 32, 40, 48, 56], [], [], [], [9, 18, 27, 36, 45, 54, 63], []],
    1: [[2, 3, 4, 5, 6, 7], [0], [9, 17, 25, 33, 41, 49, 57], [], [8], [], [10, 19, 28, 37, 46, 55], []], 
    2: [[3, 4, 5, 6, 7], [1, 0], [10, 18, 26, 34, 42, 50, 58], [], [9, 16], [], [11, 20, 29, 38, 47], []], 
    3: [[4, 5, 6, 7], [2, 1, 0], [11, 19, 27, 35, 43, 51, 59], [], [10, 17, 24], [], [12, 21, 30, 39], []], 
    4: [[5, 6, 7], [3, 2, 1, 0], [12, 20, 28, 36, 44, 52, 60], [], [11, 18, 25, 32], [], [13, 22, 31], []], 
    5: [[6, 7], [4, 3, 2, 1, 0], [13, 21, 29, 37, 45, 53, 61], [], [12, 19, 26, 33, 40], [], [14, 23], []], 
    6: [[7], [5, 4, 3, 2, 1, 0], [14, 22, 30, 38, 46, 54, 62], [], [13, 20, 27, 34, 41, 48], [], [15], []], 
    7: [[], [6, 5, 4, 3, 2, 1, 0], [15, 23, 31, 39, 47, 55, 63], [], [14, 21, 28, 35, 42, 49, 56], [], [], []], 
    8: [[9, 10, 11, 12, 13, 14, 15], [], [16, 24, 32, 40, 48, 56], [0], [], [1], [17, 26, 35, 44, 53, 62], []], 
    9: [[10, 11, 12, 13, 14, 15], [8], [17, 25, 33, 41, 49, 57], [1], [16], [2], [18, 27, 36, 45, 54, 63], [0]], 
    10: [[11, 12, 13, 14, 15], [9, 8], [18, 26, 34, 42, 50, 58], [2], [17, 24], [3], [19, 28, 37, 46, 55], [1]],
    11: [[12, 13, 14, 15], [10, 9, 8], [19, 27, 35, 43, 51, 59], [3], [18, 25, 32], [4], [20, 29, 38, 47], [2]], 
    12: [[13, 14, 15], [11, 10, 9, 8], [20, 28, 36, 44, 52, 60], [4], [19, 26, 33, 40], [5], [21, 30, 39], [3]], 
    13: [[14, 15], [12, 11, 10, 9, 8], [21, 29, 37, 45, 53, 61], [5], [20, 27, 34, 41, 48], [6], [22, 31], [4]], 
    14: [[15], [13, 12, 11, 10, 9, 8], [22, 30, 38, 46, 54, 62], [6], [21, 28, 35, 42, 49, 56], [7], [23], [5]], 
    15: [[], [14, 13, 12, 11, 10, 9, 8], [23, 31, 39, 47, 55, 63], [7], [22, 29, 36, 43, 50, 57], [], [], [6]], 
    16: [[17, 18, 19, 20, 21, 22, 23], [], [24, 32, 40, 48, 56], [8, 0], [], [9, 2], [25, 34, 43, 52, 60, 61], []], 
    17: [[18, 19, 20, 21, 22, 23], [16], [25, 33, 41, 49, 57], [9, 1], [24], [10, 3], [26, 35, 44, 53, 62], [8]], 
    18: [[19, 20, 21, 22, 23], [17, 16], [26, 34, 42, 50, 58], [10, 2], [25, 32], [11, 4], [27, 36, 45, 54, 63], [9, 0]], 
    19: [[20, 21, 22, 23], [18, 17, 16], [27, 35, 43, 51, 59], [11, 3], [26, 33, 40], [12, 5], [28, 37, 46, 55], [10, 1]], 
    20: [[21, 22, 23], [19, 18, 17, 16], [28, 36, 44, 52, 60], [12, 4], [27, 34, 41, 48], [13, 6], [29, 38, 47], [11, 2]], 
    21: [[22, 23], [20, 19, 18, 17, 16], [29, 37, 45, 53, 61], [13, 5], [28, 35, 42, 49, 56], [14, 7], [30, 39], [12, 3]], 
    22: [[23], [21, 20, 19, 18, 17, 16], [30, 38, 46, 54, 62], [14, 6], [29, 36, 43, 50, 57], [15], [31], [13, 4]], 
    23: [[], [22, 21, 20, 19, 18, 17, 16], [31, 39, 47, 55, 63], [15, 7], [30, 37, 44, 51, 58], [], [], [14, 5]], 
    24: [[25, 26, 27, 28, 29, 30, 31], [], [32, 40, 48, 56], [16, 8, 0], [], [17, 10, 3], [33, 42, 51, 60], []], 
    25: [[26, 27, 28, 29, 30, 31], [24], [33, 41, 49, 57], [17, 9, 1], [32], [18, 11, 4], [34, 43, 52, 61], [16]], 
    26: [[27, 28, 29, 30, 31], [25, 24], [34, 42, 50, 58], [18, 10, 2], [33, 40], [19, 12, 5], [35, 44, 53, 62], [17, 8]], 
    27: [[28, 29, 30, 31], [26, 25, 24], [35, 43, 51, 59], [19, 11, 3], [34, 41, 48], [20, 13, 6], [36, 45, 54, 63], [18, 9, 0]], 
    28: [[29, 30, 31], [27, 26, 25, 24], [36, 44, 52, 60], [20, 12, 4], [35, 42, 49, 56], [21, 14, 7], [37, 46, 55], [19, 10, 1]], 
    29: [[30, 31], [28, 27, 26, 25, 24], [37, 45, 53, 61], [21, 13, 5], [36, 43, 50, 57], [22, 15], [38, 47], [20, 11, 2]], 
    30: [[31], [29, 28, 27, 26, 25, 24], [38, 46, 54, 62], [22, 14, 6], [37, 44, 51, 58], [23], [39], [21, 12, 3]], 
    31: [[], [30, 29, 28, 27, 26, 25, 24], [39, 47, 55, 63], [23, 15, 7], [38, 45, 52, 59], [], [], [22, 13, 4]], 
    32: [[33, 34, 35, 36, 37, 38, 39], [], [40, 48, 56], [24, 16, 8, 0], [], [25, 18, 11, 4], [41, 50, 59], []],
    33: [[34, 35, 36, 37, 38, 39], [32], [41, 49, 57], [25, 17, 9, 1], [40], [26, 19, 12, 5], [42, 51, 60], [24]], 
    34: [[35, 36, 37, 38, 39], [33, 32], [42, 50, 58], [26, 18, 10, 2], [41, 48], [27, 20, 13, 6], [43, 52, 61], [25, 16]], 
    35: [[36, 37, 38, 39], [34, 33, 32], [43, 51, 59], [27, 19, 11, 3], [42, 49, 56], [28, 21, 14, 7], [44, 53, 62], [26, 17, 8]], 
    36: [[37, 38, 39], [35, 34, 33, 32], [44, 52, 60], [28, 20, 12, 4], [43, 50, 57], [29, 22, 15], [45, 54, 63], [27, 18, 9, 0]], 
    37: [[38, 39], [36, 35, 34, 33, 32], [45, 53, 61], [29, 21, 13, 5], [44, 51, 58], [30, 23], [46, 55], [28, 19, 10, 1]], 
    38: [[39], [37, 36, 35, 34, 33, 32], [46, 54, 62], [30, 22, 14, 6], [45, 52, 59], [31], [47], [29, 20, 11, 2]], 
    39: [[], [38, 37, 36, 35, 34, 33, 32], [47, 55, 63], [31, 23, 15, 7], [46, 53, 60], [], [], [30, 21, 12, 3]], 
    40: [[41, 42, 43, 44, 45, 46, 47], [], [48, 56], [32, 24, 16, 8, 0], [], [33, 26, 19, 12, 5], [49, 58], []], 
    41: [[42, 43, 44, 45, 46, 47], [40], [49, 57], [33, 25, 17, 9, 1], [48], [34, 27, 20, 13, 6], [50, 59], [32]], 
    42: [[43, 44, 45, 46, 47], [41, 40], [50, 58], [34, 26, 18, 10, 2], [49, 56], [35, 28, 21, 14, 7], [51, 60], [33, 24]], 
    43: [[44, 45, 46, 47], [42, 41, 40], [51, 59], [35, 27, 19, 11, 3], [50, 57], [36, 29, 22, 15], [52, 61], [34, 25, 16]], 
    44: [[45, 46, 47], [43, 42, 41, 40], [52, 60], [36, 28, 20, 12, 4], [51, 58], [37, 30, 23], [53, 62], [35, 26, 17, 8]], 
    45: [[46, 47], [44, 43, 42, 41, 40], [53, 61], [37, 29, 21, 13, 5], [52, 59], [38, 31], [54, 63], [36, 27, 18, 9, 0]], 
    46: [[47], [45, 44, 43, 42, 41, 40], [54, 62], [38, 30, 22, 14, 6], [53, 60], [39], [55], [37, 28, 19, 10, 1]], 
    47: [[], [46, 45, 44, 43, 42, 41, 40], [55, 63], [39, 31, 23, 15, 7], [54, 61], [], [], [38, 29, 20, 11, 2]], 
    48: [[49, 50, 51, 52, 53, 54, 55], [], [56], [40, 32, 24, 16, 8, 0], [], [41, 34, 27, 20, 13, 6], [57], []],
    49: [[50, 51, 52, 53, 54, 55], [48], [57], [41, 33, 25, 17, 9, 1], [56], [42, 35, 28, 21, 14, 7], [58], [40]], 
    50: [[51, 52, 53, 54, 55], [49, 48], [58], [42, 34, 26, 18, 10, 2], [57], [43, 36, 29, 22, 15], [59], [41, 32]], 
    51: [[52, 53, 54, 55], [50, 49, 48], [59], [43, 35, 27, 19, 11, 3], [58], [44, 37, 30, 23], [60], [42, 33, 24]], 
    52: [[53, 54, 55], [51, 50, 49, 48], [60], [44, 36, 28, 20, 12, 4], [59], [45, 38, 31], [61], [43, 34, 25, 16]], 
    53: [[54, 55], [52, 51, 50, 49, 48], [61], [45, 37, 29, 21, 13, 5], [60], [46, 39], [62], [44, 35, 26, 17, 8]], 
    54: [[55], [53, 52, 51, 50, 49, 48], [62], [46, 38, 30, 22, 14, 6], [61], [47], [63], [45, 36, 27, 18, 9, 0]], 
    55: [[], [54, 53, 52, 51, 50, 49, 48], [63], [47, 39, 31, 23, 15, 7], [62], [], [], [46, 37, 28, 19, 10, 1]], 
    56: [[57, 58, 59, 60, 61, 62, 63], [], [], [48, 40, 32, 24, 16, 8, 0], [], [49, 42, 35, 28, 21, 14, 7], [], []], 
    57: [[58, 59, 60, 61, 62, 63], [56], [], [49, 41, 33, 25, 17, 9, 1], [], [50, 43, 36, 29, 22, 15], [], [48]], 
    58: [[59, 60, 61, 62, 63], [57, 56], [], [50, 42, 34, 26, 18, 10, 2], [], [51, 44, 37, 30, 23], [], [49, 40]], 
    59: [[60, 61, 62, 63], [58, 57, 56], [], [51, 43, 35, 27, 19, 11, 3], [], [52, 45, 38, 31], [], [50, 41, 32]], 
    60: [[61, 62, 63], [59, 58, 57, 56], [], [52, 44, 36, 28, 20, 12, 4], [], [53, 46, 39], [], [51, 42, 33, 24]], 
    61: [[62, 63], [60, 59, 58, 57, 56], [], [53, 45, 37, 29, 21, 13, 5], [], [54, 47], [], [52, 43, 34, 25, 16]], 
    62: [[63], [61, 60, 59, 58, 57, 56], [], [54, 46, 38, 30, 22, 14, 6], [], [55], [], [53, 44, 35, 26, 17, 8]], 
    63: [[], [62, 61, 60, 59, 58, 57, 56], [], [55, 47, 39, 31, 23, 15, 7], [], [], [], [54, 45, 36, 27, 18, 9, 0]]
}
cache = {}

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
    
    quickMove(board, plr)

    sequence(board, plr, moves, tokens)

def quickMove(board, tkn):
    tokencount = 64-board.count(".")
    
    if 64-tokencount < 11:
        # negamax
        fm = q_pm(board, tkn)
        print(f"score {list(fm[0])[0]}")
        nm = negamax(board, tkn)
        print(f"Min score: {nm[0]}; move sequence: {nm[1:]}")
    else:
        fm = possible_moves(board, tkn)
        other = 'x' if tkn == 'o' else 'o'
        
        origopp_moves = possible_moves(board, other)
        edges = {0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63}
        corners = {0: {1, 8, 9}, 7: {6, 14, 15}, 56: {48, 49, 57}, 63: {54, 55, 62}}
        controlofcenter = {18,19,20,21,26,27,28,29,34,35,36,37,42,43,44,45}

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
            elif tokencount < 16:
                if move in controlofcenter:
                    weight += 1

            moves.append( (weight, move) )
        
        return sorted(moves, reverse=True)[0][1]

def negamax(brd, tkn):
    if brd+tkn in cache:
        return cache[brd+tkn]["nm"]

    mymoves, myrplmnts = q_pm(brd, tkn)
    enemy = "x" if tkn == "o" else "o"
    if len(mymoves) == 0:
        hermoves, _ = q_pm(brd, enemy)
        if len(hermoves) == 0:
            return [brd.count(tkn)-brd.count(enemy)]
        nm = negamax(brd, enemy)
        return [-nm[0]]+nm[1:]+[-1]
        
    bestSoFar = [-65]

    for mv in mymoves:
        newBrd = q_play(brd,tkn,mv,myrplmnts)
        nm = negamax(newBrd, enemy)
        if -nm[0] > bestSoFar[0]:
            bestSoFar = [-nm[0]]+nm[1:]+[mv]
    
    cache[brd+tkn] = {
        "nm": bestSoFar
    }

    return bestSoFar

def q_pm(brd, tkn):
    moves = set()
    rplmnt = {}
    other = "x" if tkn == "o" else "o"
    tknct = 64-brd.count(".")

    if tknct < 32:
        for i in range(64):
            if brd[i] == tkn:
                for direction in flips[i]:
                    for j,nbr in enumerate(direction):
                        if brd[nbr] == tkn: break
                        if j == 0 and brd[nbr] == ".": break
                        if brd[nbr] == "." and brd[direction[j-1]] == other:
                            moves.add(nbr)
                            if nbr in rplmnt:
                                rplmnt[nbr].extend(direction[:j+1])
                            else:
                                rplmnt[nbr] = direction[:j+1]
                            break
    else:
        for i in range(64):
            if brd[i] == ".":
                for direction in flips[i]:
                    for j,nbr in enumerate(direction):
                        if brd[nbr] == ".": break
                        if j == 0 and brd[nbr] == tkn: break
                        if brd[nbr] == tkn and brd[direction[j-1]] == other:
                            moves.add(i)
                            if i in rplmnt:
                                rplmnt[i].extend(direction[:j])
                            else:
                                rplmnt[i] = direction[:j]
                            break
                                
    return (moves, rplmnt)

def q_play(board, plr, move, replacements):
    for i in replacements[move]:
        board = board[:i] + plr + board[i+1:]
    board = board[:move] + plr + board[move+1:]
    return "".join(board)

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

