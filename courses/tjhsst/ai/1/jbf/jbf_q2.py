import sys; args = sys.argv[1:]

# * Q2 - 100%

def main():
    global csets, ttypes

    if len(args) > 0:
        pzl = args[0]
        ttypes = get_symbols(pzl)
    else:
        pzl = "."*24 # 24 triangles
        ttypes = ['1', '2', '3', '4', '5', '6']

    csets = [
        # hexagons
        {7,8,9,14,15,16},
        {0,1,2,6,7,8},
        {2,3,4,8,9,10},
        {9,10,11,16,17,18},
        {15,16,17,21,22,23},
        {13,14,15,19,20,21},
        {5,6,7,12,13,14}
    ]

    solution = jbf(pzl)

    if solution == "":
        print("No solution possible")
    else:
        pretty(solution)

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

def get_symbols(pzl):
    symbols = set()
    for c in pzl:
        if c != ".":
            symbols.add(c)
    
    offset = 1
    while len(symbols) < 6:
        symbols.add(str(offset))
        offset+=1

    return list(symbols)

def pretty(pzl):
    pzl = [*pzl]
    output = ""
    
    output+="  "+' '.join(pzl[0:5])+"\n"
    output+=' '.join(pzl[5:12])+"\n"
    output+=' '.join(pzl[12:19])+"\n"
    output+="  "+' '.join(pzl[19:24])
    print(output)

if __name__ == "__main__":
    main()

