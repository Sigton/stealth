from pygame.locals import *

# The control for each function

controls = {"WALK_LEFT": K_a,
            "WALK_RIGHT": K_d,
            "JUMP": K_w,
            "ACTION": K_SPACE,
            "CROUCH": K_LCTRL}

trans_dict = {192: 96,
              107: 270,
              109: 269,
              37: 276,
              39: 275,
              38: 273,
              40: 274,
              45: 277,
              36: 278,
              33: 280,
              46: 127,
              35: 279,
              34: 281}
