from copy import deepcopy
from random import seed

import numpy as np
import pygame

import variables
from snake import create_food, eat_food, get_velocity, move_snake
from snake_learn import feed_forward, prepare_data


def play(frame_threshold, constants, weights='random', draw=False, fps_clock=None, colors=None, display_surface=None):
    # initializes the constants
    learn_constants, movements = variables.learn_constants, variables.movements

    # initializes the snake in the middle of the screen
    snake = [(16 * constants['box'], 16 * constants['box'])]
    food = create_food(snake, constants)
    # plays the game without gui used for snake_learn.py
    for frame in range(frame_threshold):
        # This might not work
        # if death(snake) or move_snake(snake, food, constants) == False:
        #     print("DEATH")
        #     return constants['len'], frame

        # Creates the board vector from snake and food
        board_vector = prepare_data(snake, food)
        # Performs the prediction based on board
        prediction, weights = feed_forward(board_vector, weights)
        # Gets the corresponding key for prediction
        key = movements[np.argmax(prediction)]
        # Sets the velocity to the new velocity
        constants['vel'] = get_velocity(key, constants['box'])

        if draw:
            # draws the game
            food = eat_food(snake, food, constants, colors, display_surface)
            move_snake(snake, food, constants, colors, display_surface)
            pygame.display.update()
            fps_clock.tick(constants['fps'])
        else:
            # eats the food and creates new food if possible
            food = eat_food(snake, food, constants)
            # Moves the snake and applies the speed change
            move_snake(snake, food, constants)


def main():
    constants = deepcopy(variables.play_constants)
    colors = variables.colors

    seed(10)
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surface = pygame.display.set_mode(constants['res'])
    display_surface.fill(colors['BG'])
    pygame.display.set_caption('Snake Game')
    # initialized the snake to be at the middle of the board
    play(frame_threshold=1000000, constants=constants, weights='random', draw=True,
         fps_clock=fps_clock, colors=colors, display_surface=display_surface)

    # snake = [(16 * constants['box'], 16 * constants['box'])]
    #
    # food = create_food(snake, constants)
    # draw(snake, food, constants, colors, display_surface)


if __name__ == '__main__':
    main()
