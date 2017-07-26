import pygame, sys
from pygame.locals import *
from random import randint, seed


# Create a new random function takes n
def rand(n):
    result = randint(0, int(n))
    print('Rand function called result: ', result)
    return result


def get_velocity(key, box):
    # Using a dictionary as a switch statement
    movements = {K_LEFT: (-box, 0), K_UP: (0, -box),
                 K_RIGHT: (box, 0), K_DOWN: (0, box)}
    # Assigns the velocity and returns the velocity
    return movements[key]


def draw(snake, food, DISPLAYSURF, constants, colors):
    box = constants['box']
    # Draws the snake by draw every link in the snake body as a color['snake'] rectangle
    for link in snake[:-1]:
        pygame.draw.rect(DISPLAYSURF, colors['snake'], (link[0], link[1], box, box))
    # Draws the head using a separate color
    pygame.draw.rect(DISPLAYSURF, colors['head'], (snake[-1][0], snake[-1][1], box, box))
    # Draws the food as a rectangle with color['food']
    pygame.draw.rect(DISPLAYSURF, colors['food'], (food[0], food[1], box, box))


def move_snake(snake, DISPLAYSURF, food, constants, colors):
    """moves by removing the 0th position from the list
       and then fills display surface with the background color
       then applies the velocity"""
    vel, head = constants['vel'], snake[-1]
    if death(snake):
        print("DEATH")
        DISPLAYSURF.fill(colors['head'])

    if constants['len'] == len(snake):
        snake.pop(0)
    # Redraws the display surface to hide the previous snake
    DISPLAYSURF.fill(colors['BG'])
    # Takes the position of the head (last index in the list)
    # And adds the velocity to get the new head position
    snake.append((head[0] + vel[0], head[1] + vel[1]))
    out_screen_check(snake, constants)
    draw(snake, food, DISPLAYSURF, constants, colors)


def out_screen_check(snake, constants):
    res, box = constants['res'], constants['box']
    head = list(snake[-1])
    for i in range(len(head)):
        head[i] = head[i] % res[i]

    # print('Out of screen: ', head, 'Snake: ', snake)
    snake.pop()
    snake.append(tuple(head))
    return snake


def create_food(constants):
    res, box = constants['res'], constants['box']
    food = [rand(res[0]) // box * box, rand(res[0]) // box * box]
    print('Create food: ', food)
    return tuple(food)


def death(snake):
    if snake.count(snake[-1]) == len(snake):
        return False

    if snake[-1] in snake[:-1]:
        return True
    return False


def eat_food(snake, food, DISPLAYSURF, constants, colors):
    head = snake[-1]

    # if food[0] == head[0] and food[1] == head[1]:
    if head == food:
        del food
        constants['len'] += 1
        food = create_food(constants)
        draw(snake, food, DISPLAYSURF, constants, colors)
    return food


def main():
    colors = {"snake": (  0, 255,   0),
              "head" : (255, 255, 255),
              "food" : (255,   0,   0),
              "BG"   : ( 51,  51,  51)}

    constants = {'fps': 15,
                 'res': (640, 640),
                 'box': 20,
                 'len': 4,
                 'vel': (0, 0)}
    seed(10)
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(constants['res'])
    DISPLAYSURF.fill(colors['BG'])
    pygame.display.set_caption('Snake Game')
    # initialized the snake to be at the middle of the board
    snake = [(16 * constants['box'], 16 * constants['box'])]

    food = create_food(constants)

    draw(snake, food, DISPLAYSURF, constants, colors)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                    # Updates the velocity to the current key press
                    constants['vel'] = get_velocity(event.key, constants['box'])

        food = eat_food(snake, food, DISPLAYSURF, constants, colors)
        # Moves the snake and applies the speed change
        move_snake(snake, DISPLAYSURF, food, constants, colors)
        # updates the display surface and performs one tick of the clock
        pygame.display.update()
        FPSCLOCK.tick(constants['fps'])


if __name__ == '__main__':
    main()
