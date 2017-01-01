import numpy as np


# This block of code defines our sigmoid function and its derivative. This
# is used to change the networks guess based on how wrong the last guess was.

def nonlin(x, deriv=False):
    if (deriv == True):
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


# This is the set of training data used to train the network. Sigmoid
# Networks can find patterns in sets of data that span between 0 and
# 1. For this reason a binary example works perfectly. In this
# example only the first line will be labeled with a 1. This Data set has a
# simple set of rules determining which pattern the neural network is looking
# for however they can be used for anything from this, to facial recognition
# software.

TrainingSet = np.array([[0, 0, 1],
                        [0, 1, 1],
                        [1, 0, 1],
                        [1, 1, 1]])


# This is how you tell the neural network which patterns in the training set
# is the pattern you are looking for.

Answers = np.array([[1],
                    [0],
                    [0],
                    [0]])


# This seeds the initial guess of the network. This makes the network guess
# the same initial guess every time, making it easier to see how changing
# the network changes the result.

np.random.seed(1)


# This generates the synaptic guesses which are normalized around 0.  Their
# sizes are based off of the size of the input and the output.
syn0 = 2 * np.random.random((3, 4)) - 1
syn1 = 2 * np.random.random((4, 1)) - 1


# This loop trains the network to be able to recognize the designated
# pattern. The number in xrange('') will determine how many times the network
# trains itself based of the set it was given.

for j in xrange(60000):


    # This is where data is actually fed through the network. It is a series
    # of layers and synapses being dotted together then fed through the
    # sigmoid function.

    layer0 = TrainingSet
    layer1 = nonlin(np.dot(layer0, syn0))
    layer2 = nonlin(np.dot(layer1, syn1))


    # This line determines how wrong the NN was.

    layer2_error = Answers - layer2


    # The binary output of the network. There will be one output for every
    # row in the training set data. When the Network is properly trained this
    #  will match the Answers Matrix.

    output=np.round(layer2)


    # This loop will print the error of the NN and the networks output every
    # 10,000 iterations.

    if (j % 10000) == 0:

        print "Error:" + str(np.mean((np.abs(layer2_error))))

        print output


    # This line determines which direction the answer needs to go, as well as
    #  how much the synapses should change based on how wrong the NN was.

    layer2_delta = layer2_error * nonlin(layer2, deriv=True)


    # This line determines how much layer 1 contributed to the error.

    layer1_error = layer2_delta.dot(syn1.T)

    # This line determines which direction the answer needs to go, as well as
    # how much the synapses should change based on how wrong the NN was.

    layer1_delta = layer1_error * nonlin(layer1, deriv=True)


    # Finally the synapses are adjusted based on the above calculations.

    syn1 += layer1.T.dot(layer2_delta)
    syn0 += layer0.T.dot(layer1_delta)