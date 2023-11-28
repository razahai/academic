import sys; args = sys.argv[1:]

# Blocks - undefined%

def main():
    global cx,cy
    
    raw_blocks, cx, cy = extract_input(args)
    container = ["."]*(cx*cy)
    
    raw_blocks.sort() # TODO: sort by area
    combined_area = normalize_blocks(raw_blocks)
    add_rotations(raw_blocks)

    if combined_area > cx*cy:
        print("No solution")

    solution = jbf(container, 0, raw_blocks, [])
    if solution:
        print(f"Decomposition: {solution}")
    else:
        print("No solution")

def jbf(container, tile, raw_blocks, sol):
    if solved(container): return sol

    choices = choice(container, tile, raw_blocks)
    
    for choi in choices:
        dc_container = [c for c in container] 
        place(dc_container, tile, choi)
        
        dc_raw_blocks = [r for r in raw_blocks]
        dc_raw_blocks.remove(choi)
        
        dc_sol = [s for s in sol]
        dc_sol.append(choi)
        
        dc_tile = tile+choi[1]
        while dc_tile < len(dc_container) and dc_container[dc_tile] != ".":
            dc_tile+=1
        nbf = jbf(dc_container, dc_tile, dc_raw_blocks, dc_sol)
        if nbf: return nbf
    return ""

def choice(container, tile, raw_blocks):
    if container[tile] != ".": return []
    valid_choices = []

    for y,x in raw_blocks:

        if tile+(cx*(y-1)) < len(container) and \
            tile+(cx*(y-1))+(x-1) < len(container) and \
            tile+(x-1) < len(container) and \
            cx >= x and cy >= y:
        
            if container[tile+(cx*(y-1))] == "." and \
                container[tile+(x-1)] == "." and \
                container[tile+(cx*(y-1))+(x-1)] == ".":
                valid_choices.append((y,x))
    
    return valid_choices    

def place(container, tile, choice):
    y,x = choice

    for k in range(1, y+1):
        for i in range(tile+(cx*(k-1)), tile+(cx*(k-1))+x):
            container[i] = choice


def normalize_blocks(raw_blocks):
    carea = 0

    for y,x in raw_blocks:
        carea += x*y
    
    if cx*cy > carea:
        for i in range(cx*cy-carea):
            raw_blocks.append((1,1))
    return carea

def add_rotations(raw_blocks):
    appendage = []
    for y,x in raw_blocks:
        appendage.append((x,y))
    raw_blocks.extend(appendage)

# util
def solved(container):
    if "." in container:
        return False
    return True

def extract_input(inp):
    raw_blocks = []
    
    idx = 0
    while idx < len(inp):
        current = idx

        if len(inp[idx]) >= 3:
            y,x = inp[idx].lower().split("x")
        else:
            y = inp[idx]
            x = inp[idx+1]
            idx+=1

        if current == 0:
            cx, cy = int(x), int(y)
        else:
            raw_blocks.append((int(y),int(x)))
        idx+=1
    
    return (raw_blocks, cx, cy)

if __name__ == "__main__":
    main()

