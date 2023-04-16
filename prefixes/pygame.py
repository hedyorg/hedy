# coding=utf8

import pygame  # noqa F401
import buttons  # noqa F401

pygame.init()
canvas = pygame.display.set_mode((711, 300))
canvas.fill(pygame.Color(247, 250, 252, 255))

pygame_end = False
button_list = []


def create_button(name):
    if name not in button_list:
        button_list.append(name)
        buttons.add(name)
