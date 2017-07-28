from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_UP

learn_constants = {'input_units' : 1024,
                   'hidden_units': 64,
                   'output_units': 4,
                   'creatures'   : 1000,
                   'variance'    : 0.10,
                   'frames'      : 10000}

colors = {"snake": (0, 255, 0),
          "head" : (0, 100, 0),
          "food" : (255, 0, 0),
          "BG"   : (51, 51, 51)}

play_constants = {'fps': 15,
                  'res': (640, 640),
                  'box': 20,
                  'len': 4,
                  'vel': (0, 0)}

board_values = {'head': 2,
                'body': -1,
                'food': 1,
                'else': 0}

movements = {0: K_LEFT,
             1: K_UP,
             2: K_RIGHT,
             3: K_DOWN}
