flips = {
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
HLLIM = 10

def q_pm(brd, tkn, rpn=True):
    # Implement this method
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
                            if rpn:
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
                            if rpn:
                                if i in rplmnt:
                                    rplmnt[i].extend(direction[:j])
                                else:
                                    rplmnt[i] = direction[:j]
                            break
    
    if rpn:
        return (moves, rplmnt)
    else:
        return moves
    return 0


def quickMove(board, tkn):
    if not board: global HLLIM; HLLIM = tkn; return
    tokencount = 64-board.count(".")
    
    if 64-tokencount <= HLLIM:
        # negamax
        ab = alphabeta(board, tkn, -65, 65)
        print(f"Min score: {ab[0]}; move sequence: {ab[1:]}")
        return ab[-1]
    elif 64-tokencount > HLLIM and tokencount > 8:
        midgame = abmidgame(board, tkn, -65, 65, 6)
        print(f"Min score: {midgame[0]}; move sequence: {midgame[1:]}")
        return midgame[-1]
        # if tokencount < 25:
        #     midgame = abmidgame(board, tkn, -65, 65, 6)
        #     print(f"Min score: {midgame[0]}; move sequence: {midgame[1:]}")
        #     return midgame[-1]
        # elif tokencount < 32:
        #     midgame = abmidgame(board, tkn, -65, 65, 5)
        #     print(f"Min score: {midgame[0]}; move sequence: {midgame[1:]}")
        #     return midgame[-1]
        # else:
        #     midgame = abmidgame(board, tkn, -65, 65, 4)
        #     print(f"Min score: {midgame[0]}; move sequence: {midgame[1:]}")
        #     return midgame[-1]
        # else:
        #     midgame = abmidgame(board, tkn, -65, 65, 3)
        #     print(f"Min score: {midgame[0]}; move sequence: {midgame[1:]}")
        #     return midgame[-1]
    else:
        return rothumb(board, tkn, tokencount)

def alphabeta(brd, tkn, lower, upper):
    mymoves, myrplmnts = q_pm(brd, tkn)
    enemy = "x" if tkn == "o" else "o"
    if len(mymoves) == 0:
        if len(q_pm(brd, enemy, False)) == 0:
            return [brd.count(tkn)-brd.count(enemy)]
        ab = alphabeta(brd, enemy, -upper, -lower)
        return [-ab[0]]+ab[1:]+[-1]

    bestSoFar = [lower-1]
    mymoves = ordering(mymoves, myrplmnts, brd, tkn)
    for mv in mymoves:
        ab = alphabeta(q_play(brd, tkn, mv, myrplmnts), enemy, -upper, -lower)
        score = -ab[0]
        if score < lower: continue
        if score > upper: return [score]
        bestSoFar = [score]+ab[1:]+[mv]
        lower = score+1
        # print(f"Min score: {bestSoFar[0]}; move sequence: {bestSoFar[1:]}")
    
    return bestSoFar

def abmidgame(brd, tkn, lower, upper, level):
    mymoves, myrplmnts = q_pm(brd, tkn)
    enemy = "x" if tkn == "o" else "o"
    if level == 0:
        return [bdeval(brd, tkn)]
    if len(mymoves) == 0:
        if len(q_pm(brd, enemy, False)) == 0:
            return [bdeval(brd,tkn)+37]#[(brd.count(tkn)-brd.count(enemy))*37.3]
        ab = abmidgame(brd, enemy, -upper, -lower, level-1)
        return [-ab[0]]+ab[1:]+[-1]

    mymoves = ordering(mymoves, myrplmnts, brd, tkn)
    bestSoFar = [lower-1]
    for mv in mymoves:
        ab = abmidgame(q_play(brd, tkn, mv, myrplmnts), enemy, -upper, -lower, level-1)
        score = -ab[0]
        if score < lower: continue
        if score > upper: return [score]
        bestSoFar = [score]+ab[1:]+[mv]
        lower = score+1
        # print(f"Min score: {bestSoFar[0]}; move sequence: {bestSoFar[1:]}")
    
    return bestSoFar

def bdeval(bd, tkn):
    w = 3
    other = "o" if tkn == "x" else "x"
    mycorners = sum(1 for i in {0,7,56,63} if bd[i]==tkn)
    hercorners = sum(1 for i in {0,7,56,63} if bd[i]==other)
    mysedges = sum(1 for i in enumerate(bd) if safe_edge(i,bd,tkn))
    hersedges = sum(1 for i in enumerate(bd) if safe_edge(i,bd,other))
    return w*(mycorners-hercorners)+(mysedges-hersedges)

def ordering(fm, rm, board, tkn):
    other = 'x' if tkn == 'o' else 'o'
    
    origopp_moves = q_pm(board, other, False)
    edges = {0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63}
    corners = {0: {1, 8, 9}, 7: {6, 14, 15}, 56: {48, 49, 57}, 63: {54, 55, 62}}
    
    moves = []

    for move in fm:
        weight = 0
        nb = q_play(board, tkn, move, rm)

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

        opps_moves = q_pm(nb, other, False)
        if len(opps_moves) == 0:
            weight += 65
        if len(opps_moves) < len(origopp_moves):
            weight += 25

        moves.append( (weight, move) )
    
    return [move[1] for move in sorted(moves, reverse=True)]

def safe_edge(move, board, tkn):
    other = "x" if tkn == "o" else "o"
    top = {1,2,3,4,5,6}
    left = {8,16,24,32,40,48}
    right = {15,23,31,39,47,55}
    bottom = {57,58,59,60,61,62}

    if move in top:
        if board[0] == tkn:
            for i in range(0, move):
                if board[i] == tkn:
                    continue
                if board[i] == other:
                    continue
                if board[i] == " ":
                    return False
            return True
        if board[7] == tkn:
            for i in range(move+1, 7):
                if board[i] == tkn:
                    continue
                if board[i] == other:
                    continue
                if board[i] == " ":
                    return False
            return True
    if move in left:
        if board[0] == tkn:
            for i in range(0,move,8):
                if board[i] == tkn:
                    continue
                if board[i] == other:
                    continue
                if board[i] == " ":
                    return False
            return True
        if board[56] == tkn:
            for i in range(move+8,56,8):
                if board[i] == tkn:
                    continue
                if board[i] == other:
                    continue
                if board[i] == " ":
                    return False
            return True
    if move in right:
        if board[7] == tkn:
            for i in range(7,move,8):
                if board[i] == tkn:
                    continue
                if board[i] == other:
                    continue
                if board[i] == " ":
                    return False
            return True
        if board[63] == tkn:
            for i in range(move+8,63,8):
                if board[i] == tkn:
                    continue
                if board[i] == other:
                    continue
                if board[i] == " ":
                    return False
            return True
    if move in bottom:
        if board[56] == tkn:
            for i in range(56, move):
                if board[i] == tkn:
                    continue
                if board[i] == other:
                    continue
                if board[i] == " ":
                    return False
            return True
        if board[63] == tkn:
            for i in range(move+1, 63):
                if board[i] == tkn:
                    continue
                if board[i] == other:
                    continue
                if board[i] == " ":
                    return False
            return True
    return False

def rothumb(board, tkn, tokencount):
    fm, rm = q_pm(board, tkn)
    other = 'x' if tkn == 'o' else 'o'
    
    origopp_moves = q_pm(board, other, False)
    edges = {0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63}
    corners = {0: {1, 8, 9}, 7: {6, 14, 15}, 56: {48, 49, 57}, 63: {54, 55, 62}}
    controlofcenter = {18,19,20,21,26,27,28,29,34,35,36,37,42,43,44,45}

    moves = []

    for move in fm:
        weight = 0
        nb = q_play(board, tkn, move, rm)
        rm2 = set(rm[move])

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

        opps_moves = q_pm(nb, other, False)
        if len(opps_moves) == 0:
            weight += 65
        if len(opps_moves) < len(origopp_moves):
            weight += 25

        if tokencount < 28:
            if len(rm2) < 5:
                weight += 2
        elif tokencount > 32:
            if len(rm2) > 5:
                weight += 2
        elif tokencount < 16:
            if move in controlofcenter:
                weight += 1

        moves.append( (weight, move) )
    
    return sorted(moves, reverse=True)[0][1]

def q_play(board, plr, move, replacements):
    for i in set(replacements[move]):
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

def stability(move, board, tkn):
    other = "x" if tkn == "o" else "o"
    
    cornerExists = False
    for i in {0,7,56,63}:
        if board[i] == tkn:
            cornerExists = True
            break
    if not cornerExists:
        return False

    protected = True
    for i in range(0, len(flips[move]), 2):
        p1 = flips[move][i]
        p1_hitsBorder = False
        p1_hitsOpposingDisc = False

        p2 = flips[move][i+1]
        p2_hitsBorder = False
        p2_hitsOpposingDisc = False

        for i,n in enumerate(p1):
            if board[n] == tkn and i == len(p1)-1:
                p1_hitsBorder = True
                break
            if board[n] == " ":
                p2_hitsBorder = False
                p2_hitsOpposingDisc = False
                break
            if i-1 >= 0:
                if board[n] == other and board[p1[i-1]] == tkn:
                    p1_hitsOpposingDisc = True
                    break
            else:
                if board[n] == other:
                    p1_hitsOpposingDisc = True
                    break

        for i,n in enumerate(p2):
            if board[n] == tkn and i == len(p2)-1:
                p2_hitsBorder = True
                break
            if board[n] == " ":
                p2_hitsBorder = False
                p2_hitsOpposingDisc = False
                break
            if i-1 >= 0:
                if board[n] == other and board[p2[i-1]] == tkn:
                    p2_hitsOpposingDisc = True
                    break
            else:
                if board[n] == other:
                    p2_hitsOpposingDisc = True
                    break

        if p1_hitsBorder or p2_hitsBorder:
            protected = True
        else:
            protected = False
            break

        if p1_hitsOpposingDisc and p2_hitsOpposingDisc:
            protected = True
        else:
            protected = False
            break
        
    return protected

class Strategy:
    # Uncomment the below flags as needed
    # logging = True
    # uses_10x10_board = True
    # uses_10x10_moves = True

    def best_strategy(self, board, player, best_move, still_running, time_limit):
        tokencount = 64-board.count(".")
        
        best_move.value=rothumb(board, player, tokencount)
        
        if 64-tokencount <= HLLIM:
            # negamax
            ab = alphabeta(board, player, -65, 65)
            best_move.value=ab[-1]
        elif 64-tokencount > HLLIM and tokencount > 8:
            if tokencount < 25:
                midgame = abmidgame(board, player, -65, 65, 6)
                best_move.value=midgame[-1]
            elif tokencount < 32:
                midgame = abmidgame(board, player, -65, 65, 5)
                best_move.value=midgame[-1]
            elif tokencount < 43:
                midgame = abmidgame(board, player, -65, 65, 4)
                best_move.value=midgame[-1]
            else:
                midgame = abmidgame(board, player, -65, 65, 3)
                best_move.value=midgame[-1]
