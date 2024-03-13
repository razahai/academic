import sys; args = sys.argv[1:]

# Crossword 2 - undefined

BLOCKCHAR = "#"
OPENCHAR = "-"
EMPTYCHAR = "."

def main():
    global ROWS, COLS, NUM_OF_BLKING_SQ

    seeds = []
    dct = [word for word in open(args[0]).read().splitlines() if len(word) > 2]

    len_dct = build_dcts(dct)
            
    for i in range(1, len(args)):
        if args[i][0].lower() == "v" or args[i][0].lower() == "h":
            seeds.append(args[i])
        elif "x" in args[i]:
            ROWS, COLS = map(int, args[i].split("x"))           
        else:
            NUM_OF_BLKING_SQ = int(args[i])

    base_puzzle = make_base_puzzle(seeds)
    # check before even starting the recursion
    preliminary_rules(base_puzzle)
    puzzle = construct_crossword(base_puzzle)
    puzzle = fill_puzzle(puzzle, len_dct)
    display(puzzle)

def fill_puzzle(puzzle, len_dct):
    entries = get_entries(puzzle)
    
    filled_puzzle = _fill_puzzle_bf(puzzle, entries, len_dct)

    return filled_puzzle

def _fill_puzzle_bf(puzzle, entries, len_dct):
    if len(entries) == 0: 
        return puzzle

    display(puzzle)

    entry = entries[0]
    
    if len(entry) in len_dct:
        for word in len_dct[len(entry)]:
            invalid_word = False
            for i,let in enumerate(entry):
                if puzzle[let] != OPENCHAR:
                    if word[i].lower() != puzzle[let]:
                        invalid_word = True
                        break
            if invalid_word: continue
            
            npz = [*puzzle]

            for i in range(len(entry)):
                npz[entry[i]] = word[i]
            nld = {c: len_dct[c] for c in len_dct}
            nld[len(entry)] = [k for k in len_dct[len(entry)] if k != word]
            nent = [netr for netr in entries if netr != entry]
            nbr = _fill_puzzle_bf(npz, nent, nld)
            if nbr: return nbr
    return ""

def get_entries(puzzle):
    space = []
    spaces = []

    for i in range(len(puzzle)):
        if puzzle[i] == OPENCHAR or (puzzle[i] != BLOCKCHAR and puzzle[i] != OPENCHAR):
            space.append(i)
        if puzzle[i] == BLOCKCHAR:
            if space: spaces.append(space)
            space = []
        elif i % COLS == COLS-1:
            if space: spaces.append(space)
            space = []
    
    for c in range(COLS):
        for i in range(c, len(puzzle), COLS):
            if puzzle[i] == OPENCHAR or (puzzle[i] != BLOCKCHAR and puzzle[i] != OPENCHAR):
                space.append(i)
            if puzzle[i] == BLOCKCHAR:
                if space: spaces.append(space)
                space = []
            elif i // COLS == ROWS-1:
                if space: spaces.append(space)
                space = [] 

    spaces.sort(key=lambda sp: len(sp), reverse=True)

    return spaces  

def build_dcts(dct):
    len_dct = {}
    
    for word in dct:
        if len(word) in len_dct:
            len_dct[len(word)].append(word)
        else:
            len_dct[len(word)] = [word]

    return len_dct

def construct_crossword(puzzle):
    apply_rules(puzzle)
    
    blksq = puzzle.count(BLOCKCHAR)
    if blksq > NUM_OF_BLKING_SQ:
        # invalid
        return "" 
    elif blksq == NUM_OF_BLKING_SQ:
        # solved
        if not invalid(puzzle):
            return [p.replace(".","-") for p in puzzle]
    
    choices = []
    
    for k in range(len(puzzle)):
        if puzzle[k] == EMPTYCHAR and puzzle[-k-1] == EMPTYCHAR:
            blocked = [*puzzle]
            blocked[k] = BLOCKCHAR
            blocked[-k-1] = BLOCKCHAR
            choices.append(blocked)

            opened = [*puzzle]
            opened[k] = OPENCHAR
            opened[-k-1] = OPENCHAR
            choices.append(opened)
            break

    for choice in choices:
        nbr = construct_crossword(choice)
        if nbr: return nbr
    
    return ""

def invalid(puzzle):
    # check for <len(2) words
    for k in range(len(puzzle)):
        if puzzle[k] == BLOCKCHAR:
            if k-3 >= 0 and (k-3)//COLS==k//COLS:
                if puzzle[k-3] == BLOCKCHAR and not BLOCKCHAR*2 == "".join(puzzle[k-2:k]):
                    return True
            if k-1 >= 0 and (k-1)%COLS==0:
                if not puzzle[k-1] == BLOCKCHAR:
                    return True
            if k-2 >= 0 and (k-2)%COLS==0:
                if not (puzzle[k-1] == BLOCKCHAR or puzzle[k-2] == BLOCKCHAR):
                    return True

            if k+3 < len(puzzle) and (k+3)//COLS==k//COLS:
                if puzzle[k+3] == BLOCKCHAR and not BLOCKCHAR*2 == "".join(puzzle[k+1:k+3]):
                    return True
            if k+1 < len(puzzle) and (k+1)%COLS==COLS-1:
                if not puzzle[k+1] == BLOCKCHAR:
                    return True
            if k+2 < len(puzzle) and (k+2)%COLS==COLS-1:
                if not (puzzle[k+1] == BLOCKCHAR or puzzle[k+2] == BLOCKCHAR):
                    return True
                
            if k+COLS*3 < len(puzzle):
                if puzzle[k+COLS*3] == BLOCKCHAR and not BLOCKCHAR*2 == "".join(puzzle[k+COLS:k+COLS*3:COLS]):
                    return True
            if k+COLS < len(puzzle) and (k+COLS)//COLS==ROWS-1:
                if not puzzle[k+COLS] == BLOCKCHAR:
                    return True
            if k+COLS*2 < len(puzzle) and (k+COLS*2)//COLS==ROWS-1:
                if not (puzzle[k+COLS] == BLOCKCHAR or puzzle[k+COLS*2] == BLOCKCHAR):
                    return True
            
            if k-COLS*3 >= 0:
                if puzzle[k-COLS*3] == BLOCKCHAR and not BLOCKCHAR*2 == "".join(puzzle[k-COLS*2:k:COLS]):
                    return True
            if k-COLS >= 0 and (k-COLS)//COLS==0:
                if not puzzle[k-COLS] == BLOCKCHAR:
                    return True
            if k-COLS*2 < len(puzzle) and (k-COLS*2)//COLS==0:
                if not (puzzle[k-COLS] == BLOCKCHAR or puzzle[k-COLS*2] == BLOCKCHAR):
                    return True

    if disjointed(puzzle):
        return True
    return False

def preliminary_rules(puzzle):
    if ROWS*COLS == NUM_OF_BLKING_SQ:
        puzzle[:] = ["#"]*(ROWS*COLS)
        return
    if ROWS%2 + COLS%2 + NUM_OF_BLKING_SQ%2 == 3:
        safe_set(puzzle, (len(puzzle)-1)//2, BLOCKCHAR)
    elif ROWS%2 + COLS%2 == 2:
        safe_set(puzzle, (len(puzzle)-1)//2, OPENCHAR)  

def apply_rules(puzzle):
    q = [i for i in range(len(puzzle)) if puzzle[i] == BLOCKCHAR]

    # center check
    if puzzle[(len(puzzle)-1)//2] == OPENCHAR:
        safe_set(puzzle, ((len(puzzle)-1)//2)-1, OPENCHAR)
        safe_set(puzzle, ((len(puzzle)-1)//2)+1, OPENCHAR)
        safe_set(puzzle, ((len(puzzle)-1)//2)+COLS, OPENCHAR)
        safe_set(puzzle, ((len(puzzle)-1)//2)-COLS, OPENCHAR)

    while q:
        ind = q.pop()
        # #..# and #..| checker 
        h__h(puzzle, ind, q)
        # #~_~# and #_.. checker
        h_o_h(puzzle, ind)
        # edge checker
        edge_rules(puzzle)
    
    regions = get_disjoint_regions(puzzle)
    if len(regions) > 1:
        for r in regions:
            if puzzle.count(BLOCKCHAR)+len(r) > NUM_OF_BLKING_SQ:
                continue
            for k in r:
                safe_set(puzzle, k, BLOCKCHAR)



def edge_rules(puzzle):
    edgeinds = [i for i in range(len(puzzle)) if (not (puzzle[i] == EMPTYCHAR or puzzle[i] == BLOCKCHAR)) and (i%COLS == 0 or i%COLS == COLS-1 or i//COLS==ROWS-1 or i//COLS==0)]
    
    for ind in edgeinds:
        if ind%COLS == 0:
            # left
            if ind+2 < len(puzzle) and (ind+2)//COLS==ind//COLS:
                safe_set(puzzle, ind+1, OPENCHAR)
                safe_set(puzzle, ind+2, OPENCHAR)
        if ind%COLS == COLS-1:
            # right
            if ind-2 >= 0 and (ind-2)//COLS==ind//COLS:
                safe_set(puzzle, ind-1, OPENCHAR)
                safe_set(puzzle, ind-2, OPENCHAR)
        if ind//COLS==ROWS-1:
            # bot
            if ind-COLS*2 >= 0:
                safe_set(puzzle, ind-COLS, OPENCHAR)
                safe_set(puzzle, ind-COLS*2, OPENCHAR)
        if ind//COLS==0:
            # top
            if ind+COLS*2 < len(puzzle):
                safe_set(puzzle, ind+COLS, OPENCHAR)
                safe_set(puzzle, ind+COLS*2, OPENCHAR)


def h_o_h(puzzle, ind):
    # for h.o.h
    # right
    if ind+4 < len(puzzle) and (ind+4)//COLS==(ind)//COLS:
        middle = puzzle[ind+1:ind+4]
        if puzzle[ind+4] == BLOCKCHAR and (not BLOCKCHAR in middle or EMPTYCHAR*3 == middle):
            safe_set(puzzle, ind+1, OPENCHAR)
            safe_set(puzzle, ind+2, OPENCHAR)
            safe_set(puzzle, ind+3, OPENCHAR)
    # left
    if ind-4 >= 0 and (ind-4)//COLS==(ind)//COLS:
        middle = puzzle[ind-4:ind]
        if puzzle[ind-4] == BLOCKCHAR and (not BLOCKCHAR in middle or EMPTYCHAR*3 == middle):
            safe_set(puzzle, ind-1, OPENCHAR)
            safe_set(puzzle, ind-2, OPENCHAR)
            safe_set(puzzle, ind-3, OPENCHAR)
    # bot
    if ind+COLS*4 < len(puzzle):
        middle = puzzle[ind:ind+COLS*4:COLS]
        if puzzle[ind+COLS*4] == BLOCKCHAR and (not BLOCKCHAR in middle or EMPTYCHAR*3 == middle):
            safe_set(puzzle, ind+COLS*2, OPENCHAR)
            safe_set(puzzle, ind+COLS*2, OPENCHAR)
            safe_set(puzzle, ind+COLS*3, OPENCHAR)
    # top
    if ind-COLS*4 >= 0:
        middle = puzzle[ind-COLS*4:ind:COLS]
        if puzzle[ind-COLS*4] == BLOCKCHAR and (not BLOCKCHAR in middle or EMPTYCHAR*3 == middle):
            safe_set(puzzle, ind-COLS, OPENCHAR)
            safe_set(puzzle, ind-COLS*2, OPENCHAR)
            safe_set(puzzle, ind-COLS*3, OPENCHAR)
    
    # for #o..
    # right
    if ind+3 < len(puzzle) and (ind+3)//COLS==(ind)//COLS:
        if not(puzzle[ind+1] == EMPTYCHAR or puzzle[ind+1] == BLOCKCHAR):
            safe_set(puzzle, ind+2, OPENCHAR)
            safe_set(puzzle, ind+3, OPENCHAR)
    # left
    if ind-3 >= 0 and (ind-3)//COLS==(ind)//COLS:
        if not(puzzle[ind-1] == EMPTYCHAR or puzzle[ind-1] == BLOCKCHAR):
            safe_set(puzzle, ind-2, OPENCHAR)
            safe_set(puzzle, ind-3, OPENCHAR)
    # bot
    if ind+COLS*3 < len(puzzle):
        if not(puzzle[ind+COLS] == EMPTYCHAR or puzzle[ind+COLS] == BLOCKCHAR):
            safe_set(puzzle, ind+COLS*2, OPENCHAR)
            safe_set(puzzle, ind+COLS*3, OPENCHAR)
    # top
    if ind-COLS*3 >= 0:
        if not(puzzle[ind-COLS] == EMPTYCHAR or puzzle[ind-COLS] == BLOCKCHAR):
            safe_set(puzzle, ind-COLS*2, OPENCHAR)
            safe_set(puzzle, ind-COLS*3, OPENCHAR)

def h__h(puzzle, ind, q):
    # bot
    if ind+COLS*3 < len(puzzle):
        if puzzle[ind+COLS*3] == BLOCKCHAR:
            if safe_set(puzzle, ind+COLS, BLOCKCHAR):
                q.append(ind+COLS)
            if safe_set(puzzle, ind+COLS*2, BLOCKCHAR):
                q.append(ind+COLS*2)
        elif puzzle[ind+COLS*2] == BLOCKCHAR:
            if safe_set(puzzle, ind+COLS, BLOCKCHAR):
                q.append(ind+COLS)
        elif (ind+COLS*2)//COLS == ROWS-1:
            if safe_set(puzzle, ind+COLS, BLOCKCHAR):
                q.append(ind+COLS)
            if safe_set(puzzle, ind+COLS*2, BLOCKCHAR):
                q.append(ind+COLS*2)
    elif ind+COLS*2 < len(puzzle):
        if puzzle[ind+COLS*2] == BLOCKCHAR:
            if safe_set(puzzle, ind+COLS, BLOCKCHAR):
                q.append(ind+COLS)
        elif (ind+COLS*2)//COLS == ROWS-1:
            if safe_set(puzzle, ind+COLS, BLOCKCHAR):
                q.append(ind+COLS)
            if safe_set(puzzle, ind+COLS*2, BLOCKCHAR):
                q.append(ind+COLS*2)
    

    # left   
    if ind-3 >= 0 and (ind-3)//COLS==(ind)//COLS:
        if puzzle[ind-3] == BLOCKCHAR:
            if safe_set(puzzle, ind-1, BLOCKCHAR):
                q.append(ind-1)
            if safe_set(puzzle, ind-2, BLOCKCHAR):
                q.append(ind-2)
        elif puzzle[ind-3] == BLOCKCHAR:
            if safe_set(puzzle, ind-1, BLOCKCHAR):
                q.append(ind-1)
        elif (ind-2)%COLS == COLS-1:
            if safe_set(puzzle, ind-1, BLOCKCHAR):
                q.append(ind-1)
            if safe_set(puzzle, ind-2, BLOCKCHAR):
                q.append(ind-2)
    elif ind-2 >= 0 and (ind-2)//COLS==(ind)//COLS:
        if puzzle[ind-2] == BLOCKCHAR:
            if safe_set(puzzle, ind-1, BLOCKCHAR):
                q.append(ind-1)
        elif (ind-2)%COLS == 0:
            if safe_set(puzzle, ind-1, BLOCKCHAR):
                q.append(ind-1)
            if safe_set(puzzle, ind-2, BLOCKCHAR):
                q.append(ind-2)


    if ind+3 < len(puzzle) and (ind+3)//COLS==(ind)//COLS:
        if puzzle[ind+3] == BLOCKCHAR:
            if safe_set(puzzle, ind+1, BLOCKCHAR):
                q.append(ind+1)
            if safe_set(puzzle, ind+2, BLOCKCHAR):
                q.append(ind+2)
        elif puzzle[ind+2] == BLOCKCHAR:
            if safe_set(puzzle, ind+1, BLOCKCHAR):
                q.append(ind+1)
        elif (ind+2)%COLS == COLS-1:
            if safe_set(puzzle, ind+1, BLOCKCHAR):
                q.append(ind+1)
            if safe_set(puzzle, ind+2, BLOCKCHAR):
                q.append(ind+2)
    elif ind+2 < len(puzzle) and (ind+2)//COLS==(ind)//COLS:
        if puzzle[ind+2] == BLOCKCHAR:
            if safe_set(puzzle, ind+1, BLOCKCHAR):
                q.append(ind+1)
        elif (ind+2)%COLS == COLS-1:
            if safe_set(puzzle, ind+1, BLOCKCHAR):
                q.append(ind+1)
            if safe_set(puzzle, ind+2, BLOCKCHAR):
                q.append(ind+2)

    # top
    if ind-COLS*3 >= 0:
        if puzzle[ind-COLS*3] == BLOCKCHAR:
            if safe_set(puzzle, ind-COLS, BLOCKCHAR):
                q.append(ind-COLS)
            if safe_set(puzzle, ind-COLS*2, BLOCKCHAR):
                q.append(ind-COLS*2)
        elif puzzle[ind-COLS*2] == BLOCKCHAR:
            if safe_set(puzzle, ind-COLS, BLOCKCHAR):
                q.append(ind-COLS)
        elif (ind-COLS*2)//COLS == 0:
            if safe_set(puzzle, ind-COLS, BLOCKCHAR):
                q.append(ind-COLS)
            if safe_set(puzzle, ind-COLS*2, BLOCKCHAR):
                q.append(ind-COLS*2)
    elif ind-COLS*2 >= 0:
        if puzzle[ind-COLS*2] == BLOCKCHAR:
            if safe_set(puzzle, ind-COLS, BLOCKCHAR):
                q.append(ind-COLS)
        elif (ind-COLS*2)//COLS == 0:
            if safe_set(puzzle, ind-COLS, BLOCKCHAR):
                q.append(ind-COLS)
            if safe_set(puzzle, ind-COLS*2, BLOCKCHAR):
                q.append(ind-COLS*2)

def disjointed(puzzle):
    q = []
    seen = set()
    opens = len(puzzle)-puzzle.count(BLOCKCHAR)

    for i in range(len(puzzle)):
        if not puzzle[i] == BLOCKCHAR:
            q.append(i)
            break

    while q:
        ind = q.pop()
        if not ind in seen and not puzzle[ind] == BLOCKCHAR:
            if ind+COLS < len(puzzle) and not ind in seen:
                q.append(ind+COLS)
            if ind-COLS >= 0 and not ind in seen:
                q.append(ind-COLS)
            if ind+1 < len(puzzle) and (ind+1)//COLS == ind//COLS and not ind in seen:
                q.append(ind+1)
            if ind-1 >= 0 and (ind-1)//COLS == ind//COLS and not ind in seen:
                q.append(ind-1)
            seen.add(ind)  

    if len(seen) != opens:
        return True
    return False

def get_disjoint_regions(puzzle):
    q = []
    sets = []
    seen = set()
    opens = len(puzzle)-puzzle.count(BLOCKCHAR)

    for i in range(len(puzzle)):
        if not puzzle[i] == BLOCKCHAR:
            q.append(i)
            break
    
    while opens > 0:
        while q:
            ind = q.pop()
            if not ind in seen and not puzzle[ind] == BLOCKCHAR:
                if ind+COLS < len(puzzle) and not ind in seen:
                    q.append(ind+COLS)
                if ind-COLS >= 0 and not ind in seen:
                    q.append(ind-COLS)
                if ind+1 < len(puzzle) and (ind+1)//COLS == ind//COLS and not ind in seen:
                    q.append(ind+1)
                if ind-1 >= 0 and (ind-1)//COLS == ind//COLS and not ind in seen:
                    q.append(ind-1)
                seen.add(ind)
        opens -= len(seen)
        sets.append(seen)
        for i in range(len(puzzle)):
            if not puzzle[i] == BLOCKCHAR and not i in seen:
                q.append(i)
                break
        seen = set()

    return sets
    

# utils
def make_base_puzzle(seeds=[]):
    puzzle = [EMPTYCHAR]*(ROWS*COLS)

    for seed in seeds:
        splseed = seed.lower().split("x")
        orientation = splseed[0][0]
        vpos = int(splseed[0][1:])
        if len(splseed[1]) >= 2 and splseed[1][1].isdigit():
            hpos = int(splseed[1][0:2])
            word = splseed[1][2:]      
        else:
            hpos = int(splseed[1][0])
            word = splseed[1][1:]
        if len(splseed) > 2:
            for k in range(2, len(splseed)):
                word += "x"+splseed[k]
        sqindex = (vpos*COLS)+hpos
        if not word:
            puzzle[sqindex] = BLOCKCHAR
            puzzle[-(sqindex)-1] = BLOCKCHAR
        else:
            for i,w in enumerate(word):
                offset = i*COLS if orientation == "v" else i
                puzzle[sqindex+offset] = w
                if w == BLOCKCHAR:
                    puzzle[-(sqindex+offset)-1] = w
            
    return puzzle 

def safe_set(puzzle, ind, ch):
    if puzzle[ind] == EMPTYCHAR and puzzle[-ind-1] == EMPTYCHAR:
        puzzle[ind] = ch
        puzzle[-ind-1] = ch
        return True
    return False

def display(puzzle):
    formatted = ""

    for r in range(0, len(puzzle), COLS):
        formatted += "".join(puzzle[r:r+COLS]) + "\n"
    
    print(formatted)

if __name__ == "__main__":
    main()

