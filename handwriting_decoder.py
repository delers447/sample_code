#http://yann.lecun.com/exdb/mnist/

from nn import NeuralNetwork

import numpy as np
from mnist import MNIST
import random, math
from matplotlib import pyplot as plt
import xlwt
import struct
import time

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

loc_training_images = 'train-images.idx3-ubyte'
loc_training_labels = 'train-labels.idx1-ubyte'
loc_testing_images = 't10k-images.idx3-ubyte'
loc_testing_labels = 't10k-labels.idx1-ubyte'

labels_dict = {0: np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            1: np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
            2: np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
            3: np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
            4: np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
            5: np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
            6: np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
            7: np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
            8: np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
            9: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])}

def read_idx(filename):
    with open(filename, 'rb') as f:
        zero, data_type, dims = struct.unpack('>HBB', f.read(4))
        shape = tuple(struct.unpack('>I', f.read(4))[0] for d in range(dims))
        return np.fromstring(f.read(), dtype=np.uint8).reshape(shape)

training_labels = read_idx(loc_training_labels)
training_images = read_idx(loc_training_images)
testing_labels = read_idx(loc_testing_labels)
testing_images = read_idx(loc_testing_images)

training_images = training_images.astype(float)
testing_images = testing_images.astype(float)

def test_data():
    index = random.randrange(0, len(training_labels))
    print(training_labels[index])
    plt.imshow(training_images[index])
    plt.show()

def run_network(learning_rate, hidden_nodes):
    brain = NeuralNetwork(784, hidden_nodes, 10)
    brain.set_learning_rate(learning_rate)
    counter = 0

    for image, label in zip(training_images, training_labels):
        counter += 1
        print(f"Backward propogating the {counter} image, which was a {label} with array: {labels_dict[label]}.")
        brain.train(image.ravel(), labels_dict[label])
        #if counter > 20_000: break
        #print(brain.weights_ho[2:3, 2:4])

    correct = 0
    for i in range(len(testing_images)):
        output = brain.feedforward(testing_images[i].ravel())
        output = output.ravel()
        #print(testing_images[i].ravel())
        print(output)
        print(f"The letter was thought to be {output.argmax()} by the Neural network, but was actually {testing_labels[i]}.")
        if output.argmax() == testing_labels[i]:
            correct += 1
            print("IT WAS CORRECT!")
    print(correct/len(testing_images))
    return correct/len(testing_images)

def graph_annealing():
    space = [ x for x in range(24000)]
    brain = NeuralNetwork(4, 4, 2)
    x = list()
    y = list()
    for value in space:
        x.append(value)
        y.append(learning_rate_annealing_expo_cyclic(brain, value))
    plt.plot(x, y)
    plt.show()

def find_analytics():
    learning_rates_list = [.1, .07, .05, .03, .01, .005, .001, .0005, .0001, .00005, .00001]
    hidden_nodes_list = [100, 200, 300, 400, 500, 600, 700, 900, 1000, 1200, 1400, 1600, 1800, 2000]

    #Document LR, hidden, time, accuracy

    book = xlwt.Workbook(encoding='utf-8')
    sheet1 = book.add_sheet('Sheet 1')

    sheet1.write(0, 0, 'Learning Rate')
    sheet1.write(0, 1, '#of Hidden Nodes')
    sheet1.write(0, 2, 'Time Taken')
    sheet1.write(0, 3, 'Accuracy')

    i = 1
    for rate in learning_rates_list:
        for hidden_number in hidden_nodes_list:
            #take start time and run network
            start = time.time()
            accuracy = run_network(rate, hidden_number) #def run_network(learning_rate, hidden_nodes):
            end = time.time()

            #document the items in the ith row of the worksheet
            sheet1.write(i, 0, rate)
            sheet1.write(i, 1, hidden_number)
            sheet1.write(i, 2, end-start)
            sheet1.write(i, 3, accuracy)

            i += 1

    book.save("NN_specs_analytics.xls")

def learning_rate_annealing_cyclic(brain, iteration):
    #learning rate annealing
    #sets the learning rate based on a trinangular schedule
    rate_min = 0.000_5
    rate_max = 0.001
    step_size = 500
    cycle = math.ceil((1.0 + iteration) / (2.0 * step_size))
    x = math.fabs((iteration/step_size) - 2.0 * cycle + 1.0)
    value = x if (x) > 0 else 0
    new_learning_rate = rate_min + (rate_max - rate_min) * value
    brain.set_learning_rate(new_learning_rate)
    return new_learning_rate

def learning_rate_annealing_expo_cyclic(brain, iteration):
    #learning rate annealing
    #sets the learning rate based on a trinangular schedule
    #but scaled for each cycle by 10%
    rate_min = 0.000_5
    rate_max = 0.001
    step_size = 500
    cycle = math.ceil((1.0 + iteration) / (2.0 * step_size))
    x = math.fabs((iteration/step_size) - 2.0 * cycle + 1.0)
    value = x if (x) > 0 else 0
    new_learning_rate = rate_min + (rate_max - rate_min) * value
    new_learning_rate *= (1-.1) ** math.ceil(iteration/1000)
    new_learning_rate += rate_min
    brain.set_learning_rate(new_learning_rate)
    return new_learning_rate

def learning_rate_annealing_expo(brain, iteration):
    #learning rate annealing
    #sets the learning rate based on exponential decay
    rate_min = 0.000_5
    step_size = 500

    cycle = math.ceil((1.0 + iteration) / (2.0 * step_size))
    new_learning_rate = brain.learning_rate * (1 / math.exp(math.ceil(iteration / step_size * 2))) + rate_min
    brain.set_learning_rate(new_learning_rate)
    return new_learning_rate

def normalize_images(images):
    #normalize image values to have zero mean and unit variance.
    #converts the [0,256] range into a standard range from [0, 3]
    stdev = np.std(np.arange(256))
    mean = np.mean(np.arange(256))
    print(f"Stedev type: {type(stdev)}")
    print(f"Stedev : {stdev}")
    print(f"mean type: {type(mean)}")
    print(f"Mean : {mean}")
    for i, image in enumerate(images):
        images[i] = (image - mean) / stdev
    return images

def main():
    brain = NeuralNetwork(784, 3000, 10)
    brain.set_learning_rate(.001)
    counter = 0

    training_images_norm = normalize_images(training_images)
    testing_images_norm = normalize_images(testing_images)

    for image, label in zip(training_images_norm, training_labels):
        counter += 1
        print(f"Backward propogating the {counter} image, which was a {label} with array: {labels_dict[label]}.")
        brain.train_tanh(image.ravel(), labels_dict[label])
        #learning_rate_annealing_cyclic(brain, counter) #brain, iteration
        #print(f"Learning Rate: {brain.learning_rate}")
        if counter >= 1000:
            break

    correct = 0
    for i in range(len(testing_images_norm)):
        output = brain.feedforward_tanh(testing_images_norm[i].ravel())
        output = output.ravel()
        #print(testing_images[i].ravel())
        print(output)
        print(f"The letter was thought to be {output.argmax()} by the Neural network, but was actually {testing_labels[i]}.")
        if output.argmax() == testing_labels[i]:
            correct += 1
            print("IT WAS CORRECT!")
    print(correct/i)

main()
