import sys; args = sys.argv[1:]

# really bad score -- ~89%

def main():
    global gspace, gcoords, pcoords, width, height

    lines = open(args[0]).read().splitlines()
    goal = lines[0]
    
    width, height = (4, 4)

    data = pzl_data(goal)
    gspace = data[0]
    gcoords = data[1]
    pcoords = data[2]

    for pzl in lines:
        out = astar(pzl, goal)
        puzzcheck(out, pzl, goal)
    
def pzl_data(goal):
    gspace = goal.find("_")
    gcoords = {c: (i//height, i%width) for i,c in enumerate(goal)}
    pcoords = [(i//height, i%width) for i in range(16)]

    return [gspace, gcoords, pcoords]

def puzzcheck(result, pzl, goal):
    if result[1] == 0:
        puzzprint("G", pzl, goal)
    elif result[1] == -1: 
        puzzprint("X", pzl, goal)
    else:
        puzzprint("*", pzl, goal, condensed(result[0], width))

def md(tile, pzl, goal):
    tc_idx = pzl.find(tile)
    tg_idx = goal.find(tile)
    
    crow = tc_idx//height
    ccol = tc_idx%width
    grow = tg_idx//height
    gcol = tg_idx%width
    
    vertdiff = abs(crow - grow)
    hordiff = abs(ccol - gcol)

    return hordiff+vertdiff
    
def h(pzl, goal):
    return sum(md(tile, pzl, goal) for tile in pzl if tile != "_")

def puzzprint(type, pzl, goal, path=""):
    if type == "G":
        print(f"? {pzl} goal={goal}=> G")
    elif type == "X":
        print(f"? {pzl} goal={goal}=> X") 
    else:
        print(f"? {pzl} goal={goal}=> {path}")

def condensed(path, width):
    dirs = ""

    for i in range(len(path)-1):
        pzl = path[i].find("_")
        adj = path[i+1].find("_")

        if pzl+1 == adj:
            dirs += "R"
        elif pzl-1 == adj:
            dirs += "L"
        elif pzl-width == adj:
            dirs += "U"
        elif pzl+width == adj:
            dirs += "D"
    
    return dirs

def not_possible(start, goal):
    start_inversion = icc(start)
    goal_inversion = icc(goal)

    if width % 2 != 0:
        if start_inversion % 2 != goal_inversion % 2:
            return True
    else:
        if (start_inversion + start.find("_")//height) % 2 != (goal_inversion + goal.find("_")//height) % 2:
            return True
    return False

def astar(start, goal):
    if start == goal:
        return [[start], 0]

    if not_possible(start, goal):
        return [[start], -1]    

    openSet = [(h(start, goal), 0, start, "")]
    closedSet = {}   

    while True:
        popped = pq_remove(openSet)
        pzl = popped[2]
        parent = popped[3]
        
        if pzl in closedSet: continue
        closedSet[pzl] = parent
        if pzl == goal:
            path = []
            current = closedSet[pzl]
            
            path.append(pzl)

            while current != "":
                path.append(current)
                current = closedSet[current]

            return [path[::-1], 8888] 

        for n in neighbors(pzl):
            if n in closedSet: continue
            f = popped[0]
            if q_f(n, goal, pzl) == 1:
               f += 2
            pq_insert(openSet, (f, popped[1]+1, n, pzl))
    
def q_f(pzl, goal, parent):
    # not really that optimized but yeah
    pu_idx = parent.find("_")
    
    new = md(pzl[pu_idx], pzl, goal)
    prev = md(parent[parent.find(pzl[pu_idx])], parent, goal)

    return new-prev

def icc(seq):
    count = 0
    seq = seq.replace("_", "")

    for i in range(len(seq)):
        for j in range(i+1, len(seq)):
            if seq[i] > seq[j]:
                count += 1
    
    return count

def neighbors(puzzle: str):
    u_idx = puzzle.find("_")
    positions = []

    row = u_idx//height
    col = u_idx%width

    def swap(l, i, j):
        temp = l[i]
        l[i] = l[j]
        l[j] = temp

    if (row-1) > -1:
        pot = [*puzzle]
        swap(pot, u_idx, u_idx-width)
        positions.append(''.join(pot))
    
    if row+1 < height:
        pot = [*puzzle]
        swap(pot, u_idx, u_idx+width)
        positions.append(''.join(pot))
    
    if (col+1) < width:
        pot = [*puzzle]
        swap(pot, u_idx, u_idx+1)
        positions.append(''.join(pot))
    
    if (col-1) > -1:
        pot = [*puzzle]
        swap(pot, u_idx, u_idx-1)
        positions.append(''.join(pot))

    return positions

def get_dimensions(area):
    for i in range(1, area):
        for j in range(1, area):
            if i<j: continue
            if i*j == area:
                return (i, j) 

# pq 

def pq_insert(q, el):
    q.append(el)
    pq_bubbleup(q, 0, len(q)-1)

def pq_remove(q):
    el = q.pop()
    if q:
        newel = q[0]
        q[0] = el
        pq_bubbledown(q, 0)
        return newel
    return el

def pq_bubbledown(q, pos):
    orig = pos
    el = q[pos]
    smallpos = 4*pos + 1

    while smallpos < len(q):
        for c in range(1,4):
            pos_smallerpos = smallpos + c
            # compare f()s
            if pos_smallerpos < len(q) and q[smallpos][0] > q[pos_smallerpos][0]:
                smallpos = pos_smallerpos
        q[pos] = q[smallpos]
        pos = smallpos
        smallpos = 4*pos + 1

    q[pos] = el
    pq_bubbleup(q, orig, pos)

def pq_bubbleup(q, start, pos):
    el = q[pos]

    while pos > start:
        pntpos = (pos - 1) // 4
        parent = q[pntpos]

        if el < parent:
            q[pos] = parent
            pos = pntpos
            continue
        break

    q[pos] = el

if __name__ == "__main__":
    main()

