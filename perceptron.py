import random
import matplotlib.pyplot as plt

a, b = -0.5, 0.3

def f(x):
    return a*x + b

class Perceptron:
    def __init__(self):
        self.weights = list()
        for i in range(3): #x, y, and bias
            self.weights.append(random.random() * random.choice ([-1, 1]))
        print(self.weights)
        self.learning_rate = 0.1

    def guess(self, inputs):
        sum = 0
        for i in range(len(self.weights)):
            sum += inputs[i] * self.weights[i]
        output = 1 if sum>0 else -1 if sum<0 else 0
        return output

    def train(self, inputs, target):
        guess = self.guess(inputs)
        error = target - guess

        #tune all the weights
        for i in range(len(self.weights)):
            self.weights[i] += error * inputs[i] * self.learning_rate


class Point:
    def __init__(self):
        self.bias = 1
        self.x, self.y = random.random() * random.choice ([-1, 1]), random.random() * random.choice ([-1, 1])
        if self.y > f(self.x):
            self.label = 1
        elif self.y < f(self.x):
            self.label = -1
        else:
            self.label = 0

def make_scatter_from_points(points):
    plots = {'1': ([], []), '-1': ([], []), '0': ([], [])}
    markers = {'1': 'o', '-1': 's', '0': '^'}
    colors = {'1': 'b', '-1': 'g', '0': 'r'}

    point_data = list()
    for point in points:
        print(f'([{point.x}, {point.y}], {str(point.label)}')
        point_data.append(([point.x, point.y], str(point.label)))

    #point_data = [ ([x, y], '-1'),
    #                ([x, y], '-1'),
    #                ([x, y], '-1'), ...    ]

    for cords, value in point_data:
        plots[value][0].append(cords[0])
        plots[value][1].append(cords[1])

    for value, (x, y) in plots.items():
        plt.scatter(x, y, color=colors[value], marker=markers[value], label=value, zorder=10)

    x1, y1 = [-1, 1], [f(-1), f(1)]
    plt.plot(x1, y1, marker='.')

    plt.legend(loc=0)
    #plt.axis([-1, 1, ])
    plt.title("Perceptron Training Data")
    plt.show()

def main():
    training_points = [ Point() for _ in range(30)]

    perp = Perceptron()
    for point in training_points:
        p_label = point.label
        inputs = [point.x, point.y, point.bias]
        perp.train(inputs, p_label)

    testing_points = [ Point() for _ in range(200)]
    for point in testing_points:
        point.label = perp.guess([point.x, point.y, point.bias])

    #make_scatter_from_points(training_points)
    make_scatter_from_points(testing_points)

main()
