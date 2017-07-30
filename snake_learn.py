from copy import deepcopy

import numpy as np

import variables


class Creature:
    # Sets the variance to variance in the learn constants
    variance = variables.learn_constants['variance']
    constants = variables.play_constants

    def __init__(self, *, weights_1=None, weights_2=None):
        self.len = deepcopy(__class__.constants['len'])
        self.vel = deepcopy(__class__.constants['vel'])

        self.frames = None
        # Checks to see if weights are given
        if weights_1 and weights_2:
            self.weights_1 = weights_1
            self.weights_2 = weights_2
        else:
            self.create_weights()

    def create_weights(self):
        # Subtracts 0.5 to zero-center and make the values from -0.5 to 0.5
        self.weights_1 = np.random.rand(64, 1025) - 0.5
        self.weights_2 = np.random.rand(4, 65) - 0.5

    def mutate(self):
        # assigns the weights of each layer to a variable
        low, high = (1 - __class__.variance, 1 + __class__.variance)
        self.mutation_1 = np.random.uniform(low, high, size=self.weights_1.shape)
        self.mutation_2 = np.random.uniform(low, high, size=self.weights_2.shape)
        # element wise multiplication of the weights and the mutation rate arrays
        self.weights_1 = np.multiply(self.weights_1, self.mutation_1)
        self.weights_2 = np.multiply(self.weights_2, self.mutation_2)

    @property
    def score(self):
        return self.len, self.frames

    # overloads the less than (<) operator for sorting
    def __lt__(self, other):
        if self.score < other.score:
            return True
        return False


def prepare_data(snake, food):
    # Todo maybe move into Snake Class
    values = variables.board_values
    box = variables.play_constants['box']
    # Scales the coordinates for both the snake and food by 20 (box size)
    food = (int(food[0] / box), int(food[1] / box))
    snake = [(int(link[0] / box), int(link[1] / box)) for link in snake]

    # Creates an 32x32 matrix containing the value of 'else'
    board_matrix = np.ones((32, 32)) * values['else']
    # Adds the values for the snake body
    for i, j in snake[:-1]:
        board_matrix[i, j] = values['body']
    # Add the value for the head
    board_matrix[snake[-1]] = values['head']
    # Add the value of the food
    board_matrix[food] = values['food']
    # Turns the matrix into a column vector
    board_vector = board_matrix.flatten()
    return board_vector


def feed_forward(input_vector, weights_1, weights_2):
    # TODO maybe move into Snake Class
    # makes ReLU work element wise on np array
    activation = np.vectorize(ReLU)

    # Feed forward part of the neural network
    # adds a bias unit to the input vector
    a1 = np.r_[1, input_vector]
    # performs matrix multiplication
    z2 = a1.dot(weights_1.T)
    # applies the activation function and then adds a bias unit
    a2 = np.r_[1, activation(z2)]
    z3 = a2.dot(weights_2.T)
    # Applies the soft max activation function to the output
    prediction = soft_max(z3)
    return prediction, (weights_1, weights_2)


def soft_max(array):
    array = np.exp(array)
    array = np.array([np.round(i / sum(array), 3) for i in array])
    return array


def ReLU(n):
    return max(0, n)


def run():
    # TODO make sure this is No longer needed before removing
    np.set_printoptions(threshold=np.inf)
    learn_constants = variables.learn_constants
    snake = [(500, 160), (500, 180), (500, 200), (500, 220), (500, 240), (480, 240), (460, 240), (440, 240), (420, 240),
             (400, 240), (380, 240), (380, 220), (380, 200), (380, 180), (380, 160), (380, 140), (380, 120), (380, 100),
             (380, 80), (360, 80), (340, 80), (320, 80), (300, 80), (280, 80), (260, 80), (240, 80), (220, 80),
             (200, 80), (180, 80), (160, 80), (140, 80), (120, 80), (100, 80), (80, 80), (60, 80), (40, 80), (20, 80),
             (0, 80), (620, 80), (600, 80), (580, 80), (560, 80)]
    food = (620, 260)

    # board_vector = prepare_data(snake, food)
    # prediction, weights = feed_forward(board_vector)
    # new_weights = mutate(weights, learn_constants)
    # print(weights)
    # print('\n\n\n', new_weights)


if __name__ == '__main__':
    run()