import numpy as np

import variables


def mutate(weights, learn_constants):
    # Sets the variance to variance in the learn constants
    variance = learn_constants['variance']
    # assigns the weights of each layer to a variable
    weights_1, weights_2 = weights

    low, high = (1 - variance, 1 + variance)
    mutation_1 = np.random.uniform(low, high, size=weights_1.shape)
    mutation_2 = np.random.uniform(low, high, size=weights_2.shape)
    # element wise multiplication of the weights and the mutation rate arrays
    weights_1 = np.multiply(weights_1, mutation_1)
    weights_2 = np.multiply(weights_2, mutation_2)

    return weights_1, weights_2


def prepare_data(snake, food):
    values = variables.board_values
    # Scales the coordinates for both the snake and food by 20 (box size)
    food = tuple([int(i / 20) for i in food])
    snake = [(int(link[0] / 20), int(link[1] / 20)) for link in snake]

    # Creates an 32x32 matrix of zeros
    board_matrix = np.zeros((32, 32))
    # Adds the values for the snake body
    for i, j in snake[:-1]:
        board_matrix[i, j] = values['body']
    # Add the value for the head
    board_matrix[snake[-1]] = values['head']
    # Add the value of the food
    board_matrix[food] = values['food']
    # Fill the values for the empty tiles
    for i in range(len(board_matrix)):
        for j in range(len(board_matrix)):
            if board_matrix[i, j] == 0:
                board_matrix[i, j] = values['else']
    # Turns the matrix into a column vector
    board_vector = board_matrix.flatten()
    return board_vector


def feed_forward(input_vector, weights='random'):
    # Creates random weights if no weight is given
    if weights == 'random':
        # Subtracts 0.5 to zero-center and make the values from -0.5 to 0.5
        weights_1 = np.random.rand(64, 1025) - 0.5
        weights_2 = np.random.rand(4, 65) - 0.5
    else:
        weights_1, weights_2 = weights[0], weights[1]

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
    np.set_printoptions(threshold=np.inf)
    learn_constants = variables.learn_constants
    snake = [(500, 160), (500, 180), (500, 200), (500, 220), (500, 240), (480, 240), (460, 240), (440, 240), (420, 240),
             (400, 240), (380, 240), (380, 220), (380, 200), (380, 180), (380, 160), (380, 140), (380, 120), (380, 100),
             (380, 80), (360, 80), (340, 80), (320, 80), (300, 80), (280, 80), (260, 80), (240, 80), (220, 80),
             (200, 80), (180, 80), (160, 80), (140, 80), (120, 80), (100, 80), (80, 80), (60, 80), (40, 80), (20, 80),
             (0, 80), (620, 80), (600, 80), (580, 80), (560, 80)]
    food = (440, 160)

    board_vector = prepare_data(snake, food)
    prediction, weights = feed_forward(board_vector)
    print(prediction)

    new_weights = mutate(weights, learn_constants)


if __name__ == '__main__':
    run()
