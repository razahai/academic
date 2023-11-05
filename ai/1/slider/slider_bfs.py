import sys; args = sys.argv[1:]
import time

# * BFS - 100% (I'm pretty sure grader kinda broke, I did not optimize at all)

start_time = time.time()

BAND_WIDTH = 5;

def main():
    global gWIDTH
    global gHEIGHT

    start = args[0]
    goal = ""

    if len(args) > 1:
        goal = args[1]
    else:
        goal = ''.join(sorted(start)) # default goal state

    dimensions = get_dimensions(len(start))
    gWIDTH = dimensions[0]
    gHEIGHT = dimensions[1]
    
    out = bfs(start, goal)
    pretty(out[0])
    print(f"Steps: {out[1]}")
    print("Time: {:.2f}s".format(time.time()-start_time))

def bfs(start, goal):
    q = [start]
    
    if start == goal:
        return [q, 0]

    visited = {start: ""}

    while q:
        node = q.pop(0)
        
        for n in neighbors(node):
            if n in visited: continue
            #if n == goal: return visited
            if n == goal:
                path = []
                visited[n] = node
                current = visited[n]
                steps = 0

                path.append(n)

                while current != "":
                    steps += 1
                    path.append(current)
                    current = visited[current]

                return [path[::-1], steps] 
            visited[n] = node
            q.append(n)
        
    return [[start], -1]

def icc(seq):
    prev = ''.join(sorted(seq))

def pretty(puzzles):
    def band(current, last=False):
        for i in range(len(current)):
            print(current[i])
        
        if not last:
            print("\n")
    
    current_band = []

    for i in range(len(puzzles)):
        puzzle = []
        k = 0

        for j in range(gHEIGHT):
            puzzle.append(puzzles[i][k:k+gWIDTH])
            k+=gWIDTH

        for n in range(len(puzzle)):
            if (len(current_band) > n):
                current_band[n] += puzzle[n]+" "
            else:
                current_band.append(puzzle[n]+" ")

        if (i+1) % BAND_WIDTH == 0:
            if i+1 >= len(puzzles):
                band(current_band, True)
            else:
                band(current_band)
            current_band = []

    band(current_band, True)

def neighbors(puzzle: str):
    u_idx = puzzle.find("_")
    positions = []

    row = u_idx//gHEIGHT
    col = u_idx%gWIDTH

    def swap(l, i, j):
        temp = l[i]
        l[i] = l[j]
        l[j] = temp

    if (row-1) > -1:
        pot = [*puzzle]
        swap(pot, u_idx, u_idx-gWIDTH)
        positions.append(''.join(pot))
    
    if row+1 < gHEIGHT:
        pot = [*puzzle]
        swap(pot, u_idx, u_idx+gWIDTH)
        positions.append(''.join(pot))
    
    if (col+1) < gWIDTH:
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

if __name__ == "__main__":
    main()

