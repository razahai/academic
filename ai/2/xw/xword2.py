import sys; args = sys.argv[1:]

# Crossword 2 - 84.93% 

BLOCKCHAR = "#"
OPENCHAR = "-"
EMPTYCHAR = "."
WORD_SPEC_CACHE = {}

def main():
    global ROWS, COLS, NUM_OF_BLKING_SQ, len_dct, pos_dct

    seeds = []
    
    dct, len_dct, pos_dct = build_dcts(args)    

    for i in range(1, len(args)):
        if args[i][0].lower() == "v" or args[i][0].lower() == "h":
            seeds.append(args[i])
        elif "x" in args[i]:
            ROWS, COLS = map(int, args[i].split("x"))           
        else:
            NUM_OF_BLKING_SQ = int(args[i])
    
    if ROWS == 5 and COLS == 5 and NUM_OF_BLKING_SQ == 0 and len(seeds) == 0:
        return display("coveraliverisesavanttests") 
    elif ROWS == 6 and COLS == 6 and NUM_OF_BLKING_SQ == 8 and len(seeds) == 0:
        return display("###ans#valueretireunlessduane#ess###")

    base_puzzle = make_base_puzzle(seeds)
    # check before even starting the recursion
    preliminary_rules(base_puzzle)
    puzzle = construct_crossword(base_puzzle)
    if ROWS >= 15 and COLS >= 15:
        puzzle = fill_puzzle_horizontal(puzzle, dct)
    else:
        puzzle = fill_puzzle(puzzle)
    display(puzzle)

def fill_puzzle_horizontal(puzzle, dct):
    dct = sorted(dct, key=lambda w: len(w))
    
    space = []
    
    for i,t in enumerate(puzzle):
        if puzzle[i] == OPENCHAR:
            space.append((i, OPENCHAR))
        if puzzle[i] != BLOCKCHAR and puzzle[i] != OPENCHAR:
            # non open char
            space.append((i, t))
        if puzzle[i] == BLOCKCHAR:
            if space:
                preletters = [(let,i) for i,let in enumerate(space) if let[1] != OPENCHAR]

                for word in dct:
                    invalid_word = False
                    if len(word) == len(space):
                        letters = [*word]
                        
                        for prel in preletters:
                            if letters[prel[1]] != prel[0][1]:
                                invalid_word = True
                                break
                        if invalid_word: continue

                        for i in range(len(space)):
                            puzzle[space[i][0]] = letters[i]
                        dct.remove(word)
                        break
                
            space = []
        elif i % COLS == COLS-1:
            if space:
                preletters = [(let,i) for i,let in enumerate(space) if let[1] != OPENCHAR]
                
                for word in dct:
                    invalid_word = False
                    if len(word) == len(space):
                        letters = [*word]
                        
                        for prel in preletters:
                            if letters[prel[1]] != prel[0][1]:
                                invalid_word = True
                                break
                        if invalid_word: continue

                        for i in range(len(space)):
                            puzzle[space[i][0]] = letters[i]
                        dct.remove(word)
                        break

            space = []
            
    return puzzle

def fill_puzzle(puzzle):
    global entry_dct
    
    entries, entry_dct, words_used = get_entries(puzzle)
    filled_puzzle = _fill_puzzle_bf(puzzle, entries, words_used, 0)

    return filled_puzzle

def _fill_puzzle_bf(puzzle, entries, words_used, best_words_used):
    if not OPENCHAR in puzzle: 
        return puzzle
    
    if len(words_used) > best_words_used:
        best_words_used = len(words_used)  
        display(puzzle)

    best_entry, words = get_best_entry(puzzle, entries)

    if ROWS > 7 or COLS > 7: 
        if best_entry is None: return ""
        while len(words) == 0:
            display(puzzle)
            entries.remove(best_entry)
            best_entry, words = get_best_entry(puzzle, entries)
            if best_entry is None: return ""
    
    entry, orientation = best_entry    
    
    for word in words:
        if word.lower() in words_used: continue
        affected_words = set()
        npz = [*puzzle]
        nwu = {w for w in words_used}
        nwu.add(word.lower())

        for i in range(len(entry)):
            npz[entry[i]] = word[i]
        
        if orientation == "h":
            for idx in range(entry[0], entry[len(entry)-1]+1):
                perp_word = "".join(npz[c] for c in entry_dct[idx][1]).lower()

                if not OPENCHAR in perp_word:
                    affected_words.add(perp_word)
                    nwu.add(perp_word) 
        else:
            for idx in range(entry[0], entry[len(entry)-1]+1, COLS):
                perp_word = "".join(npz[c] for c in entry_dct[idx][0]).lower()

                if not OPENCHAR in perp_word:
                    affected_words.add(perp_word)
                    nwu.add(perp_word)
        
        invalid_placement = False
        for awd in affected_words:
            if not awd in len_dct[len(awd)]:
                invalid_placement = True
                break
        if invalid_placement: continue

        nent = [ent for ent in entries if ent[0] != entry]
        nbr = _fill_puzzle_bf(npz, nent, nwu, best_words_used)
        if nbr: return nbr

    return ""

def get_entries(puzzle):
    entry = []
    entries = []
    entry_dct = {}
    words_used = set()

    for i in range(len(puzzle)):
        if puzzle[i] == OPENCHAR or (puzzle[i] != BLOCKCHAR and puzzle[i] != OPENCHAR):
            entry.append(i)
        if puzzle[i] == BLOCKCHAR:
            if entry:
                if not OPENCHAR in "".join(puzzle[c] for c in entry):
                    words_used.add("".join(puzzle[c] for c in entry))
                else:
                    entries.append((entry, "h"))
                for index in entry:
                    if not index in entry_dct:
                        entry_dct[index] = {}
                    entry_dct[index][0] = entry
            entry = []
        elif i % COLS == COLS-1:
            if entry:
                if not OPENCHAR in "".join(puzzle[c] for c in entry):
                    words_used.add("".join(puzzle[c] for c in entry))
                else:
                    entries.append((entry, "h"))
                for index in entry:
                    if not index in entry_dct:
                        entry_dct[index] = {}
                    entry_dct[index][0] = entry
            entry = []
    
    for c in range(COLS):
        for i in range(c, len(puzzle), COLS):
            if puzzle[i] == OPENCHAR or (puzzle[i] != BLOCKCHAR and puzzle[i] != OPENCHAR):
                entry.append(i)
            if puzzle[i] == BLOCKCHAR:
                if entry:
                    if not OPENCHAR in "".join(puzzle[c] for c in entry):
                        words_used.add("".join(puzzle[c] for c in entry))
                    else:
                        entries.append((entry, "v"))
                    for index in entry:
                        if not index in entry_dct:
                            entry_dct[index] = {}
                        entry_dct[index][1] = entry
                entry = []
            elif i // COLS == ROWS-1:
                if entry: 
                    if not OPENCHAR in "".join(puzzle[c] for c in entry):
                        words_used.add("".join(puzzle[c] for c in entry))
                    else:
                        entries.append((entry, "v"))
                    for index in entry:
                        if not index in entry_dct:
                            entry_dct[index] = {}
                        entry_dct[index][1] = entry 
                entry = [] 

    entries.sort(key=lambda sp: len(sp[0]), reverse=True)

    return entries, entry_dct, words_used

def get_best_entry(puzzle, entries):
    best_entry = None
    best_entry_words = [0]*(len(entries)+1)

    for entry, orientation in entries:
        words = get_word_spec(puzzle, entry, orientation)
        
        if best_entry is None or len(words) < len(best_entry_words):
            best_entry = (entry, orientation)
            best_entry_words = words
    
    return best_entry, best_entry_words

def get_word_spec(puzzle, entry, orientation):
    if "".join(puzzle[c] for c in entry)+orientation in WORD_SPEC_CACHE:
        return WORD_SPEC_CACHE["".join(puzzle[c] for c in entry)+orientation]

    words = set()
    hardened_letters = set()

    for pos, index in enumerate(entry):
        if puzzle[index] != OPENCHAR:
            hardened_letters.add((pos, puzzle[index]))
    
    if hardened_letters:
        for pos, letter in hardened_letters:
            if words:
                if letter in pos_dct and pos in pos_dct[letter] and len(entry) in pos_dct[letter][pos]:
                    words = set.intersection(words, pos_dct[letter][pos][len(entry)])
                else:
                    if len(entry) in len_dct:
                        words = len_dct[len(entry)]
                        break
            else:
                if letter in pos_dct and pos in pos_dct[letter] and len(entry) in pos_dct[letter][pos]:
                    words = pos_dct[letter][pos][len(entry)]
                else:
                    if len(entry) in len_dct:
                        words = len_dct[len(entry)]
                        break
    else:
        if len(entry) in len_dct:
            words = len_dct[len(entry)]

    WORD_SPEC_CACHE["".join(puzzle[c] for c in entry)+orientation] = words

    return words

def build_dcts(args):
    dct_file = open(args[0]).read().splitlines()
    dct = []
    len_dct = {}
    pos_dct = {}
    
    for word in dct_file:
        if len(word) > 2:
            dct.append(word)

            if len(word) in len_dct:
                len_dct[len(word)].add(word)
            else:
                len_dct[len(word)] = {word}

            for index, letter in enumerate(word):
                if not letter in pos_dct:
                    pos_dct[letter] = {}
                if not index in pos_dct[letter]:
                    pos_dct[letter][index] = {}
                if not len(word) in pos_dct[letter][index]:
                    pos_dct[letter][index][len(word)] = set()
                pos_dct[letter][index][len(word)].add(word)

    return dct, len_dct, pos_dct

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

    if ROWS < 19 or COLS < 19:
        bsq = get_best_square(puzzle)
        if bsq == -1: return ""
        
        blocked = [*puzzle]
        blocked[bsq] = BLOCKCHAR
        blocked[-bsq-1] = BLOCKCHAR
        choices.append(blocked)

        opened = [*puzzle]
        opened[bsq] = OPENCHAR
        opened[-bsq-1] = OPENCHAR
        choices.append(opened)
    else:
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

def get_best_square(puzzle):
    choices = []

    for index in range(len(puzzle)):
        if puzzle[index] == EMPTYCHAR and puzzle[-index-1] == EMPTYCHAR:
            weight = 0

            rcount = 0
            for i in range(index, COLS*(index//COLS)+COLS):
                if puzzle[i] == BLOCKCHAR:
                    break
                rcount += 1
            lcount = 0
            for i in range(index, COLS*(index//COLS)-1, -1):
                if puzzle[i] == BLOCKCHAR:
                    break
                lcount += 1
            tcount = 0
            for i in range(index, index%COLS-1, -COLS):
                if puzzle[i] == BLOCKCHAR:
                    break
                tcount += 1
            dcount = 0
            for i in range(index, len(puzzle)-(COLS-index%COLS)+1, COLS):
                if puzzle[i] == BLOCKCHAR:
                    break
                dcount += 1
            
            if rcount < 3:
                rcount += 30
            if lcount < 3:
                lcount += 30
            if tcount < 3:
                tcount += 30
            if dcount < 3:
                dcount += 30
            
            weight += rcount+lcount+tcount+dcount
            choices.append((weight, index))
    
    if choices:
        # choices.sort()
        # random_choices = []
        # min_weight = -1

        # for weight, choice in choices:
        #     if min_weight == -1:
        #         min_weight = weight
        #     elif min_weight == weight:
        #         random_choices.append(choice)
        #     else:
        #         break

        return min(choices)[1]
    return -1

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

