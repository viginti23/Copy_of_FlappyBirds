import pygame
import sys
from surfaces import PipeSurface, BackgroundSurface, FloorSurface, BirdSurface
from display_surface import FPS, WIDTH, HEIGHT, SIZE, screen
from game_variables import gravity, bird_movement

pygame.init()

clock = pygame.time.Clock()

### SURFACES ###
# Setting background image surface
bg_surface = BackgroundSurface('FlappyBird_Python-master/assets/background-day.png', scale_surface=True)
bg_surface.change_position(0, 0)

# Setting floor image surface
floor_surface = FloorSurface('FlappyBird_Python-master/assets/base.png', scale_surface=True)
floor_surface.change_position(0, HEIGHT - floor_surface.height)


# SPAWNPIPE (USEREVENT) is a kind of a signal (as an event) that is being sent in order to initialize custom tasks
# Pygame has a total of 32 event slots (ID’s), of which the first 23 are used by Pygame (pre-defined events).
# Event ID’s from 24 to 32 are available for our use.
# The pygame.USEREVENT has a value of 24, which we can assign to our user-defined event.
# For creating a second event, you would do pygame.USEREVENT + 1 (for an ID of 25), and so on.

SPAWNPIPE = pygame.USEREVENT
# Timer are responsible for broadcasting our custom events
pygame.time.set_timer(SPAWNPIPE, 1200)

# Setting pipe image surface
pipe_surface = PipeSurface('FlappyBird_Python-master/assets/pipe-green.png', scale_surface=True)

# Setting bird image surface
bird_surface = BirdSurface('FlappyBird_Python-master/assets/bluebird-midflap.png', scale_surface=True)

# Bird rect controls bird_surface's position and movement
# bird_rect has a width and height of bird_surface and position of center of the rect is (100, WIDTH/2)
bird_rect = bird_surface.get_rect(center=(100, WIDTH / 2))

# Game event loop -> pygame.event
# Game loop checks for user input and handles the game logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pygame.QUIT being an event of clicking on X to close the window
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12
        if event.type == SPAWNPIPE:
            # Create a rect of a pipe_surface
            bottom_pipe_rect = pipe_surface.create_bottom_pipe_rect()
            top_pipe_rect = pipe_surface.create_top_pipe_rect(bottom_pipe_rect)

            pipe_surface.add_pipe_to_pipes_rects_list(bottom_pipe_rect)
            pipe_surface.add_pipe_to_pipes_rects_list(top_pipe_rect)

    # Render the bg_surface on the display surface at given coordinates
    bg_surface.draw_background()

    # Render pipe_surfaces
    pipe_surface.move_pipes()  # Gives the pipes speed (eg. pipe.centerx -= 5)
    pipe_surface.draw_pipes()  # Actually draws the pipes

    # Render the floor_surface on the display surface at given coordinates
    floor_surface.draw_floor()
    floor_surface.change_position(x_change=-1)

    if floor_surface.x_position == - floor_surface.width:
        floor_surface.x_position = 0

    # Bird movement -> speed
    # gravity -> acceleration
    # center y -> direction of the movement
    bird_movement += gravity
    bird_rect.centery += bird_movement

    # Render the bird_surface with the position of its bird_rect
    bird_surface.draw_bird(bird_rect)

    pygame.display.update()
    clock.tick(FPS)  # How many times per second the loop is executed
