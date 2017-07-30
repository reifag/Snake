import sys

import pygame
from numpy.random import randint as rand
from pygame.locals import KEYUP, K_DOWN, K_LEFT, K_RIGHT, K_UP, QUIT

import variables
from snake_learn import Creature


def get_velocity(key, box):
    # Using a dictionary as a switch statement
    movements = {K_LEFT: (-box, 0), K_UP: (0, -box), K_RIGHT: (box, 0), K_DOWN: (0, box)}
    # Assigns the velocity and returns the velocity
    return movements[key]


def draw(snake, food, constants, colors, display_surface):
    box = constants['box']
    # Draws the snake by draw every link in the snake body as a color['snake'] rectangle
    for link in snake[:-1]:
        pygame.draw.rect(display_surface, colors['snake'], (link[0], link[1], box, box))
    # Draws the head using a separate color
    pygame.draw.rect(display_surface, colors['head'], (snake[-1][0], snake[-1][1], box, box))
    # Draws the food as a rectangle with color['food']
    pygame.draw.rect(display_surface, colors['food'], (food[0], food[1], box, box))


def move_snake(creature, snake, food, constants, colors=None, display_surface=None):
    """moves by removing the 0th position from the list
       and then fills display surface with the background color
       then applies the velocity"""
    head = snake[-1]
    if death(snake):
        return True
    # if length constant is greater than snake list length don't pop tail
    if creature.len == len(snake):
        snake.pop(0)
    # Takes the position of the head (last index in the list)
    # And adds the velocity to get the new head position
    snake.append((head[0] + creature.vel[0], head[1] + creature.vel[1]))
    out_screen_check(snake, constants)
    # Redraws the display surface to hide the previous snake
    if display_surface is not None:
        display_surface.fill(colors['BG'])
        draw(snake, food, constants, colors, display_surface)


def out_screen_check(snake, constants):
    res, box = constants['res'], constants['box']
    head = list(snake[-1])
    for i in range(len(head)):
        head[i] = head[i] % res[i]

    snake.pop()
    snake.append(tuple(head))
    return snake


def create_food(snake, constants):
    res, box = constants['res'], constants['box']
    food = [rand(res[0]) // box * box, rand(res[0]) // box * box]
    # Prevents the food from spawning inside the snake's body
    while food in snake:
        food = [rand(res[0]) // box * box, rand(res[0]) // box * box]
    return tuple(food)


def death(snake):
    if snake.count(snake[-1]) == len(snake):
        return False
    # Checks to see if the head intersects the body
    if snake[-1] in snake[:-1]:
        return True
    return False


def eat_food(creature, snake, food, constants, colors=None, display_surface=None):
    if snake[-1] == food:
        creature.len += 1
        food = create_food(snake, constants)
        # checks if the snake needs to be drawn
        if display_surface is not None:
            draw(snake, food, constants, colors, display_surface)
    return food


def main():
    # acquires the constants required to play the game
    colors, constants = variables.colors, variables.game_constants
    creature = Creature()
    # Initializes the game
    pygame.init()
    # Initializes the game clock
    fps_clock = pygame.time.Clock()
    display_surface = pygame.display.set_mode(constants['res'])
    display_surface.fill(colors['BG'])
    pygame.display.set_caption('Snake Game')
    # initialized the snake to be at the middle of the board
    snake = [(16 * constants['box'], 16 * constants['box'])]
    # Creates the initial food position and draws the game
    food = create_food(snake, constants)
    draw(snake, food, constants, colors, display_surface)
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                    # Updates the velocity to the current key press
                    creature.vel = get_velocity(event.key, constants['box'])

        food = eat_food(creature, snake, food, constants, colors=colors, display_surface=display_surface)
        # Moves the snake and applies the speed change
        move_snake(creature, snake, food, constants, colors=colors, display_surface=display_surface)
        # updates the display surface and performs one tick of the clock
        pygame.display.update()
        fps_clock.tick(constants['fps'])


if __name__ == '__main__':
    main()
