import pygame
import random
from display_surface import screen, SIZE, HEIGHT, WIDTH

DISPLAY_SURFACE = screen
DISPLAY_SURFACE_WIDTH = WIDTH
DISPLAY_SURFACE_HEIGHT = HEIGHT


def get_display_surface():
    return DISPLAY_SURFACE


def get_display_surface_width():
    return DISPLAY_SURFACE_WIDTH


def get_display_surface_height():
    return DISPLAY_SURFACE_HEIGHT


class CustomSurface(pygame.Surface):
    def __init__(self, directory: str, scale_surface: bool = False, *args, **kwargs):
        self.surface = pygame.image.load(directory).convert()
        self.directory = directory
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.display_surface = get_display_surface()
        self.size = (self.width, self.height)
        self.x_position = 0
        self.y_position = 0
        if scale_surface:
            self.surface = pygame.transform.scale2x(self.surface)
        super().__init__(size=self.size, *args, **kwargs)

    def change_position(self, x_change=0, y_change=0):
        self.x_position += x_change
        self.y_position += y_change

    def draw_surface(self, x_position=None, y_position=None):
        if not x_position:
            x_position = self.x_position
        if not y_position:
            y_position = self.y_position
        self.display_surface.blit(self.surface, (x_position, y_position))


class FloorSurface(CustomSurface):
    def draw_floor(self):
        """
        Takes a surface (with a given image on the surface) and draws it to the display surface.
        """
        self.display_surface.blit(self.surface, (self.x_position, self.y_position))
        self.display_surface.blit(self.surface, (self.x_position + self.width, self.y_position))


class BackgroundSurface(CustomSurface):
    def draw_background(self):
        """
        Takes a surface (with a given image on the surface) and draws it to the display surface.
        """
        self.display_surface.blit(self.surface, (self.x_position, self.y_position))


class BirdSurface(CustomSurface):
    BIRD_GAP = 100

    def __init__(self, directory: str, *args, **kwargs):
        super().__init__(directory, *args, **kwargs)
        BirdSurface.BIRD_GAP += self.surface.get_height()

    def draw_bird(self, rect):
        """
        Takes a surface (with a given image on the surface) and draws it to the display surface.
        """
        self.display_surface.blit(self.surface, rect)


class PipeSurface(CustomSurface):
    # List of pipes' rects
    PIPE_RECTS_LIST = []

    def create_bottom_pipe_rect(self, x_position=None):
        # X-axis default starting position
        if not x_position:
            x_position = WIDTH+self.width

        if self.surface.get_height() > HEIGHT:
            bottom_pipe_min_midtop = BirdSurface.BIRD_GAP
        else:
            bottom_pipe_min_midtop = HEIGHT - self.surface.get_height()

        bottom_pipe_max_midtop = HEIGHT
        random_midtop_point = random.randrange(bottom_pipe_min_midtop, bottom_pipe_max_midtop)
        bottom_pipe_rect = self.surface.get_rect(midtop=(x_position, random_midtop_point))
        return bottom_pipe_rect

    def create_top_pipe_rect(self, bottom_pipe_rect):
        flip_pipe_surface = pygame.transform.flip(self.surface, False, True)
        x_position = bottom_pipe_rect.midtop[0]
        y_position = HEIGHT - bottom_pipe_rect.midtop[1] - BirdSurface.BIRD_GAP
        top_pipe_rect = flip_pipe_surface.get_rect(midbottom=(x_position, y_position))
        return top_pipe_rect

    def add_pipe_to_pipes_rects_list(self, pipe):
        self.PIPE_RECTS_LIST.append(pipe)

    def move_pipes(self):
        pipes = self.PIPE_RECTS_LIST
        # print(pipes)
        for pipe_rect in pipes:
            pipe_rect.centerx -= 5  # pipe's speed in x axis
        self.PIPE_RECTS_LIST = pipes
        # return self.PIPE_RECTS_LIST

    def draw_pipes(self):
        """
        Takes a surface (with a given image on the surface) and draws it to the display surface.
        """
        for pipe_rect in self.PIPE_RECTS_LIST:
            self.display_surface.blit(self.surface, pipe_rect)
