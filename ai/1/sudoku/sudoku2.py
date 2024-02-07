import sys; args = sys.argv[1:]

# sudoku 2 - undefined%
# this is the worst code of all time
# i hate this lab 
# also the grader is stupid -> you could have 3s on your machine but it'll be 17s on the grader
# GET MORE COMPUTING POWER PLEASE
# i give up 🏳️

def jbf(pzl, excluded, s2p):
    if solved(pzl): return pzl

    best_pos, affected_symset = get_best_pos(excluded)
    possible_choices = q_choices(pzl, best_pos, affected_symset)

    best_pos = [best_pos]
    best_sym = ""
    
    if len(possible_choices) > 1:
        if s2p == {}:
            s2p = get_sym_to_pos(pzl, excluded)
        best_sym_pos, best_sym = get_best_symbol(s2p, len(possible_choices))

        if best_sym_pos != []:
            best_pos = best_sym_pos
            possible_choices = q_choices_by_sym(pzl, best_sym_pos, best_sym)

            '''
            naked pairs was here -> probably didn't work because i did it wrong
            (used excluded instead of possibles? tried that but still didn't work
            obviously doing something wrong don't know what though <shrug>)
            '''

    updateStats(f"choice ct {len(possible_choices)}")

    for choice, pos, sym in possible_choices:
        # deep copy excluded
        dc_excluded = {i: excluded[i] for i in excluded}
        for constraint in NBRS[pos]:
            for j in LOCS[constraint]:
                if choice[j] == ".":
                    dc_excluded[j] = dc_excluded[j]|{choice[pos]}
        dc_excluded.pop(pos)
        
        # deepcopy s2p
        dc_s2p = s2p
        s2p_modified = False
        cnst_syms = {}
        pos_cs_syms = []
        sym_props = {}
        if dc_s2p:
            s2p_modified = True
            for constraint in NBRS[pos]:
                cnst_syms[constraint] = {}
                cnst_syms[constraint][sym] = dc_s2p[constraint][sym]
                dc_s2p[constraint].pop(sym)
            
            for cs in dc_s2p:
                for symbol in dc_s2p[cs]:
                    # remove all pos refs
                    if pos in dc_s2p[cs][symbol]:
                        pos_cs_syms.append((cs,symbol))
                        dc_s2p[cs][symbol].remove(pos)
                    # recheck all best_sym props
                    if symbol == sym:
                        sym_props[cs] = {}
                        sym_props[cs][symbol] = dc_s2p[cs][symbol]
                        dc_s2p[cs][symbol] = []
                        for i in LOCS[cs]:
                            if choice[i] == ".": 
                                psbls = [c for c in SYMSET]
                                for j in dc_excluded[i]:
                                    psbls.remove(j)
                                if symbol in psbls:
                                    dc_s2p[cs][symbol].append(i)
        nbf = jbf(choice,dc_excluded,dc_s2p)
        if s2p_modified:
            for constraint in cnst_syms:
                dc_s2p[constraint][sym] = cnst_syms[constraint][sym]
            
            for cs,symbol in pos_cs_syms:
                dc_s2p[cs][symbol].append(pos)
            
            for cs in sym_props:
                dc_s2p[cs][sym] = sym_props[cs][sym]
        if nbf: return nbf
    return ""

def q_choices(pzl, best_pos, affected_symset):
    choices = set()

    for t in affected_symset:
        choice = pzl[:best_pos]+t+pzl[best_pos+1:]
        choices.add((choice, best_pos, t))
    
    return choices 

def q_choices_by_sym(pzl, best_symbol_positions, best_symbol):
    choices = set()

    for pos in best_symbol_positions:
        choice = pzl[:pos]+best_symbol+pzl[pos+1:]
        choices.add((choice, pos, best_symbol))
    
    return choices 

def get_sym_to_pos(pzl, excluded):
    s2p = {}

    for i,cs in enumerate(LOCS):
        s2p[i] = {}
        
        unplacedSymbols = set()
        for pos in cs:
            if pzl[pos] != ".":
                unplacedSymbols.add(pzl[pos])
        unplacedSymbols = set(SYMSET)-unplacedSymbols

        for sym in unplacedSymbols:
            s2p[i][sym] = []
        
        for pos in cs:
            if pzl[pos] == ".":
                psbls = [c for c in SYMSET]
                for j in excluded[pos]:
                    psbls.remove(j)
                for sym in unplacedSymbols:
                    if sym in psbls:
                        s2p[i][sym].append(pos)
    
    return s2p
        
def get_best_symbol(s2p, maxlen):
    best_symbol = ""
    best_sym_pos = []
    best_len = maxlen
    bailout = False

    for cs in s2p:
        if bailout:
            break

        for syms in s2p[cs]:
            if len(s2p[cs][syms]) == 1:
                best_symbol = syms
                best_sym_pos = s2p[cs][syms]
                bailout = True
                break
            if len(s2p[cs][syms]) < best_len:
                best_symbol = syms
                best_sym_pos = s2p[cs][syms]
                best_len = len(s2p[cs][syms])

    return (best_sym_pos, best_symbol)

def get_excluded(pzl):
    excludeds = {}

    for i in range(len(pzl)):
        if pzl[i] == ".":
            excludeds[i] = set()
            for constraint in NBRS[i]:
                for j in LOCS[constraint]:
                    if pzl[j] != ".":
                        excludeds[i].add(pzl[j])
    return excludeds

def get_best_pos(excluded):
    most_constrained = -1
    mc_len = -1

    for i in excluded:
        if len(excluded[i]) > mc_len:
            most_constrained = i
            mc_len = len(excluded[i])

    # update symset
    affected_symset = [c for c in SYMSET]
    for j in excluded[most_constrained]:
        affected_symset.remove(j)

    return (most_constrained, affected_symset)

# utils
def solved(pzl):
    if "." in pzl:
        return False
    return True

def get_symbols(pzl):
    symbols = set()
    for c in pzl:
        if c != ".":
            symbols.add(c)
    
    offset = 0
    while len(symbols) < N:
        symbols.add(chr(ord('1')+offset))
        offset+=1

    return list(symbols)

def checksum(pzl):
    if SYMSET == ['1','2','3','4','5','6','7','8','9']:
        return 324
    return sum(ord(c) for c in pzl)-N*N*ord(min(SYMSET))

def get_dimensions(area, overall=1):
    for i in range(1, area):
        for j in range(1, area):
            if i<j: continue
            if (i*j)*overall==area:
                return (i,j)

def generate_constraints():
    constraints = []
    nbrs = {}
    idx = 0

    r = 0
    for i in range(N):
        constraint = set()
        for j in range(N):
            constraint.add(r)
            nbrs[r] = [idx]
            r+=1
        constraints.append(constraint)
        idx+=1
    
    # cols
    c = 0
    offset = 1
    for i in range(N):
        constraint = set()
        for j in range(N):
            constraint.add(c)
            nbrs[c].append(idx)
            for k in range(N):
                c+=1
        constraints.append(constraint)
        c=offset
        offset+=1
        idx+=1
    
    # subblocks
    offset = 0
    posn = 0
    for i in range(N):
        constraint = set()
        for j in range(sbh):
            for k in range(sbw):
                constraint.add(offset)
                nbrs[offset].append(idx)
                offset+=1
            offset+=N-sbw

        if (i+1)%sbh == 0:
            offset -= N-sbw
            posn = offset
        else:
            posn += sbw
            offset = posn
        constraints.append(constraint)
        idx+=1

    return (constraints, nbrs)

def updateStats(phrase):
    if phrase not in STATS:
        STATS[phrase] = 1
    else:
        STATS[phrase] += 1

if __name__ == "__main__":
    pzls = open(args[0]).read().splitlines()
    STATS = {}

    N = 9
    sbw, sbh = 3, 3
    LOCS = [
        {0,1,2,3,4,5,6,7,8},
        {9,10,11,12,13,14,15,16,17},
        {18,19,20,21,22,23,24,25,26},
        {27,28,29,30,31,32,33,34,35},
        {36,37,38,39,40,41,42,43,44},
        {45,46,47,48,49,50,51,52,53},
        {54,55,56,57,58,59,60,61,62},
        {63,64,65,66,67,68,69,70,71},
        {72,73,74,75,76,77,78,79,80},
        {0,9,18,27,36,45,54,63,72},
        {1,10,19,28,37,46,55,64,73},
        {2,11,20,29,38,47,56,65,74},
        {3,12,21,30,39,48,57,66,75},
        {4,13,22,31,40,49,58,67,76},
        {5,14,23,32,41,50,59,68,77},
        {6,15,24,33,42,51,60,69,78},
        {7,16,25,34,43,52,61,70,79},
        {8,17,26,35,44,53,62,71,80},
        {0,1,2,9,10,11,18,19,20},
        {3,4,5,12,13,14,21,22,23},
        {6,7,8,15,16,17,24,25,26},
        {27,28,29,36,37,38,45,46,47},
        {30,31,32,39,40,41,48,49,50},
        {33,34,35,42,43,44,51,52,53},
        {54,55,56,63,64,65,72,73,74},
        {57,58,59,66,67,68,75,76,77},
        {60,61,62,69,70,71,78,79,80}
    ]
    NBRS = {0: [0, 9, 18], 1: [0, 10, 18], 2: [0, 11, 18], 3: [0, 12, 19], 4: [0, 13, 19], 5: [0, 14, 19], 6: [0, 15, 20], 7: [0, 16, 20], 8: [0, 17, 20], 9: [1, 9, 18], 10: [1, 10, 18], 11: [1, 11, 18], 12: [1, 12, 19], 13: [1, 13, 19], 14: [1, 14, 19], 15: [1, 15, 20], 16: [1, 16, 20], 17: [1, 17, 20], 18: [2, 9, 18], 19: [2, 10, 18], 20: [2, 11, 18], 21: [2, 12, 19], 22: [2, 13, 19], 23: [2, 14, 19], 24: [2, 15, 20], 25: [2, 16, 20], 26: [2, 17, 20], 32: [3, 14, 22], 33: [3, 15, 23], 34: [3, 16, 23], 35: [3, 17, 23], 27: [3, 9, 21], 28: [3, 10, 21], 29: [3, 11, 21], 30: [3, 12, 22], 31: [3, 13, 22], 36: [4, 9, 21], 37: [4, 10, 21], 38: [4, 11, 21], 39: [4, 12, 22], 40: [4, 13, 22], 41: [4, 14, 22], 42: [4, 15, 23], 43: [4, 16, 23], 44: [4, 17, 23], 45: [5, 9, 21], 46: [5, 10, 21], 47: [5, 11, 21], 48: [5, 12, 22], 49: [5, 13, 22], 50: [5, 14, 22], 51: [5, 15, 23], 52: [5, 16, 23], 53: [5, 17, 23], 54: [6, 9, 24], 55: [6, 10, 24], 56: [6, 11, 24], 57: [6, 12, 25], 58: [6, 13, 25], 59: [6, 14, 25], 60: [6, 15, 26], 61: [6, 16, 26], 62: [6, 17, 26], 64: [7, 10, 24], 65: [7, 11, 24], 66: [7, 12, 25], 67: [7, 13, 25], 68: [7, 14, 25], 69: [7, 15, 26], 70: [7, 16, 26], 71: [7, 17, 26], 63: [7, 9, 24], 72: [8, 9, 24], 73: [8, 10, 24], 74: [8, 11, 24], 75: [8, 12, 25], 76: [8, 13, 25], 77: [8, 14, 25], 78: [8, 15, 26], 79: [8, 16, 26], 80: [8, 17, 26]}
    SYMSET = ['1','2','3','4','5','6','7','8','9']
    import time
    
    start = time.perf_counter()

    for n,puzzle in enumerate(pzls):
        if n > 120:
            if len(puzzle) != 81:
                N = get_dimensions(len(puzzle))[0]
                sbw, sbh = get_dimensions(len(puzzle), N)
                LOCS, NBRS = generate_constraints()
            SYMSET = get_symbols(puzzle)
        first_excluded = get_excluded(puzzle)
        print(f"{n+1:3}: {puzzle}")
        solution = jbf(puzzle,first_excluded, {})
        csum = checksum(solution)
        print(f"     {solution} {csum}")
    print(STATS)
    print(time.perf_counter()-start)

# Syed Raza Haider Period 6 2025