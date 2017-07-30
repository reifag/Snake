import numpy as np
import pygame

import variables
from snake_game import create_food, eat_food, get_velocity, move_snake
from snake_learn import Creature, prepare_data


def play(frame_threshold, creature, draw=False, fps_clock=None, colors=None, display_surface=None):
    # initializes the constants
    movements = variables.movements
    constants = variables.game_constants
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
        prediction = creature.feed_forward(board_vector)
        # Gets the corresponding key for prediction
        key = movements[np.argmax(prediction)]
        # Sets the velocity to the new velocity
        creature.vel = get_velocity(key, constants['box'])
        if draw:
            # called so that the os doesn't think the game crashed
            pygame.event.pump()

            # draws the game
            food = eat_food(creature, snake, food, constants, colors=colors, display_surface=display_surface)
            dead = bool(move_snake(creature, snake, food, constants, colors=colors, display_surface=display_surface))
            pygame.display.update()
            fps_clock.tick(constants['fps'])
        else:
            # eats the food and creates new food if possible
            food = eat_food(creature, snake, food, constants)
            # Moves the snake and applies the speed change
            dead = bool(move_snake(creature, snake, food, constants))
    else:
        # In case the for loop doesn't terminate prematurely
        creature.frames = frame_threshold
        return creature.score


def main():
    draw = True

    constants = variables.game_constants
    generation = []
    if draw:
        colors = variables.colors

        pygame.init()

        display_surface = pygame.display.set_mode(constants['res'])
        display_surface.fill(colors['BG'])
        pygame.display.set_caption('Snake Game')
        fps_clock = pygame.time.Clock()

        for i in range(50):
            # initialized the snake to be at the middle of the board
            generation.append(play(50, Creature(), draw=True, fps_clock=fps_clock,
                                   colors=colors, display_surface=display_surface))
    else:
        for i in range(50):
            # initialized the snake to be at the middle of the board
            generation.append(play(50, Creature()))


if __name__ == '__main__':
    main()
