import pygame
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)

image_dir = os.path.join(parent_dir, "data", "images")

sprites = {
    "FLOOR": pygame.image.load(os.path.join(image_dir, 'free.png')),
    "EMPTY": pygame.image.load(os.path.join(image_dir, 'unused.png')),
    "WALL": pygame.image.load(os.path.join(image_dir, 'wall.png')),
    "PLAYER": pygame.image.load(os.path.join(image_dir, 'icon.png')),
    "TARGET": pygame.image.load(os.path.join(image_dir, 'finish.png')),
    "ICE": pygame.image.load(os.path.join(image_dir, 'ice.png')),
    "GOLDEN_KEY": pygame.image.load(os.path.join(image_dir, 'key.png')),
    "MOVING_BLOCK_TILE": pygame.image.load(os.path.join(image_dir, 'movingBlockTile.png')),
    "MOVING_BLOCK": pygame.image.load(os.path.join(image_dir, 'movingBlock.png')),
    "ICE_AND_MOVING_BLOCK": pygame.image.load(os.path.join(image_dir, 'movingBlock.png')),
    "MOVING_BLOCK_TILE_AND_GOLDEN_KEY": pygame.image.load(os.path.join(image_dir, 'movingBlockTile.png')),
    "ICE_AND_GOLDEN_KEY": pygame.image.load(os.path.join(image_dir, 'ice.png')),
    "TELEPORTER_1": pygame.image.load(os.path.join(image_dir, 'teleporter.png')),
    "TELEPORTER_2": pygame.image.load(os.path.join(image_dir, 'teleporter.png')),
    "KEY_HOLE": pygame.image.load(os.path.join(image_dir, 'socket.png')),
    "TREASURE": pygame.image.load(os.path.join(image_dir, 'treasure.png')),
    "WATER": pygame.image.load(os.path.join(image_dir, 'water.png'))
}

