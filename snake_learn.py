import numpy as np

import variables


class Creature:
    # Sets the variance to variance in the learn constants
    variance = variables.learn_constants['variance']

    def __init__(self, *, weights_1=None, weights_2=None):
        self.len = 4
        self.vel = (0, 0)
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
        mutation_1 = np.random.uniform(low, high, size=self.weights_1.shape)
        mutation_2 = np.random.uniform(low, high, size=self.weights_2.shape)
        # element wise multiplication of the weights and the mutation rate arrays
        self.weights_1 = np.multiply(self.weights_1, mutation_1)
        self.weights_2 = np.multiply(self.weights_2, mutation_2)

    def feed_forward(self, input_vector):
        # adds a bias unit to the input vector
        a1 = np.r_[1, input_vector]
        # performs matrix multiplication
        z2 = a1.dot(self.weights_1.T)
        # applies the activation function and then adds a bias unit
        a2 = np.r_[1, ReLU(z2)]
        z3 = a2.dot(self.weights_2.T)
        # Applies the soft max activation function to the output
        prediction = self.soft_max(z3)
        return prediction

    @staticmethod
    def soft_max(array):
        array = np.exp(array)
        array = np.array([np.round(i / sum(array), 3) for i in array])
        return array

    @property
    def score(self):
        return self.len, self.frames

    # overloads the less than (<) operator for sorting
    def __lt__(self, other):
        if self.score < other.score:
            return True
        return False


@np.vectorize
def ReLU(n):
    return max(0, n)


def prepare_data(snake, food):
    values = variables.board_values
    box = variables.game_constants['box']
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
