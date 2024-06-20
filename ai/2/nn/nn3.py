import sys; args = sys.argv[1:]
import random
import math

# NN3 - 99.5%

alpha = 0.25

def main():
    inequality, num = extract_input(args[0])
    inputs, outputs = generate_data(inequality, num)    

    best_out_err = float("inf")

    # while True:
    nn, weights = init_nn(inputs[0], outputs[0])
    out_err = 0
    for epoch in range(100):
        out_err = 0
        for i in range(len(inputs)):
            nn[0] = inputs[i]
            out_err += back_propagate(nn, weights, outputs[i])
        out_err *= .5
        if epoch % 10 == 0 and out_err < best_out_err:
            print(f"epoch {epoch}")
            print(f"error {out_err}")
            display(nn, weights)
        if out_err < best_out_err:
            best_out_err = out_err
    
    if out_err < best_out_err:
        display(nn, weights)
        best_out_err = out_err

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
        if layer+1 == len(nn)-1:
            err = prev_err[n] * weights[layer][n]
        else:
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
                preactivation += weights[layer-1][(n * len(nn[layer-1])) + pn] * pnode 
            nn[layer][n] = sigmoid(preactivation)
            preactivation = 0
    
    # output layer no activation
    preactivation = 0
    for n in range(len(nn[-1])):
        preactivation += weights[-1][n] * nn[-2][n]
        nn[-1][n] = preactivation
        preactivation = 0

def generate_data(inequality, num):
    inputs = []
    outputs = []

    for _ in range(10000):
        x = random.uniform(-1.5, 1.5)
        y = random.uniform(-1.5, 1.5)
        inputs.append([x, y, 1])
        if inequality == "<":
            if (x*x + y*y) < num:
                outputs.append([1])
            else:
                outputs.append([0])
        elif inequality == ">":
            if (x*x + y*y) > num:
                outputs.append([1])
            else:
                outputs.append([0])
        elif inequality == ">=":
            if (x*x + y*y) >= num:
                outputs.append([1])
            else:
                outputs.append([0])
        elif inequality == "<=":
            if (x*x + y*y) <= num:
                outputs.append([1])
            else:
                outputs.append([0])

    return inputs, outputs

def init_nn(inp, out):
    nn = []
    weights = []

    if len(out) <= 1:
        nn.append(inp)
        nn.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        nn.append([0, 0, 0, 0, 0, 0])
        nn.append([0])
        nn.append([0])

        for i in range(4): 
            weight = []
            for _ in range(len(nn[i]) * len(nn[i+1])):
                std = math.sqrt(2 / (len(nn[i]) + len(nn[i+1])))
                weight.append(random.gauss(0, std))
                # weight.append(random.random())
            weights.append(weight)
    else:
        nn.append(inp)
        nn.append([0, 0])
        nn.append([0, 0])
        nn.append([0, 0])

        for i in range(2):
            weight = []
            for _ in range(len(nn[i]) * len(nn[i+1])):
                std = math.sqrt(2 / (len(nn[i]) + len(nn[i+1])))
                weight.append(random.gauss(0, std))
                # weight.append(random.random())
            weights.append(weight)
        
        weights.append([random.random(), random.random()])
        
    return nn, weights

def sigmoid(X):
    return 1 / (1 + math.exp(-X))

def sigmoid_prime(X):
    # X = sigmoid(x)
    return X*(1 - X)

def extract_input(inp):
    inequality = ""
    num = ""

    for c in inp[7:]:
        if c in {"<", ">", "="}:
            inequality += c
        else:
            num += c
    
    return inequality, float(num)

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

