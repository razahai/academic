import sys; args = sys.argv[1:]

# RL Setup - 100%
# dumb lab, literally just gw2 (but this time we had to get all paths, not shortest)

edges = []
rwds = []
implied_reward = 12
maximize_fn = 1 # G0 or G1
POSSIBILITIES = {
    "U": "U",
    "D": "D",
    "L": "L",
    "R": "R",
    "RU": "V",
    "DRU": "W",
    "DR": "S",
    "DLR": "T",
    "DL": "E",
    "DLU": "F",
    "LU": "M",
    "LRU": "N",
    "DU": "|",
    "LR": "-",
    "DLRU": "+",
    "": "."
}

def main():
    global maximize_fn 

    num_elements = int(args[0])
    arg_offset = 1
    if len(args) > 1 and args[1].isnumeric():
        width = int(args[1])
        arg_offset += 1
    else:
        width = calc_width(num_elements)
    
    for _ in range(num_elements):
        edges.append(set())
    for _ in range(num_elements):
        rwds.append("_")
    
    assume_edges(num_elements, width)

    for i in range(arg_offset, len(args)):
        if args[i][0].upper() == "R":
            # reward directive
            r_directive(args[i])
        elif args[i][0].upper() == "B":
            # block directive
            b_directive(args[i], width)
        elif args[i][0].upper() == "G":
            # g directive
            #   if G0, then you get the max reachable reward
            #   if G1, then you maximize reward/#steps 
            maximize_fn = int(args[i][1])
    
    policy = evaluate_policy(width)
    print(policy)

def evaluate_policy(width):
    output = ""

    # get all cells with rwds
    rwd_cells = set()
    for cell,rwd in enumerate(rwds):
        if rwd != "_":
            rwd_cells.add((cell, rwd))

    for cell in range(len(edges)):
        paths = find_path_directions(cell, rwd_cells)
        direction = paths2direction(cell, paths, width)

        if cell % width == 0 and cell != 0:
            output += "\n"
        output += direction
    
    return output

def find_path_directions(cell, rwd_cells):
    if rwds[cell] != "_":
        return [cell] 
    
    nbrs = sorted(edges[cell], key=lambda n: rwds[n] == "_")
    paths = []

    for nbr in nbrs:
        if rwds[nbr] != "_":
            paths.append((nbr, 1, rwds[nbr]))
        else:
            for c, rwd in rwd_cells:
                depth = find_path(nbr, c)
                if depth != -1:
                    paths.append((nbr, depth, rwd))
                
    directions = set()

    if paths:
        if maximize_fn == 0:
            max_rwd = max(paths, key=lambda p: p[2])[2]
            p_dirs = []

            for p in paths:
                if p[2] == max_rwd:
                    p_dirs.append(p)
    
            min_depth = min(p_dirs, key=lambda p: p[1])[1]
            for p in p_dirs:
                if p[1] == min_depth:
                    directions.add(p[0])
        elif maximize_fn == 1:
            max_fn = max(paths, key=lambda p: p[2]/p[1]) # depth _should_ never be 0
            fn = max_fn[2]/max_fn[1]

            for p in paths:
                if p[2]/p[1] == fn:
                    directions.add(p[0])            
            
    return directions

def find_path(cell, rwd_cell):
    # here we do not need the base case of if start == goal since we check that beforehand
    q = [cell]
    visited = {cell: ""}

    while q:
        node = q.pop(0)
        nbrs = edges[node]
        
        for n in nbrs:
            # i'm assuming that rwds are considered terminal, so we cannot go over them unless it's rwd_cell
            if n in visited or (rwds[n] != "_" and n != rwd_cell): continue            
            if n == rwd_cell:
                visited[n] = node
                current = visited[n]
                depth = 0

                while current != "":
                    depth += 1
                    current = visited[current]

                return depth+1 # for the original nbr step
            visited[n] = node
            q.append(n)

    return -1

def paths2direction(cell, paths, width):
    directions = ""
    
    if cell in paths:
        return "*"

    for path in paths:
        if cell+1 == path and width != 1 and not cell in range(width-1, len(edges), width):
            directions += "R"
        elif cell-1 == path and width != 1 and not cell in range(0, len(edges)-width+1, width):
            directions += "L"
        elif cell-width == path and width < len(edges) and not cell in range(0, width):
            directions += "U"
        elif cell+width == path and width < len(edges) and not cell in range(len(edges)-width, len(edges)):
            directions += "D"
        
    directions = "".join(sorted(directions))
    return POSSIBILITIES[directions]

def assume_edges(num_elements, width):
    for v in range(num_elements):
        if width != 1 and not v in range(width-1, num_elements, width):
            edges[v].add(v+1)
        if width != 1 and not v in range(0, num_elements-width+1, width):
            edges[v].add(v-1)
        if width < num_elements and not v in range(0, width):
            edges[v].add(v-width)
        if width < num_elements and not v in range(num_elements-width, num_elements):
            edges[v].add(v+width)

def r_directive(directive):
    global implied_reward

    cells = directive.split(":")
    if len(cells) == 1:
        # R#
        rwds[int(directive[1:])] = implied_reward
    elif len(cells) == 2 and cells[0].upper() == "R":
        # R:#
        implied_reward = int(directive[2:])
    else:
        # R#:#
        rwds[int(cells[0][1:])] = int(cells[1])

def b_directive(directive, width):
    cell = ""
    d_offset = 1
    for ch in directive[1:]:
        if ch != "N" and ch != "S" and ch != "E" and ch != "W":
            cell += ch
            d_offset += 1
        else:
            break
    cell = int(cell)

    if d_offset == len(directive):
        # B#
        rem_edges, new_edges = generate_toggles(cell, width)
        for v, v1 in rem_edges:
            edges[v].remove(v1)
        for v, v1 in new_edges:
            edges[v].add(v1)
    else:
        # B#[NSEW]+
        directions = directive[d_offset:].split()
        rem_edges, new_edges = generate_toggles(cell, width, directions)
        for v, v1 in rem_edges:
            edges[v].remove(v1)
        for v, v1 in new_edges:
            edges[v].add(v1)

def generate_toggles(cell, width, directions=[]):
    rem_edges = set()
    new_edges = set()

    p_nbrs = set()
    if len(directions) > 0:
        for direction in directions:
            if direction == "N":
                if not cell in range(0, width):
                    p_nbrs.add(cell-width)
            elif direction == "S":
                if not cell in range(len(edges)-width, len(edges)):
                    p_nbrs.add(cell+width)
            elif direction == "E":
                if not cell in range(width-1, len(edges), width):
                    p_nbrs.add(cell+1)
            elif direction == "W":
                if not cell in range(0, len(edges)-width+1, width):
                    p_nbrs.add(cell-1)
    else:
        if not cell in range(0, len(edges)-width+1, width):
            p_nbrs.add(cell-1)
        if not cell in range(width-1, len(edges), width):
            p_nbrs.add(cell+1)
        if not cell in range(0, width):
            p_nbrs.add(cell-width)
        if not cell in range(len(edges)-width, len(edges)):
            p_nbrs.add(cell+width)

    for v1 in p_nbrs:
        if v1 in edges[cell]:
            rem_edges.add((cell, v1))
        else:
            new_edges.add((cell, v1))

        if cell in edges[v1]:
            rem_edges.add((v1, cell))
        else:
            new_edges.add((v1, cell))
    
    return (rem_edges, new_edges)

def calc_width(num_elements):
    for i in range(1, num_elements+1):
        for j in range(1, num_elements+1):
            if i<j: continue
            if i*j == num_elements:
                return i 

if __name__ == "__main__":
    main()

