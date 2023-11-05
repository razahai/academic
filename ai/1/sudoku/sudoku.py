import sys; args = sys.argv[1:]

# sudoku - undefined%

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
        for i in constraint:
            for j in constraint:
                if pzl[i] == pzl[j] and pzl[i] != "." and i!=j:
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

def checksum(pzl):
    return 324

def formatted(n, pzl, solution):
    output = ""
    cs = checksum(pzl)

    if n < 10:
        output += "  "+str(n)+": "
    elif n < 100:
        output += " "+str(n)+": "
    else:
        output += str(n)+": "
    
    output += pzl+"\n"
    output += "     "+solution # 5 spaces
    output += " "+str(cs)

    return output

if __name__ == "__main__":
    pzls = open(args[0]).read().splitlines()
    
    for n,pzl in enumerate(pzls):
        set_globals(pzl)
        LOCS = gen_csets()
        solution = jbf(pzl)
        print(formatted(n+1, pzl, solution))

