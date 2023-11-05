import sys; args = sys.argv[1:]
from time import perf_counter

# * Get test cases from compsci.sites.tjhsst.edu
# * WL - ~97.11%

def main():
    lines = open(args[0]).read().splitlines()
    start_time = perf_counter()

    graph = create_graph(lines)
    
    if len(args) > 1:
        word1 = args[1]
        word2 = args[2]
        md = metadata(lines, graph, word1)
        result(lines, graph, start_time, md, word1, word2)
    else:
        md = metadata(lines, graph)
        result(lines, graph, start_time, md)

def create_graph(lines):
    graph = []

    lookup = {abc: {} for abc in "abcdefghijklmnopqrstuvwxyz"}

    for i in range(len(lines)):
        graph.append(set())
        partials = create_lookup_partials(lines[i])
        
        for p in partials:
            if not p in lookup[lines[i][0]]:
                lookup[lines[i][0]][p] = set()
            lookup[lines[i][0]][p].add(i)
            if not p in lookup[lines[i][-1]]:
                lookup[lines[i][-1]][p] = set()
            lookup[lines[i][-1]][p].add(i)

    for lu in lookup: # all letters
        for k in lookup[lu]: # all partials
            for j in lookup[lu][k]: # all words that are neighbors
                for o in lookup[lu][k]:
                    if o == j: continue
                    graph[j].add(o)

    return graph

def create_lookup_partials(word):
    partials = set()
    for i in range(len(word)):
        partials.add(word[:i]+"?"+word[i+1:])
    return partials

def result(lines, graph, start_time, md, word1="", word2=""):
    print(f"Word count: {len(lines)}")
    print(f"Edge count: {int(md[0]/2)}")
    print(f"Degree List: {[k[0] for k in md[1]]}")
    print("Construction time: {:.1f}s".format(perf_counter()-start_time))

    if word1:
        bfs_res = bfs(graph, lines, word1, md[6], word2)
        print(f"Second degree word: {md[2]}")
        print(f"Connected component size count: {md[3]}")
        print(f"Largest component size: {md[4]}")
        print(f"K2 count: {md[5][0]}")
        print(f"K3 count: {md[5][1]}")
        print(f"K4 count: {md[5][2]}")
        print(f"Neighbors: {[lines[k] for k in graph[md[6]]]}")
        print(f"Farthest: {bfs_res[1]}")
        print(f"Path: {bfs_res[0]}")
        

def metadata(lines, graph, word1=""):
    # // word index
    word1_idx = -1
    
    # edge
    edge_count = 0
    
    # degree
    degree_list = []
    degree_backlog = {}
    degree_inc = 0
    
    # component
    cmp_visited = set()
    cmp_distinct = set()
    cmp_amt = 0
    cmp_largest = 0

    # -> kn
    k2 = 0
    k3 = 0
    k4 = 0 

    for i in range(len(graph)):
        length = len(graph[i])

        if lines[i] == word1:
            word1_idx = i
        
        # num edges
        edge_count += length
        
        # degree list
        if length == degree_inc:
            degree_list.append([1, lines[i]])
            degree_inc += 1

            if length in degree_backlog:
                degree_list[length][0] += degree_backlog[length][0]
                degree_backlog.pop(length) # o(1)
        elif len(degree_list) > length:
            degree_list[length][0] += 1
        elif length in degree_backlog:
            degree_backlog[length][0] += 1
        else:
            degree_backlog[length] = [1, lines[i]]

        # component
        if not i in cmp_visited:
            component = set()
            q = [i]
            ptr = 0

            while ptr < len(q):
                popped = q[ptr]
                ptr += 1
                if popped in cmp_visited: continue
                
                component |= graph[popped]
                
                for j in graph[popped]:
                    q.append(j)
                
                cmp_visited.add(popped)            
            cmp_visited.add(i)

            cmp_length = len(component)
            if cmp_length > cmp_largest:
                cmp_largest = cmp_length
            if not cmp_length in cmp_distinct:
                cmp_amt += 1
            
            # kn
            if cmp_length == 2:
                k2 += 1
            elif cmp_length == 3:
                isk = True
                for k in component:
                    for l in component:
                        if l == k: continue
                        if not check_edge(lines[k], lines[l]): 
                            isk = False
                            break
                if isk:
                    k3 += 1
            elif cmp_length == 4:
                isk = True
                for k in component:
                    for l in component:
                        if l == k: continue
                        if not check_edge(lines[k], lines[l]): 
                            isk = False
                            break
                if isk:
                    k4 += 1

            cmp_distinct.add(cmp_length)

    if degree_backlog:
        for b in degree_backlog:
            degree_list.insert(b, degree_backlog[b])
    second_degree_word = degree_list[-2][1]

    return [edge_count, degree_list, second_degree_word, cmp_amt, cmp_largest, [k2, k3, k4], word1_idx]    

def bfs(graph, lines, word1, word1_idx, word2):
    q = [word1_idx]
    ptr = 0
    path = []
    
    max_distance = 0
    max_dist_node = word1

    if word1 == word2:
        path = q

    visited = {word1: ("", 0)}

    while ptr < len(q):
        node = q[ptr]
        ptr += 1

        for nbr in graph[node]:
            if lines[nbr] in visited: continue
            if lines[nbr] == word2:
                path_arr = []
                visited[lines[nbr]] = (lines[node], visited[lines[node]][1]+1)
                current = visited[lines[nbr]][0]
                path_arr.append(lines[nbr])
                
                while current != "":
                    path_arr.append(current)
                    current = visited[current][0]
                
                path = path_arr[::-1]
            visited[lines[nbr]] = (lines[node], visited[lines[node]][1]+1)
            q.append(nbr)
            if visited[lines[nbr]][1] > max_distance:
                max_distance = visited[lines[nbr]][1]
                max_dist_node = lines[nbr]
    
    return [path, max_dist_node]

def check_edge(word1, word2): 
    return True if len([True for c1, c2 in zip(word1, word2) if c1 != c2]) == 1 else False

if __name__ == "__main__":
    main()

