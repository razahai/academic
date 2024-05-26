import sys; args = sys.argv[1:]
import random
import math

# NN2 - undefined%

def main():
    gates = open(args[0]).read().splitlines()
    
    for gate in gates:
        inputs, outputs = list(map(lambda s: list(map(float, s.strip().split(" "))), gate.split("=>")))
        nn, weights = init_nn(inputs)
        for epoch in range(5000):
            back_propagate(nn, weights, outputs)
        print(nn)
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
        for i in range(len(nn[layer])):
            for j in range(len(prev_err)):
                _g = nn[layer][i] * prev_err[j]
                gradient.append(_g)
        G.append(gradient)
        prev_err = layer_err
    
    G.reverse()

    for i in range(len(weights)):
        for j in range(len(weights[i])):
            weights[i][j] += 0.1 * G[i][j]

    return False
    
def calculate_error(nn, weights, layer, prev_err):
    errs = []
    
    # E_i^layer = ((sigma)j w_ij^layer * E_j^layer+1) * f'(@x_i^layer)
    for n in range(len(nn[layer])):
        err = 0
        for j in range(len(nn[layer+1])):
            err += prev_err[j] * weights[layer][n * len(nn[layer+1]) + j]
        err *= sigmoid_prime(nn[layer][n])
        errs.append(err)

    return errs

def feed_forward(nn, weights):
    for layer in range(1, len(nn)-1):
        preactivation = 0

        for n in range(len(nn[layer])):
            for pn, pnode in enumerate(nn[layer-1]):
                preactivation += weights[layer-1][(n * len(nn[layer-1])) + pn] * pnode # here it would be dot(W, X) + B but there's no bias and all we are given is one-dimensional vectors
            nn[layer][n] = sigmoid(preactivation)
            preactivation = 0
    
    # output layer no activation
    preactivation = 0
    for n in range(len(nn[-1])):
        for pn, pnode in enumerate(nn[-2]):
            preactivation += weights[-1][(n * len(nn[-1])) + pn] * pnode
        nn[-1][n] = preactivation
        preactivation = 0

def init_nn(inputs):
    nn = []
    weights = []

    # hardcoding the (1 + # inputs) 2 1 1 architecture
    nn.append(inputs + [1])
    nn.append([0, 0])
    nn.append([0])
    nn.append([0])

    # init weights 2(1 + # inputs) 2 1
    for i in range(3): 
        weight = []
        for _ in range(len(nn[i]) * len(nn[i+1])):
            weight.append(random.uniform(0, 1))
        weights.append(weight)

    # weights = [[2, 1, 1, 0, 2, 3], [1/2, 3/4], [7/8]]

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

