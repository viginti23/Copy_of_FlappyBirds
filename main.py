import pygame
import sys
from surfaces import PipeSurface, BackgroundSurface, FloorSurface, BirdSurface
from game_settings import GRAVITY, BIRD_MOVEMENT, GAME_ACTIVE, FPS, WIDTH, HEIGHT

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
# Timer are responsible for broadcasting our custom events

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1400)

# Setting pipe image surface
pipe_surface = PipeSurface('FlappyBird_Python-master/assets/pipe-green.png', scale_surface=True)
flip_surface = PipeSurface('FlappyBird_Python-master/assets/pipe-green.png', scale_surface=True, flip_y=True,
                           flip_x=True)

# Setting bird image surface
bird_surface = BirdSurface('FlappyBird_Python-master/assets/bluebird-midflap.png', scale_surface=True)

# Bird rect controls bird_surface's position and movement
# bird_rect has a width and height of bird_surface and position of center of the rect is (100, WIDTH/2)
bird_rect_initial_pos = (100, WIDTH/2)
bird_rect = bird_surface.get_rect(center=bird_rect_initial_pos)
bird_surface.rect = bird_rect

# Game event loop -> pygame.event
# Game loop checks for user input and handles the game logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pygame.QUIT being an event of clicking on X to close the window
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and GAME_ACTIVE:
                BIRD_MOVEMENT = 0
                BIRD_MOVEMENT -= 7
            if event.key == pygame.K_SPACE and not GAME_ACTIVE:
                bird_rect.center = bird_rect_initial_pos
                BIRD_MOVEMENT = 0
                PipeSurface.PIPE_RECTS_LIST.clear()
                GAME_ACTIVE = True

        if event.type == SPAWNPIPE:
            # Create a rect of a pipe_surface
            pipe_rects = pipe_surface.create_top_and_bottom_rects()
            pipe_surface.add_pipe_to_pipes_rects_list(pipe_rects)

    # Render the bg_surface on the display surface at given coordinates
    bg_surface.draw_background()

    # Render pipe_surfaces
    pipe_surface.draw_pipes()  # Actually draws the pipes

    # Render the floor_surface on the display surface at given coordinates
    floor_surface.draw_floor()

    if GAME_ACTIVE:
        pipe_surface.move_pipes()  # Gives the pipes speed (eg. pipe.centerx -= 5)

        floor_surface.change_position(x_change=-4)
        if floor_surface.x_position <= - floor_surface.width:
            floor_surface.x_position = 0

        # Bird movement -> speed
        # GRAVITY -> acceleration
        # center y -> direction of the movement
        BIRD_MOVEMENT += GRAVITY
        bird_rect.centery += BIRD_MOVEMENT

        # Render the bird_surface with the position of its bird_rect
        bird_surface.draw_bird(bird_rect)

        GAME_ACTIVE = bird_surface.check_collisions(PipeSurface.PIPE_RECTS_LIST)

    pygame.display.update()
    clock.tick(FPS)  # How many times per second the loop is executed
