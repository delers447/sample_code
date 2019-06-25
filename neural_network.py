
import numpy as np
import math, random

def sigmoid(x):
    return 1 / ( 1 + np.exp(-x)) #sigmoid

def dsigmoid(y):
    return y * (1 - y) #sigmoid

def tanh(x):
    return (2 / (1 + np.exp(-2 * x))) - 1

def dtanh(x):
    return 1 - tanh(x) ** 2

def leaky_relu(x):
    return np.where(x < 0, .01*x, x)

def d_leaky_relu(x):
    return np.where(x < 0, .01, 1)

class NeuralNetwork:
    def __init__(self, numI, numH, numO):
        self.learning_rate = .000_1
        self.input_nodes = numI
        self.hidden_nodes = numH
        self.output_nodes = numO

        self.weights_ih = np.random.random((self.hidden_nodes, self.input_nodes))
        signs_of_weights_ih = np.random.choice([-1, 1], size=(self.hidden_nodes, self.input_nodes))
        self.weights_ih *= signs_of_weights_ih
        self.weights_ho = np.random.random((self.output_nodes, self.hidden_nodes))
        signs_of_weights_ho = np.random.choice([-1, 1], size=(self.output_nodes, self.hidden_nodes))
        self.weights_ho *= signs_of_weights_ho
        #need to make the weights both positive and negative

        self.bias_h = np.random.random((self.hidden_nodes, 1))
        self.bias_o = np.random.random((self.output_nodes, 1))

    def feedforward(self, input_array):
        #LOTS OF MATRIX MATH!
        inputs = np.array(input_array).reshape(self.input_nodes, 1)

        hidden_guess = sigmoid(np.matmul(self.weights_ih, inputs) + self.bias_h)
        output_guess = sigmoid(np.matmul(self.weights_ho, hidden_guess) + self.bias_o)

        return output_guess

    def train(self, inputs_list, answers_list):
        inputs = np.array(inputs_list).reshape(self.input_nodes, 1)
        answers = np.array(answers_list).reshape(self.output_nodes, 1)
        hidden_guess = sigmoid(np.matmul(self.weights_ih, inputs) + self.bias_h)
        output_guess = sigmoid(np.matmul(self.weights_ho, hidden_guess) + self.bias_o)

        #calculate the errors: Error = Answer - Guess
        output_errors = answers - output_guess
        hidden_errors =  np.matmul(self.weights_ho.T, output_errors)

        output_gradient = self.learning_rate * output_errors * dsigmoid(output_guess)
        weights_ho_delta = np.matmul(output_gradient, hidden_guess.transpose())
        self.weights_ho += weights_ho_delta
        self.bias_o += output_gradient

        hidden_gradient = self.learning_rate * hidden_errors * dsigmoid(hidden_guess)
        weights_ih_delta = np.matmul(hidden_gradient, inputs.transpose())
        self.weights_ih += weights_ih_delta
        self.bias_h += hidden_gradient

    def feedforward_tanh(self, input_array):
        #LOTS OF MATRIX MATH!
        inputs = np.array(input_array).reshape(self.input_nodes, 1)

        hidden_guess = tanh(np.matmul(self.weights_ih, inputs) + self.bias_h)
        output_guess = tanh(np.matmul(self.weights_ho, hidden_guess) + self.bias_o)

        return output_guess

    def train_tanh(self, inputs_list, answers_list):
        inputs = np.array(inputs_list).reshape(self.input_nodes, 1)
        answers = np.array(answers_list).reshape(self.output_nodes, 1)
        hidden_guess = tanh(np.matmul(self.weights_ih, inputs) + self.bias_h)
        output_guess = tanh(np.matmul(self.weights_ho, hidden_guess) + self.bias_o)

        #calculate the errors: Error = Answer - Guess
        output_errors = answers - output_guess
        hidden_errors =  np.matmul(self.weights_ho.T, output_errors)

        output_gradient = self.learning_rate * output_errors * dtanh(output_guess)
        weights_ho_delta = np.matmul(output_gradient, hidden_guess.transpose())
        self.weights_ho += weights_ho_delta
        self.bias_o += output_gradient

        hidden_gradient = self.learning_rate * hidden_errors * dtanh(hidden_guess)
        weights_ih_delta = np.matmul(hidden_gradient, inputs.transpose())
        self.weights_ih += weights_ih_delta
        self.bias_h += hidden_gradient

    def feedforward_relu(self, input_array):
        #LOTS OF MATRIX MATH!
        inputs = np.array(input_array).reshape(self.input_nodes, 1)

        hidden_guess = leaky_relu(np.matmul(self.weights_ih, inputs) + self.bias_h)
        output_guess = leaky_relu(np.matmul(self.weights_ho, hidden_guess) + self.bias_o)

        return output_guess

    def train_relu(self, inputs_list, answers_list):
        inputs = np.array(inputs_list).reshape(self.input_nodes, 1)
        answers = np.array(answers_list).reshape(self.output_nodes, 1)
        hidden_guess = leaky_relu(np.matmul(self.weights_ih, inputs) + self.bias_h)
        output_guess = leaky_relu(np.matmul(self.weights_ho, hidden_guess) + self.bias_o)

        #calculate the errors: Error = Answer - Guess
        output_errors = answers - output_guess
        hidden_errors =  np.matmul(self.weights_ho.T, output_errors)

        output_gradient = self.learning_rate * output_errors * d_leaky_relu(output_guess)
        weights_ho_delta = np.matmul(output_gradient, hidden_guess.transpose())
        self.weights_ho += weights_ho_delta
        self.bias_o += output_gradient

        hidden_gradient = self.learning_rate * hidden_errors * d_leaky_relu(hidden_guess)
        weights_ih_delta = np.matmul(hidden_gradient, inputs.transpose())
        self.weights_ih += weights_ih_delta
        self.bias_h += hidden_gradient


    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate

def main():
    nn = NeuralNetwork(2, 4, 1)

    training_data = [
            ([1,0],[1]),
            ([0,1],[1]),
            ([1,1],[0]),
            ([0,0],[0])]
    for i in range(100):
        print(i)
        random.shuffle(training_data)
        for datum in training_data:
            nn.train(datum[0], datum[1])

    testing_data = [
            ([1,0],[1]),
            ([0,1],[1]),
            ([1,1],[0]),
            ([0,0],[0])]
    print("I trained my neural network with 20,000 inputs of the XOR logic space.")
    print("The NN has 2 inputs, 4 hidden layers, and 1 output.")
    print("Now I am feeding forward the logic space, to test whether the NN is successful.")
    for datum in testing_data:
        print(f"Data point {datum[0]} yields a value of {nn.feedforward(datum[0])} where the correct value was {datum[1]}.")
