import pygame


# For every frame we will add GRAVITY to BIRD_MOVEMENT
# Bird movement being movement downwards of the bird rect

GRAVITY = 0.5
BIRD_MOVEMENT = 0

GAME_ACTIVE = True


### DISPLAY SURFACE
# Screen properties
WIDTH, HEIGHT = 512, 1024
SIZE = (WIDTH, HEIGHT)

# Set screen (display surface) with given properties
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Frame rate
FPS = 60
