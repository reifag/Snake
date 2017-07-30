from copy import deepcopy

import numpy as np
import pygame

import variables
from snake_game import create_food, eat_food, get_velocity, move_snake
from snake_learn import Creature, feed_forward, prepare_data


def play(frame_threshold, creature, draw=False, fps_clock=None, colors=None, display_surface=None):
    # initializes the constants
    movements = variables.movements
    constants = variables.play_constants
    dead = False
    # initializes the snake in the middle of the screen
    snake = [(16 * constants['box'], 16 * constants['box'])]
    food = create_food(snake, constants)
    # plays the game without gui used for snake_learn.py
    for frame in range(frame_threshold):
        if dead:
            creature.frames = frame
            return creature.score

        # Creates the board vector from snake and food
        board_vector = prepare_data(snake, food)
        # Performs the prediction based on board
        prediction, weights = feed_forward(board_vector, creature.weights_1, creature.weights_2)
        # Gets the corresponding key for prediction
        key = movements[np.argmax(prediction)]
        # Sets the velocity to the new velocity
        creature.vel = get_velocity(key, constants['box'])
        if draw:
            # called so that the os doesn't think the game crashed
            pygame.event.pump()

            # draws the game
            food = eat_food(snake, food, constants, colors, display_surface, creature=creature)
            dead = bool(move_snake(snake, food, constants, colors, display_surface, creature=creature))
            pygame.display.update()
            fps_clock.tick(constants['fps'])
        else:
            # eats the food and creates new food if possible
            food = eat_food(snake, food, constants, creature=creature)
            # Moves the snake and applies the speed change
            dead = bool(move_snake(snake, food, constants, creature=creature))
    else:
        # In case the for loop doesn't terminate prematurely
        creature.frames = frame_threshold
        return creature.score


def main():
    draw = False
    constants = deepcopy(variables.play_constants)
    frames_threshold = 50
    generation = [Creature() for i in range(frames_threshold)]
    if draw:
        colors = variables.colors

        pygame.init()

        display_surface = pygame.display.set_mode(constants['res'])
        display_surface.fill(colors['BG'])
        pygame.display.set_caption('Snake Game')
        fps_clock = pygame.time.Clock()

        for creature in range(50):
            # initialized the snake to be at the middle of the board
            generation.append(
                    play(frame_threshold=50, creature=Creature(), draw=True, fps_clock=fps_clock, colors=colors,
                         display_surface=display_surface))
    else:
        for creature in generation:
            # initialized the snake to be at the middle of the board
            play(50, creature)
    print(generation)
    print(sorted(generation, reverse=True))


if __name__ == '__main__':
    main()
