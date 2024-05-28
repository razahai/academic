import sys; args = sys.argv[1:]
import random
import math

# NN2 - 90.91% :(

alpha = 0.35

def main():
    gates = open(args[0]).read().splitlines()
    inputs = []
    outputs = []
    
    f = open("output1.txt", "w")
    f.write("Error\n")

    for gate in gates:
        inp, out = list(map(lambda s: list(map(float, s.strip().split(" "))), gate.split("=>")))
        inputs.append(inp + [1])
        outputs.append(out)

    nn, weights = init_nn(inputs[0], outputs[0])
    best_out_err = float("inf")

    out_err = 0
    for epoch in range(50000):
        out_err = 0
        for i in range(len(inputs)):
            nn[0] = inputs[i]
            out_err += bp(nn, weights, outputs[i])
        out_err *= .5
        if epoch % 1000 == 0:
            f.write(str(out_err) + "\n")
        if epoch % 1000 == 0 and out_err < best_out_err:
            display(nn, weights)
        if out_err < best_out_err:
            best_out_err = out_err
    
    if out_err < best_out_err:
        display(nn, weights)

def back_propagate(nn, weights, outputs):
    feed_forward(nn, weights)
    # E = t_i - y_i^l
    output_err = [outputs[i] - nn[-1][i] for i in range(len(outputs))]
    prev_err = output_err
    
    G = []

    for layer in range(len(nn)-2, -1, -1):
        layer_err = calculate_error(nn, weights, layer, prev_err)
        gradient = []   
        if layer == len(nn)-2:
            for j in range(len(prev_err)):
                _g = nn[layer][j] * prev_err[j]
                gradient.append(_g)
        else:
            for j in range(len(prev_err)):
                for i in range(len(nn[layer])):
                    _g = nn[layer][i] * prev_err[j]
                    gradient.append(_g)
        G.append(gradient)
        prev_err = layer_err
    
    G.reverse()
    
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            weights[i][j] += (alpha * G[i][j])
    
    return sum(list(map(lambda err: err*err, output_err)))
    
def calculate_error(nn, weights, layer, prev_err):
    errs = []
    
    # E_i^layer = ((sigma)j w_ij^layer * E_j^layer+1) * f'(@x_i^layer)
    for n in range(len(nn[layer])):
        err = 0
        for j in range(len(nn[layer+1])):
            if layer+1 == len(nn)-1:
                err += prev_err[j] * weights[layer][j]
            else:
                err += prev_err[j] * weights[layer][n * len(nn[layer+1]) + j]
        err *= sigmoid_prime(nn[layer][n])
        errs.append(err)

    return errs

def feed_forward(nn, weights):
    for layer in range(1, len(nn)-1):
        preactivation = 0

        for n in range(len(nn[layer])):
            for pn, pnode in enumerate(nn[layer-1]):
                preactivation += weights[layer-1][(n * len(nn[layer-1])) + pn] * pnode 
            nn[layer][n] = sigmoid(preactivation)
            preactivation = 0
    
    # output layer no activation
    preactivation = 0
    for n in range(len(nn[-1])):
        for pn, pnode in enumerate(nn[-2]):
            preactivation += weights[-1][pn] * pnode
            #(n * len(nn[-1])) + pn
        nn[-1][n] = preactivation
        preactivation = 0

def init_nn(inp, out):
    nn = []
    weights = []

    if len(out) <= 1:
        # hardcoding the (1 + # inputs) 2 1 1 architecture
        nn.append(inp)
        nn.append([0, 0])
        nn.append([0])
        nn.append([0])

        # init weights 2(1 + # inputs) 2 1
        for i in range(3): 
            weight = []
            for _ in range(len(nn[i]) * len(nn[i+1])):
                weight.append(random.random())
            weights.append(weight)
        
        # weights = [[0, 0, 0, 0, 0, 0], [0, 0], [0]]
    else:
        nn.append(inp)
        nn.append([0, 0])
        nn.append([0, 0])
        nn.append([0, 0])

        for i in range(2):
            weight = []
            for _ in range(len(nn[i]) * len(nn[i+1])):
                weight.append(random.random())
            weights.append(weight)
        
        weights.append([random.random(), random.random()])
        # weights = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0]]

    return nn, weights

def sigmoid(X):
    return 1 / (1 + math.exp(-X))

def sigmoid_prime(X):
    # X = sigmoid(x)
    return X*(1 - X)

def display(nn, weights):
    layer_cts = "Layer counts "
    weight_outputs = ""

    for layer in range(len(nn)):
        layer_cts += f"{len(nn[layer])} "
    
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            weight_outputs += f"{weights[i][j]} "
        weight_outputs += "\n"

    print(layer_cts.strip())
    print(weight_outputs[:-2])

if __name__ == "__main__":
    main()

