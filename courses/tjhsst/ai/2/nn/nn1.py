import sys; args = sys.argv[1:]
import math

# NN1 - 100%

def main():
    weights = [list(map(float, line.split(" "))) for line in open(args[0]).read().splitlines()]
    tfn = args[1] # T1: linear; T2: ramp/relu; T3: logistic/sigmoid; T4: 2(T3)-1
    inputs = list(map(float, args[2:]))

    print("weights:", weights)
    
    nn = init_nn(inputs, weights)
    print("starting NN:", nn)

    feed_forward(nn, weights, tfn)
    print("forward propagation:", nn)

    output = output_layer(nn, weights)
    for v in output:
        print(v[:6], end=" ")

def init_nn(inputs, weights):
    
    _nn = []

    for l in range(len(weights)-1, -1, -1):
        if l == len(weights)-1: # output layer
            _nn.append([0] * len(weights[l]))
        else:
            _nn.append([0] * (len(weights[l]) // len(_nn[len(_nn)-1]))) # int div just in case
    
    _nn.reverse()
    _nn[0] = inputs

    return _nn

def feed_forward(nn, weights, fn):
    for layer in range(1, len(nn)):
        preactivation = 0

        for n in range(len(nn[layer])):
            for pn, pnode in enumerate(nn[layer-1]):
                preactivation += weights[layer-1][(n * len(nn[layer-1])) + pn] * pnode # here it would be dot(W, X) + B but there's no bias and all we are given is one-dimensional vectors
            nn[layer][n] = activation_fn(preactivation, fn)
            preactivation = 0        

def output_layer(nn, weights):
    output = []

    for n, node in enumerate(nn[len(nn)-1]):
        # we need to handle this in strings because the grader wants -0 instead of 0 for some reason
        # UPDATE 5/3/24 13:44 EST: i don't know if the above is true anymore since i thought of the output layer wrong conceptually
        out = str(weights[len(nn)-1][n] * node)
        if out == "0" and (weights[len(nn)-1][n] < 0 or node < 0):
            out = "-0.0"
        output.append(out)
    
    return output


def activation_fn(preactivation, fn):
    if fn.upper() == "T1":
        # linear
        return preactivation
    elif fn.upper() == "T2":
        # ramp/relu
        return relu(preactivation)
    elif fn.upper() == "T3":
        # logistic/sigmoid
        return sigmoid(preactivation)
    elif fn.upper() == "T4":
        # 2(T3)-1
        return (2 * sigmoid(preactivation)) - 1

# activation functions
def relu(X):
    return X if X >= 0 else 0

def sigmoid(X):
    return 1 / (1 + math.exp(-X))

if __name__ == "__main__":
    main()

