import pygame
from config import *


def create_text_surface_and_rect(text, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    return text_surface, text_rect


def initialize_text(current_level, total_number_of_tiles, total_destroid_tiles, solved_levels, points):
    texts = [
        f'level: {current_level}',
        f'{total_destroid_tiles}/{total_number_of_tiles}',
        f'solved: {solved_levels}',
        f'reset',
        f'points: {points}'
    ]

    # Font and Text
    font = pygame.font.Font(TEXTFONT, FONTSIZE)
    text_surfaces_and_rects = [create_text_surface_and_rect(text, font, BLUE) for text in texts]
    text_surfaces, text_rects = zip(*text_surfaces_and_rects)

    # Set text positions
    positions = [
        LEFT_TEXT_POSITION,
        CENTER_TEXT_POSITION,
        RIGHT_TEXT_POSITION,
        LEFT_BOTTOM_TEXT_POSITION,
        RIGHT_BOTTOM_TEXT_POSITION
    ]

    for rect, pos in zip(text_rects, positions):
        rect.center = pos

    return text_surfaces, text_rects
