from render.low_resolution_render import MapRender
import matplotlib.pyplot as plt


class Cell:
    def __init__(self, position, cell_type, pass_counter=0):
        self.position = position
        self.cell_type = cell_type
        self.pass_counter = pass_counter

    def __str__(self):
        return f"MazeCell {self.position} - Type: {self.cell_type}"

    def __repr__(self):
        return str(self)


class Maze:
    def __init__(self, width, height, cells, player_cell):
        self.width = width
        self.height = height
        self.cells = cells
        self.player_cell = player_cell

    def __str__(self):
        return f"Maze (Width: {self.width}, Height: {self.height}, Cells: {len(self.cells)})"

    def find_element_position(self, element_type):
        # Find the position of the first cell with the specified element type
        for cell in self.cells:
            if cell.cell_type == element_type:
                return cell.position
        return None

    def find_elements_positions(self, element_type):
        # Find positions of all cells with the specified element type
        elements = [cell.position for cell in self.cells if cell.cell_type == element_type]
        return elements

    def get_element_by_position(self, position):
        # Get the cell type at a specific position
        for cell in self.cells:
            if cell.position == position:
                return cell

    def kill_tile(self, position, to_floor=False, ice=False):
        # Destroy a tile at a specific position, optionally converting it to FLOOR
        for x, cell in enumerate(self.cells):
            if cell.position == position:
                if to_floor:
                    self.cells[x] = Cell(position, "FLOOR")
                elif ice:
                    self.cells[x] = Cell(position, "FLOOR")
                else:
                    self.cells[x] = Cell(position, "WATER")
                break

    def get_neighborhood(self, position):
        # Get the cell types of the neighborhood around a specific position
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        adjacent_cell_types = [self.get_element_by_position(position.add(direction)).cell_type for direction in
                               directions]

        return adjacent_cell_types


class Position:
    def __init__(self, col, line):
        self.col = col
        self.line = line

    def __str__(self):
        return f"Position(Col: {self.col}, Line: {self.line})"

    def add(self, direction):
        # Add a direction to the current position to get a new position
        return Position(self.col + direction[0], self.line + direction[1])

    def __eq__(self, other):
        # Check if two positions are equal
        return self.col == other.col and self.line == other.line


def char_to_cell_type(char):
    # Map characters to cell types
    cell_types = {
        'F': 'FLOOR',
        '0': 'EMPTY',
        'W': 'WALL',
        'P': 'PLAYER',
        'E': 'TARGET',
        'I': 'ICE',
        'K': 'GOLDEN_KEY',
        'B': 'MOVING_BLOCK_TILE',
        'T': 'MOVING_BLOCK',
        '%': 'ICE_AND_MOVING_BLOCK',
        '&': 'MOVING_BLOCK_TILE_AND_GOLDEN_KEY',
        '!': 'ICE_AND_GOLDEN_KEY',
        '1': 'TELEPORTER_1',
        '2': 'TELEPORTER_2',
        'H': 'KEY_HOLE',
        'M': 'TREASURE',
        '9': 'AFTERICE'
    }
    return cell_types.get(char, None)


def load_level(level_number):
    # Load level from a text file
    with open(f"data/maps/level{level_number}.txt", 'r') as file:
        lines = file.readlines()

    width = max(len(line.strip()) for line in lines)
    height = len(lines)

    cells = []
    player_cell = None

    for x, line in enumerate(lines):
        line = list(line.strip('\n'))
        for y, char in enumerate(line):
            cell_type = char_to_cell_type(char)
            if (cell_type is not None) and (cell_type != "PLAYER") and (cell_type != "GOLDEN_KEY") \
                    and (cell_type != "TREASURE"):
                cells.append(Cell(Position(x, y), cell_type))
            if cell_type == "PLAYER":
                player_cell = Cell(Position(x, y), cell_type)
                cells.append(Cell(Position(x, y), "FLOOR", 1))
            if cell_type == "GOLDEN_KEY":
                cells.append(Cell(Position(x, y), cell_type))
                cells.append(Cell(Position(x, y), "FLOOR", 1))
            if cell_type == "TREASURE":
                cells.append(Cell(Position(x, y), cell_type))
                cells.append(Cell(Position(x, y), "FLOOR", 1))
    return Maze(width=width, height=height, cells=cells, player_cell=player_cell)


if __name__ == "__main__":
    # Test
    level = load_level(10)
    MapRender(level, "./render/renderImages/lowRender.png").plot_maze()
