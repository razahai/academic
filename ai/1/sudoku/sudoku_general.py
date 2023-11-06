import sys; args = sys.argv[1:]

def jbf(pzl):
    if invalid(pzl): return ""
    if solved(pzl): return pzl

    possible_choices = choices(pzl)
    
    for choice in possible_choices:
        nbf = jbf(choice)
        if nbf: return nbf
    return ""

# utils
def invalid(pzl):
    for constraint in LOCS:
        if len(ls:=[pzl[i] for i in constraint if pzl[i] != "."]) != len(set(ls)):
            return True
    return False

def solved(pzl):
    if "." in pzl:
        return False
    return True

def choices(pzl):
    choices = set()
    for i in range(len(pzl)):
        if pzl[i] == ".":
            for t in SYMSET:
                choice = pzl[:i]+t+pzl[i+1:]
                choices.add(choice)
            return choices

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

def gen_csets():
    constraints = []

    # rows
    r = 0
    for i in range(N):
        constraint = set()
        for j in range(N):
            constraint.add(r)
            r+=1
        constraints.append(constraint)
    
    # cols
    c = 0
    offset = 1
    for i in range(N):
        constraint = set()
        for j in range(N):
            constraint.add(c)
            for k in range(N):
                c+=1
        constraints.append(constraint)
        c=offset
        offset+=1
    
    # subblocks
    offset = 0
    for i in range(N):
        constraint = set()
        for j in range(sbw):
            constraint.add(offset)
            constraint.add(offset+N)
            offset+=1
        if (offset-1)%N == N-1:
            offset+=N*(sbh-1)
        constraints.append(constraint)

    return constraints

def get_dimensions(area, overall=1):
    for i in range(1, area):
        for j in range(1, area):
            if i<j: continue
            if (i*j)*overall==area:
                return (i,j)
      
def set_globals(pzl):    
    global N, SYMSET, sbw, sbh

    N = get_dimensions(len(pzl))[0] # (n, n) <- get n
    SYMSET = get_symbols(pzl)
    sbw, sbh = get_dimensions(len(pzl), N)

def get_nbrs():
    # FIXME: very disgusting
    
    dct = {}

    for i,constraint in enumerate(LOCS):
        for j in constraint:
            if j in dct:
                dct[j].append(i)
            else:
                dct[j] = [i]
    return dct


def checksum(pzl):
    return sum(ord(c) for c in pzl)-N*N*ord(min(SYMSET))

if __name__ == "__main__":
    pzls = open(args[0]).read().splitlines()

    for n,pzl in enumerate(pzls):
        set_globals(pzl)
        LOCS = gen_csets()
        print(f"{n+1:3}: {pzl}")
        solution = jbf(pzl)
        print(f"     {solution} {checksum(solution)}")

