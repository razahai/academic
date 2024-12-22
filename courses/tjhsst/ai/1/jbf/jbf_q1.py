import sys; args = sys.argv[1:]

# * Q1 - 100%

def main():
    global csets, ttypes

    if len(args) > 0:
        n = int(args[0])
        pzl = "."*(n*n)
        ttypes = gen_ttypes(n)
        if len(args) > 1:
            pzl = args[1]
            ttypes = get_symbols(pzl,n)
    else:
        n = 7
        pzl = "."*49 # 7x7 board -> 7*7 array
        ttypes = ['a','b','c','d','e','f','g']

    csets = [
        # rows
        {0, 1, 2, 3, 4, 5, 6},
        {7, 8, 9, 10, 11, 12, 13},
        {14, 15, 16, 17, 18, 19, 20},
        {21, 22, 23, 24, 25, 26, 27},
        {28, 29, 30, 31, 32, 33, 34},
        {35, 36, 37, 38, 39, 40, 41},
        {42, 43, 44, 45, 46, 47, 48},
        # cols
        {0, 7, 14, 21, 28, 35, 42},
        {1, 8, 15, 22, 29, 36, 43},
        {2, 9, 16, 23, 30, 37, 44},
        {3, 10, 17, 24, 31, 38, 45},
        {4, 11, 18, 25, 32, 39, 46},
        {5, 12, 19, 26, 33, 40, 47},
        {6, 13, 20, 27, 34, 41, 48},
        # diags
        {0, 8, 16, 24, 32, 40, 48},
        {6, 12, 18, 24, 30, 36, 42}
    ]

    if n != 7:
        csets = gen_csets(n)

    solution = jbf(pzl)

    if solution == "":
        print("No solution possible")
    else:
        pretty(solution, n)

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
    for constraint in csets:
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
            for t in ttypes:
                choice = pzl[:i]+t+pzl[i+1:]
                choices.add(choice)
            return choices

def get_symbols(pzl,n):
    symbols = set()
    for c in pzl:
        if c != ".":
            symbols.add(c)
    
    offset = 0
    while len(symbols) < n:
        symbols.add(chr(ord('a')+offset))
        offset+=1

    return list(symbols)

def gen_csets(n):
    constraints = []

    r = 0
    for i in range(n):
        constraint = set()
        for j in range(n):
            constraint.add(r)
            r+=1
        constraints.append(constraint)
    
    c = 0
    offset = 1
    for i in range(n):
        constraint = set()
        for j in range(n):
            constraint.add(c)
            for k in range(n):
                c+=1
        constraints.append(constraint)
        c=offset
        offset+=1
    
    d1 = 0
    diag1 = set()
    for _ in range(n):
        diag1.add(d1)
        d1+=n+1
    constraints.append(diag1)  

    d2 = n-1
    diag2 = set()
    for _ in range(n):
        diag2.add(d2)
        d2+=n-1
    constraints.append(diag2)

    return constraints

def gen_ttypes(n):
    types = []
    
    offset = 0
    for _ in range(n):
        types.append(chr(ord('a')+offset))
        offset+=1
    
    return types


def pretty(pzl,n):
    pzl = [*pzl]
    output = ""
    
    offset = 0
    for i in range(n):
        output+=' '.join(pzl[offset:offset+n])+"\n"
        offset+=n
    
    print(output.strip())

if __name__ == "__main__":
    main()

