# coding=utf8

import os
import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"  # No real image drivers exist, set to dummy for testing
os.environ["SDL_AUDIODRIVER"] = "disk"  # No real audio drivers exist, set to disk for testing

pygame.init()
canvas = pygame.display.set_mode((711, 300))
canvas.fill(pygame.Color(247, 250, 252, 255))
pygame_end = True  # Set to True so that we don't get stuck in a loop during testing'
