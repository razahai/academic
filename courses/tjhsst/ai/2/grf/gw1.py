import sys; args = sys.argv[1:]
import re

# GW1 - 2000/2000 - 100%

def gDirective(directive, graphDS):
    directiveRegex = r"G(G|N)?(\d+)(W(\d+))?(R(\d+))?"
    if (match := re.match(directiveRegex, directive)):
        # G[graphType]#[W#][R#] 
        graphType = match.group(1) or "G" # G (gridworld) is default graphType
        graphSize = int(match.group(2))
        graphRwd = match.group(6) or 12 # default reward = 12
        graphRwd = int(graphRwd)
        if graphType.lower == "n":
            # GGW0 ~= (i.e. congruent symbol; grader doesn't allow) GN
            graphWidth = 0
        else:
            graphWidth = int(match.group(4) or calcWidth(graphType, graphSize)) # width defaults to smallest int, at least sqrt(graphSize)
        
        graph = []
        
        for _ in range(graphSize):
            graph.append(set())

        if graphType.lower() == "g" and graphWidth != 0:
            assumeEdges(graph, graphWidth)

        graphDS["edges"] = graph
        graphDS["type"] = graphType
        graphDS["width"] = graphWidth
        graphDS["rwd"] = graphRwd 
        # initializing vertexProps here because g directive will always be provided
        # whereas v directives might not be - despite this, grfVProps will still need
        # to access vertexProps, so we need to create a default empty state first
        #
        # another way to do this would be to simply check if vProps & the specific vertex
        # exists in graphDS within the grfVProps function and if it doesn't, return {}
        graphDS["vertexProps"] = [{}]*len(graph)
        graphDS["edgeProps"] = {} # this is subject to change since the spec says to combine this with "edges"
            
def vDirective(directive, graphDS):
    directiveRegex = r"V([-\d:,]+)((B)|(-?R(\d+)?)|(T))*"
    if (match := re.match(directiveRegex, directive)):
        # Vvslcs[B|[-]R[#]|T]*
        vslcs = match.group(1)
        vBarrier = match.group(3) or False
        rwdExists = match.group(4) or False
        vRwd = match.group(5) or graphDS["rwd"]
        vTerminal = match.group(6) or False
    
        vertices = set(computeVslcs(vslcs, len(graphDS["edges"])))

        vRwd = int(vRwd)
        if vTerminal:
            # i don't know a more elegant way to do this
            vTerminal = True

        if vBarrier:
            for v in vertices:
                remEdges, newEdges = generateEdges(v, vertices, graphDS["edges"], graphDS["type"].lower(), graphDS["width"])
                [graphDS["edges"][edge[0]].remove(edge[1]) for edge in remEdges] # rem
                [graphDS["edges"][edge[0]].add(edge[1]) for edge in newEdges] # add
                for edge in remEdges:
                    if edge in graphDS["edgeProps"]:
                        graphDS["edgeProps"][edge] = {}

        vProps = {"rwd": vRwd}#, "terminal": vTerminal}
        
        # populate vertexProps
        if rwdExists:
            for v in vertices:
                graphDS["vertexProps"][v] = vProps 
    
def eDirective(directive, graphDS):
    firstDirectiveRegex = r"E(!|\+|\*|~|@)?([-\d:,]+)([=~])([-\d:,]+)((R(\d+)?)|(T))*"
    secondDirectiveRegex = r"E(!|\+|\*|~|@)?([-\d:,]+)([NSEW]+)([=~])((R(\d+)?)|(T))*"
    graph = graphDS["edges"]
 
    if (match := re.match(firstDirectiveRegex, directive)):
        mngmnt = match.group(1) or "~"
        vslcs1 = match.group(2)
        eDirectionality = match.group(3)
        vslcs2 = match.group(4)
        rwdExists = match.group(6) or False
        eRwd = match.group(7) or graphDS["rwd"]
        eTerminal = match.group(8) or False

        eRwd = int(eRwd)
        if eTerminal:
            eTerminal = True
        
        vertices1 = computeVslcs(vslcs1, len(graphDS["edges"]))
        vertices2 = computeVslcs(vslcs2, len(graphDS["edges"]))

        specifiedEdges = list(zip(vertices1, vertices2))
        if eDirectionality == "=":
            # bidirectionality, so the reverse of all edges must also be included
            specifiedEdges.extend(list(zip(vertices2, vertices1)))

        # refactor somehow; while this is fine i feel like we could
        # just do everything before using sets instead of turning it into a set afterwards 
        specifiedEdges = set(specifiedEdges)

        if rwdExists:
            eProps = {"rwd": eRwd}#, "terminal": eTerminal}
        else:
            eProps = {}
            
        for edge in specifiedEdges:
            if mngmnt == "!":
                # remove any extant edges
                graph[edge[0]] -= {edge[1]}
                if edge in graphDS["edgeProps"]:
                    graphDS["edgeProps"][edge] = {}
            elif mngmnt == "+":
                # add new with properties; ignore (skip) extant edges
                if edge[1] in graph[edge[0]]: continue
                graph[edge[0]].add(edge[1])
                graphDS["edgeProps"][edge] = eProps 
            elif mngmnt == "*":
                # add if missing, apply properties both new and previously extant edges
                if not edge[1] in graph[edge[0]]:
                    graph[edge[0]].add(edge[1])
                graphDS["edgeProps"][edge] = eProps
            elif mngmnt == "~":
                # toggle (default); apply properties to newly created edges
                if edge[1] in graph[edge[0]]:
                    graph[edge[0]].remove(edge[1])
                    if edge in graphDS["edgeProps"]:
                        graphDS["edgeProps"][edge] = {}
                else:
                    graph[edge[0]].add(edge[1])
                    graphDS["edgeProps"][edge] = eProps
            elif mngmnt == "@":
                # apply properties to extant edges; don't create new edges
                if edge[1] in graph[edge[0]]:
                    graphDS["edgeProps"][(edge)] = eProps
            
    elif (match := re.match(secondDirectiveRegex, directive)):
        mngmnt = match.group(1) or "~"
        vslcs = match.group(2)
        eDirections = match.group(3)
        eDirectionality = match.group(4)
        rwdExists = match.group(6) or False
        eRwd = match.group(7) or graphDS["rwd"]
        eTerminal = match.group(8) or False

        eRwd = int(eRwd)
        if eTerminal:
            eTerminal = True

        specifiedEdges = generateEdgesFromDirections(vslcs, eDirections, len(graphDS["edges"]), graphDS["width"], eDirectionality)

        specifiedEdges = set(specifiedEdges)

        if rwdExists:
            eProps = {"rwd": eRwd}#, "terminal": eTerminal}
        else:
            eProps = {}

        for edge in specifiedEdges:
            if mngmnt == "!":
                # remove any extant edges
                graph[edge[0]] -= {edge[1]}
                if edge in graphDS["edgeProps"]:
                    graphDS["edgeProps"][edge] = {}
            elif mngmnt == "+":
                # add new with properties; ignore (skip) extant edges
                if edge[1] in graph[edge[0]]: continue
                graph[edge[0]].add(edge[1])
                graphDS["edgeProps"][edge] = eProps 
            elif mngmnt == "*":
                # add if missing, apply properties both new and previously extant edges
                if not edge[1] in graph[edge[0]]:
                    graph[edge[0]].add(edge[1])
                graphDS["edgeProps"][edge] = eProps
            elif mngmnt == "~":
                # toggle (default); apply properties to newly created edges
                if edge[1] in graph[edge[0]]:
                    graph[edge[0]].remove(edge[1])
                    if edge in graphDS["edgeProps"]:
                        graphDS["edgeProps"][edge] = {}
                else:
                    graph[edge[0]].add(edge[1])
                    graphDS["edgeProps"][edge] = eProps
            elif mngmnt == "@":
                # apply properties to extant edges; don't create new edges
                if edge[1] in graph[edge[0]]:
                    graphDS["edgeProps"][(edge)] = eProps
            
def generateEdgesFromDirections(vslcs, directions, size, width, directionality):
    edges = []
    vertices = computeVslcs(vslcs, size)

    for v in vertices:
        for direction in directions:
            if direction == "N":
                if v in range(0, width): continue
                edges.append((v, v-width))
                if directionality == "=":
                    edges.append((v-width, v))
            elif direction == "E":
                if v in range(width-1, size, width): continue
                edges.append((v, v+1))
                if directionality == "=":
                    edges.append((v+1, v))
            elif direction == "S":
                if v in range(size-width, size): continue
                edges.append((v, v+width))
                if directionality == "=":
                    edges.append((v+width, v))
            elif direction == "W":
                if v in range(0, size-width+1, width): continue
                edges.append((v, v-1))
                if directionality == "=":
                    edges.append((v-1, v))
    
    return edges

def generateEdges(v, vertices, edges, type, width):
    remEdges = set()
    newEdges = set()

    if type == "n":
        # n graphs don't have any implicit edges, so i assume you simply have to remove all edges?
        remEdges.update(set(zip([v]*len(edges[v]), edges[v])))
    else:
        # this could be a lot simpler and if you are intending to use this method,
        # try thinking about how to do it yourself, because right now this code is pretty stupid
        possibleNbrs = set()
        edge = {v0 for v0 in edges[v]}
    
        if not v in range(0, len(edges)-width+1, width):
            possibleNbrs.add(v-1)
        if not v in range(width-1, len(edges), width):
            possibleNbrs.add(v+1)
        if not v in range(0, width):
            possibleNbrs.add(v-width)
        if not v in range(len(edges)-width, len(edges)):
            possibleNbrs.add(v+width)
        
        for v1 in possibleNbrs:
            if v1 in vertices:
                # since W is set of vertices and X = V-W, we only care about the complement of W
                continue
            
            removedEdge = False
            removedEdgeRev = False
            if v1 in edges[v]:
                remEdges.add((v, v1))
                edge.remove(v1)
                removedEdge = True
            if v in edges[v1]:
                remEdges.add((v1, v))
                removedEdgeRev = True

            # native edges according to gridworld type
            if not removedEdge:
                newEdges.add((v, v1))
            if not removedEdgeRev:
                newEdges.add((v1, v))
        # for all jumps
        for v1 in (({v0 for v0 in range(len(edges)) if v in edges[v0]} - possibleNbrs) | edge):
            if v1 in vertices: 
                # same reasoning as above
                continue
            if v1 in edges[v]:
                remEdges.add((v, v1))
            if v in edges[v1]:
                remEdges.add((v1, v))
        
    return remEdges, newEdges

def computeVslcs(vslcs, graphSize):
    indivVslcs = vslcs.split(",")
    vertices = []
    possibleVerts = list(range(graphSize))

    for vslc in indivVslcs:
        vslcNum = vslc.split(":")
        
        if len(vslcNum) == 3:
            # n:n:n, n::n, ::n, n::, :n:, :n:n
            if vslcNum[0] and vslcNum[1] and vslcNum[2]:
                vertices.extend(possibleVerts[int(vslcNum[0]):int(vslcNum[1]):int(vslcNum[2])])
            elif vslcNum[0] and not vslcNum[1] and vslcNum[2]:
                vertices.extend(possibleVerts[int(vslcNum[0])::int(vslcNum[2])])
            elif not vslcNum[0] and not vslcNum[1] and vslcNum[2]:
                vertices.extend(possibleVerts[::int(vslcNum[2])])
            elif not vslcNum[0] and vslcNum[1] and not vslcNum[2]:
                vertices.extend(possibleVerts[:int(vslcNum[1]):])
            elif vslcNum[0] and not vslcNum[1] and not vslcNum[2]:
                vertices.extend(possibleVerts[int(vslcNum[0])::])
            elif not vslcNum[0] and vslcNum[1] and vslcNum[2]:
                vertices.extend(possibleVerts[:int(vslcNum[1]):int(vslcNum[2])])
            elif not vslcNum[0] and not vslcNum[1] and not vslcNum[2]:
                vertices.extend(possibleVerts[::])
        elif len(vslcNum) == 2:
            # n:n, :n, n:
            if vslcNum[0] and vslcNum[1]:
                vertices.extend(possibleVerts[int(vslcNum[0]):int(vslcNum[1])])
            elif vslcNum[0] and not vslcNum[1]:
                vertices.extend(possibleVerts[int(vslcNum[0]):])
            elif not vslcNum[0] and vslcNum[1]:
                vertices.extend(possibleVerts[:int(vslcNum[1])])
            elif not vslcNum[0] and not vslcNum[1]:
                vertices.extend(possibleVerts[:])
        elif len(vslcNum) == 1:
            # n
            vertices.append(possibleVerts[int(vslcNum[0])])
    
    return vertices

def calcWidth(graphType, graphSize):
    if graphType.lower() == "n":
        return 0
    for i in range(1, graphSize+1):
        for j in range(1, graphSize+1):
            if i<j: continue
            if i*j == graphSize:
                return i # only need width? 

def assumeEdges(graph, graphWidth):
    for v in range(len(graph)):
        # corners
        if v == 0:
            graph[v].add(v+1)
            if len(graph) > graphWidth:
                graph[v].add(v+graphWidth)
        elif v == graphWidth-1:
            graph[v].add(v-1)
            if len(graph) > graphWidth:
                graph[v].add(v+graphWidth)
        elif v == len(graph)-graphWidth:
            graph[v].add(v+1)
            if len(graph) > graphWidth:
                graph[v].add(v-graphWidth)
        elif v == len(graph)-1:
            graph[v].add(v-1)
            if len(graph) > graphWidth:
                graph[v].add(v-graphWidth)
        # edges
        elif v in range(1, graphWidth-1):
            graph[v].add(v+1)
            graph[v].add(v-1)
            if len(graph) > graphWidth:
                graph[v].add(v+graphWidth)
        elif v in range(graphWidth, len(graph)-graphWidth, graphWidth):
            graph[v].add(v+1)
            if len(graph) > graphWidth:
                graph[v].add(v+graphWidth)
                graph[v].add(v-graphWidth)
        elif v in range((graphWidth*2)-1, len(graph)-1, graphWidth):
            graph[v].add(v-1)
            if len(graph) > graphWidth:
                graph[v].add(v+graphWidth)
                graph[v].add(v-graphWidth)
        elif v in range(len(graph)-graphWidth+1, len(graph)-1):
            if len(graph) > graphWidth:
                graph[v].add(v-graphWidth)
            graph[v].add(v+1)
            graph[v].add(v-1)
        # the rest
        else:
            graph[v].add(v+1)
            graph[v].add(v-1)
            if len(graph) > graphWidth:
                graph[v].add(v-graphWidth)
                graph[v].add(v+graphWidth)

def stringifyEdges(edges, width):
    edgeStr = ""
    jumpStr = ""
    possibilities = {
        "N": "N",
        "E": "E",
        "S": "S",
        "W": "W",
        "EN": "L",
        "SW": "7",
        "ES": "r",
        "NW": "J",
        "EW": "-",
        "NS": "|",
        "ENSW": "+",
        "ENW": "^",
        "ESW": "v",
        "ENS": ">",
        "NSW": "<",
        "": "."
    }
    jumps = set()
    typeJumps = {"~": set(), "=": set()}
    
    for v,e in enumerate(edges):
        directions = ""
    
        for v1 in e:
            if width == 0: # type n
                if (v, v1) in jumps: continue
                if v == v1:
                    typeJumps["~"].add((v,v1))
                    jumps.add((v, v1))
                else:
                    if v in edges[v1]:
                        typeJumps["="].add((v,v1))
                    else:
                        typeJumps["~"].add((v,v1))
                    jumps.add((v, v1))
                    jumps.add((v1, v))
            else:
                if v1 == v-1 and not v in range(0, len(edges)+1, width):
                    directions += "W"
                elif v1 == v+1 and not v in range(width-1, len(edges), width):
                    directions += "E"
                elif v1 == v-width and not v in range(0, width):
                    directions += "N"
                elif v1 == v+width and not v in range(len(edges)-width, len(edges)):
                    directions += "S"
                else:
                    # jump
                    if (v, v1) in jumps: continue
                    if v == v1:
                        typeJumps["~"].add((v,v1))
                        jumps.add((v, v1))
                    else:
                        if v in edges[v1]:
                            typeJumps["="].add((v,v1))
                        else:
                            typeJumps["~"].add((v,v1))
                        jumps.add((v, v1))
                        jumps.add((v1, v))

        # so possiblities dict matches this string
        if width != 0:
            directions = "".join(sorted(directions))
            edgeStr += possibilities[directions]

    # compute jumpStr
    for typ in typeJumps:
        if len(typeJumps[typ]) == 0: continue
        leftSide = ""
        rightSide = ""

        for edge in typeJumps[typ]:
            leftSide += f"{edge[0]},"
            rightSide += f"{edge[1]},"
        
        jumpStr += f"{leftSide[:-1]}{typ}{rightSide[:-1]};"
    
    return edgeStr, jumpStr[:-1]

def displayEdges(edgesStr, width, type):
    edgesStr2D = ""
    jumpLoc = edgesStr.find("Jumps")
    if jumpLoc != -1:
        jumpsStr = edgesStr[edgesStr.find("Jumps"):]
        edgesStr = edgesStr[:edgesStr.find("Jumps")]
    else:
        jumpsStr = ""
    
    if type.lower() == "n" or width == 0:
        if jumpsStr:
            edgesStr2D += jumpsStr
        return edgesStr2D

    # Sidenote: I don't know why the grader doesn't accept the lazy way of printing out jumps 
    # (i.e 1=2;3=4;5=6 as opposed to 1,3,5=2,4,6) and printing out vertex/edge properties
    # (i.e v:{rwd: int} as opposed to v: rwd: int) even though the spec says otherwise - the only 
    # reason I had to work on this lab for like 3 more hours was because the grader was spitting out 
    # the "Spurious key" error even when it would have the key in its own Expected run - the only difference
    # was my run had different formatting - so I changed it exactly to the Expected formatting and got 2000/2000
    
    for k in range(0, len(edgesStr), width):
        edgesStr2D += edgesStr[k:k+width] + "\n"
    
    edgesStr2D = edgesStr2D.strip("\n")

    if jumpsStr:
        edgesStr2D += f"\n{jumpsStr}"

    return edgesStr2D

def grfParse(lstArgs): 
    # graphDS spec: {"type": str, "width": int, "rwd": int, "edges": list[set[int]], "vertexProps": list[dict]}
    graphDS = {}        

    for arg in lstArgs:
        if arg.lower().startswith("g"): gDirective(arg, graphDS)
        elif arg.lower().startswith("v"): vDirective(arg, graphDS)
        elif arg.lower().startswith("e"): eDirective(arg, graphDS)

    return graphDS

def grfSize(graphDS):
    # just so someone reading this isn't confused:
    # yes technically |e| can != |v|, but our data structure is obviously an adjacency
    # list so it's a list[set] of size v where each index is the list of edges that a
    # specific vertex has 
    return len(graphDS["edges"]) 

def grfNbrs(graphDS, vert):
    return graphDS["edges"][vert]

def grfGProps(graphDS):
    props = {}
    if graphDS["type"].lower() != "n":
        # "type" could be removed in favor of N graph widths = -1 instead of 0
        # this does not technically follow the spec, but since width is essentially
        # useless for N graphs, i think it's fine if we deviate from the spec and use -1 instead of 0
        props["width"] = graphDS["width"]
    props["rwd"] = graphDS["rwd"]
    return props

def grfVProps(graphDS, v):
    return graphDS["vertexProps"][v]

def grfEProps(graphDS, v1, v2):
    if (v1, v2) in graphDS["edgeProps"]:
        return graphDS["edgeProps"][(v1, v2)]
    return {}

def grfStrEdges(graphDS):
    edgeStr, jumpStr = stringifyEdges(graphDS["edges"], graphDS["width"])
    outputStr = (edgeStr if graphDS["type"].lower() != "n" and graphDS["width"] != 0 else "") + ("\nJumps: " + jumpStr if jumpStr else "")
    return outputStr

def grfStrProps(graphDS):
    propsOutput = ""
    
    # gprops
    gProps = grfGProps(graphDS)
    if "rwd" in gProps:
        propsOutput += f"rwd: {gProps['rwd']}"
    if "width" in gProps:
        if propsOutput:
            propsOutput += ", "
        propsOutput += f"width: {gProps['width']}\n"
    else:
        if propsOutput:
            propsOutput += "\n"
    
    # vprops
    vProps = {}
    for v in range(len(graphDS["vertexProps"])):
        if len(graphDS["vertexProps"][v]) != 0: # exists
            vProp = grfVProps(graphDS, v)
            if not vProp["rwd"] in vProps:
                vProps[vProp["rwd"]] = set()
            vProps[vProp["rwd"]].add(v)
    for rwd in vProps:
        allVertices = ""
        for vert in vProps[rwd]:
            allVertices += f"{vert}, "
        propsOutput += f"{allVertices[:-2]}: rwd: {rwd}\n"
    
    # eprops
    eProps = {}
    for e in graphDS["edgeProps"]:
        if len(graphDS["edgeProps"][e]) != 0:
            v1, v2 = e
            eProp = grfEProps(graphDS, v1, v2)
            if not eProp["rwd"] in eProps:
                eProps[eProp["rwd"]] = set()
            eProps[eProp["rwd"]].add(e)
    for rwd in eProps:
        allEdges = ""
        for edge in eProps[rwd]:
            allEdges += f"{edge}, "
        propsOutput += f"{allEdges[:-2]}: rwd: {rwd}\n"
    # remove last \n
    propsOutput = propsOutput[:-1]
    
    return propsOutput


def main():
    graphDS = grfParse(args)
    edgesStr = grfStrEdges(graphDS)
    propsStr = grfStrProps(graphDS)

    print(displayEdges(edgesStr, graphDS["width"], graphDS["type"]))
    print(propsStr)
    

if __name__ == "__main__":
    main()

