import sys; args = sys.argv[1:]

# Blocks - undefined%

def main():
    global cx,cy
    
    raw_blocks, cx, cy = extract_input(args)
    container = ["."]*(cx*cy)
    
    raw_blocks.sort()#(key=lambda bk: bk[0]*bk[1], reverse=True) # <- sorted by area (pot imp)
    combined_area = normalize_blocks(raw_blocks)
    add_rotations(raw_blocks)
    
    if combined_area > cx*cy:
        print("No solution")
    
    solution = jbf(container, 0, raw_blocks, [])
    if solution:
        print(f"Decomposition: {solution}")
    else:
        print("No solution")
    
    #     ret = ""

    #     for fb, sb in first_row:
    #         ccontainer = ["."]*(cx*cy)
        
    #         place(ccontainer, 0, fb)
    #         place(ccontainer, fb[1], sb)
            
    #         if fb[0] > sb[0]:
    #             tile = (cx*(fb[0]-1))+(fb[1]-1)
    #         elif sb[0] > fb[0]:
    #             tile = (cx*fb[0])
    #         else:
    #             tile = (cx*(fb[0]))
            
    #         dc_raw_blocks = [r for r in raw_blocks]
    #         dc_raw_blocks.remove(fb)
    #         dc_raw_blocks.remove(sb)
    #         if fb[1] != fb[0]:
    #             dc_raw_blocks.remove((fb[1], fb[0]))
    #         if sb[1] != sb[0]:
    #             dc_raw_blocks.remove((sb[1], sb[0]))

    #         print(tile, fb, sb)
    #         solution = jbf(ccontainer, tile, dc_raw_blocks, [fb, sb])

    #         if solution:
    #             ret = f"Decomposition: {solution}"
    #             break
    #         else:
    #             # keep going in case there is a solution
    #             ret = "No solution"
            
    #     if ret == "No solution":
    #         solution = jbf(container, 0, raw_blocks, [])
    #         if solution:
    #             print(f"Decomposition: {solution}")
    #         else:
    #             print("No solution")
    #     else:
    #         print(ret)
    
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

'''
* might need -- not working yet -- possibly not a good optimization either
'''
# def frow(raw_blocks):
#     valid_blocks = []
#     sorted_blocks = sorted(raw_blocks, key=lambda bk: bk[0]*bk[1], reverse=True)

#     for i in range(len(sorted_blocks)):
#         if sorted_blocks[i][1] == cx:
#             return []

#         for j in range(i+1, len(sorted_blocks)):
#             if sorted_blocks[i][1] + sorted_blocks[j][1] == cx:
#                 if sorted_blocks[i][0] == sorted_blocks[j][1] and sorted_blocks[i][1] == sorted_blocks[j][0]:
#                     continue
#                 if sorted_blocks[i][0] > cy or sorted_blocks[j][0] > cy:
#                     continue
                
#                 valid_blocks.append((sorted_blocks[i], sorted_blocks[j]))
#             else:
#                 summed = sorted_blocks[i][1]+sorted_blocks[j][1]
#                 for k in range(j+1, len(sorted_blocks)):
#                     if cx-summed == sorted_blocks[k][1]:
#                         if sorted_blocks[i][0] == sorted_blocks[j][1] and sorted_blocks[i][1] == sorted_blocks[j][0] or \
#                             sorted_blocks[i][0] == sorted_blocks[k][1] and sorted_blocks[i][1] == sorted_blocks[k][0] or \
#                             sorted_blocks[j][0] == sorted_blocks[k][1] and sorted_blocks[j][1] == sorted_blocks[k][0]:
#                             continue
#                         if sorted_blocks[i][0] > cy or sorted_blocks[j][0] > cy or sorted_blocks[k][0] > cy:
#                             continue
#                         if (sorted_blocks[i], sorted_blocks[j], sorted_blocks[k]) in valid_blocks:
#                             continue
#                         valid_blocks.append((sorted_blocks[i], sorted_blocks[j], sorted_blocks[k]))
                    
#     valid_blocks.sort(reverse=True)

#     return valid_blocks

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

