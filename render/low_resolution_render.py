import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps


class MapRender:
    def __init__(self, level, FileName):
        self.level = level
        self.fileName = FileName

        # Define cell types
        self.FLOOR = "FLOOR"
        self.WATER = "WATER"
        self.WALL = "WALL"
        self.EMPTY = "EMPTY"
        self.TARGET = "TARGET"
        self.PLAYER = "PLAYER"
        self.GOLDEN_KEY = "GOLDEN_KEY"
        self.KEY_HOLE = "KEY_HOLE"
        self.ICE = "ICE"
        self.TREASURE = "TREASURE"

        # Define colors for each cell type
        self.colors = {
            self.FLOOR: 'royalblue',
            self.WATER: 'cyan',
            self.WALL: 'black',
            self.EMPTY: 'white',
            self.TARGET: 'brown',
            self.PLAYER: 'red',
            self.GOLDEN_KEY: 'gold',
            self.KEY_HOLE: 'orange',
            self.ICE: 'lightblue',
            self.TREASURE: 'tan'
        }

    def plot_maze(self):
        num_columns = self.level.width
        num_rows = self.level.height

        fig, ax = plt.subplots()

        for cell in self.level.cells:
            color = self.colors.get(cell.cell_type)
            rect = plt.Rectangle((cell.position.line, cell.position.col), 1, 1, facecolor=color)
            ax.add_patch(rect)

        color_player = self.colors.get(self.PLAYER)
        rect = plt.Rectangle((self.level.player_cell.position.line, self.level.player_cell.position.col), 1, 1,
                             facecolor=color_player)
        ax.add_patch(rect)

        treasure_position = self.level.find_element_position(self.TREASURE)
        key_position = self.level.find_element_position(self.GOLDEN_KEY)
        keyhole_position = self.level.find_element_position(self.KEY_HOLE)

        if treasure_position is not None:
            rect = plt.Rectangle((treasure_position.line, treasure_position.col), 1, 1,
                                 facecolor=self.colors.get(self.TREASURE))
            ax.add_patch(rect)

        if key_position is not None:
            rect = plt.Rectangle((key_position.line, key_position.col), 1, 1,
                                 facecolor=self.colors.get(self.GOLDEN_KEY))
            ax.add_patch(rect)
        if keyhole_position is not None:
            rect = plt.Rectangle((keyhole_position.line, keyhole_position.col), 1, 1,
                                 facecolor=self.colors.get(self.KEY_HOLE))
            ax.add_patch(rect)

        ax.set_xlim(0, num_columns)
        ax.set_ylim(0, num_rows)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xticks(np.arange(0, num_columns, 1))
        ax.set_yticks(np.arange(0, num_rows, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.axis('off')
        plt.savefig(self.fileName, bbox_inches='tight', pad_inches=0)

        '''
        image = Image.open(self.fileName)
        rotated_image = image.rotate(180)
        flipped_image = ImageOps.mirror(rotated_image)
        flipped_image.save(self.fileName)
        image.close()
        '''

        plt.close()