import sys; args = sys.argv[1:]

# Blocks - undefined%

def main():
    global cx,cy
    
    raw_blocks, cx, cy = extract_input(args)
    
    raw_blocks.sort(key=lambda bk: bk[0]*bk[1], reverse=True) # <- sorted by area (pot imp)
    combined_area = normalize_blocks(raw_blocks)
    add_rotations(raw_blocks)
    
    if combined_area > cx*cy:
        print("No solution")
    
    first_row = frow(raw_blocks)
    
    if len(first_row) == 0:
        container = ["."]*(cx*cy)
        solution = jbf(container, 0, raw_blocks, [])
        if solution:
            print(f"Decomposition: {solution}")
        else:
            print("No solution")
    else:
        ret = ""

        for blocks in first_row:
            container = ["."]*(cx*cy)
            rbcpy = [r for r in raw_blocks]
            fb = blocks[0]

            place(container, 0, fb)
            rbcpy.remove(fb)
            if fb[0] != fb[1]:
                rbcpy.remove((fb[1], fb[0]))

            if len(blocks) == 1:
                tile = cx*fb[0]
                solution = jbf(container, tile, rbcpy, [fb])
            elif len(blocks) == 2:
                sb = blocks[1]
                solarr = [fb,sb]

                place(container, fb[1], sb)
                rbcpy.remove(sb)
                if sb[0] != sb[1]:
                    rbcpy.remove((sb[1], sb[0]))

                minheight = min(solarr, key=lambda bk: bk[0])                
                tile = 0
                if fb[0] > sb[0]:
                    tile = cx*(minheight[0])+fb[1]
                elif fb[0] == minheight[0]:
                    tile = cx*minheight[0]

                solution = jbf(container, tile, rbcpy, solarr)
            elif len(blocks) == 3:
                sb = blocks[1]
                tb = blocks[2]
                solarr = [fb,sb,tb]

                place(container, fb[1], sb)
                rbcpy.remove(sb)
                if sb[0] != sb[1]:
                    rbcpy.remove((sb[1], sb[0]))

                place(container, fb[1]+sb[1], tb)
                rbcpy.remove(tb)
                if tb[0] != tb[1]:
                    rbcpy.remove((tb[1], tb[0]))
                
                minheight = min(solarr, key=lambda bk: bk[0])                
                tile = 0
                if fb[0] > sb[0]:
                    tile = cx*(minheight[0])+fb[1]
                elif fb[0] == sb[0] and fb[0] > tb[0]:
                    tile = cx*(minheight[0])+fb[1]+sb[1]
                elif fb[0] == minheight[0]:
                    tile = cx*minheight[0]

                solution = jbf(container, tile, rbcpy, solarr)
            else:
                sb = blocks[1]
                tb = blocks[2]
                fob = blocks[3]
                solarr = [fb,sb,tb,fob]

                place(container, fb[1], sb)
                rbcpy.remove(sb)
                if sb[0] != sb[1]:
                    rbcpy.remove((sb[1], sb[0]))

                place(container, fb[1]+sb[1], tb)
                rbcpy.remove(tb)
                if tb[0] != tb[1]:
                    rbcpy.remove((tb[1], tb[0]))
                
                place(container, fb[1]+sb[1]+tb[1], fob)
                rbcpy.remove(fob)
                if fob[0] != fob[1]:
                    rbcpy.remove((fob[1], fob[0]))

                minheight = min(solarr, key=lambda bk: bk[0])                
                tile = 0
                if fb[0] > sb[0]:
                    tile = cx*(minheight[0])+fb[1]
                elif fb[0] == sb[0] and fb[0] > tb[0]:
                    tile = cx*(minheight[0])+fb[1]+sb[1]
                elif fb[0] == sb[0] and fb[0] == tb[0] and fb[0] > fob[0]:
                    tile = cx*(minheight[0])+fb[1]+sb[1]+fob[1]
                elif fb[0] == minheight[0]:
                    tile = cx*minheight[0]

                solution = jbf(container, tile, rbcpy, solarr)
            if solution:
                ret = f"Decomposition: {solution}"
                break
            else:
                # keep going in case there is a solution
                ret = "No solution"

        print(ret)    
    # solution = jbf(container, 0, raw_blocks, [])
    # if solution:
    #     print(f"Decomposition: {solution}")
    # else:
    #     print("No solution")
    
def jbf(container, tile, raw_blocks, sol):
    if solved(container): return sol

    choices = choice(container, tile, raw_blocks)
    
    for choi in choices:
        dc_container = [c for c in container] 
        place(dc_container, tile, choi)
        
        dc_raw_blocks = [r for r in raw_blocks]
        dc_raw_blocks.remove(choi)
        if (choi[1],choi[0]) in dc_raw_blocks and choi[1] != choi[0]:
            dc_raw_blocks.remove((choi[1],choi[0]))
        
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
            
            if (tile+(x-1))//cx == tile//cx:
                if container[tile+(cx*(y-1))] == "." and \
                    container[tile+(x-1)] == "." and \
                    container[tile+(cx*(y-1))+(x-1)] == ".":
                    valid_choices.append((y,x))
    
    # sort by area
    valid_choices.sort(key=lambda bk: bk[0]*bk[1], reverse=True)
    
    return valid_choices    

def place(container, tile, choice):
    y,x = choice

    for k in range(1, y+1):
        for i in range(tile+(cx*(k-1)), tile+(cx*(k-1))+x):
            container[i] = choice

def frow(raw_blocks):
    valid_blocks = []
    sorted_blocks = sorted(raw_blocks, key=lambda bk: bk[0]*bk[1], reverse=True)

    for i in range(len(sorted_blocks)):
        first = sorted_blocks[i]

        if first[1] == cx:
            valid_blocks.append(((first),))
        else:
            for j in range(i+1, len(sorted_blocks)):
                second = sorted_blocks[j]
                
                if first[1] + second[1] == cx:
                    if first[0] == second[1] and first[1] == second[0]:
                        continue
                    if first[0] > cy or second[0] > cy:
                        continue
                    
                    valid_blocks.append((first, second))
                else:
                    duosum = first[1]+second[1]
                    if cx-duosum <= 0: continue

                    for k in range(j+1, len(sorted_blocks)):
                        third = sorted_blocks[k]
                        
                        if cx-duosum == third[1]:
                            if first[0] == second[1] and first[1] == second[0] or \
                                first[0] == third[1] and first[1] == third[0] or \
                                second[0] == third[1] and second[1] == third[0]:
                                continue
                            if first[0] > cy or second[0] > cy or third[0] > cy:
                                continue
                            if (first, second, third) in valid_blocks:
                                continue
                            valid_blocks.append((first, second, third))
                        else:
                            trisum = first[1]+second[1]+third[1]
                            if cx-trisum <= 0: continue
                            
                            for m in range(k+1, len(sorted_blocks)):
                                fourth = sorted_blocks[m]

                                if cx-trisum == fourth[1]:
                                    if first[0] == second[1] and first[1] == second[0] or \
                                        first[0] == third[1] and first[1] == third[0] or \
                                        second[0] == third[1] and second[1] == third[0] or \
                                        first[0] == fourth[1] and first[1] == fourth[0] or \
                                        second[0] == fourth[1] and second[1] == fourth[0] or \
                                        third[0] == fourth[1] and third[1] and fourth[0]:
                                        continue
                                    if first[0] > cy or second[0] > cy or third[0] > cy or fourth[0] > cy:
                                        continue
                                    if (first, second, third, fourth) in valid_blocks:
                                        continue
                                    valid_blocks.append((first, second, third, fourth))

    valid_blocks.sort(key=lambda bk: len(bk), reverse=True)

    return valid_blocks

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
        if y == x:
            continue
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

        if "x" in inp[idx].lower():
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

