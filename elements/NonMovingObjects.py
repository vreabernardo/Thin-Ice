from elements.sprites import sprites

class NonMovingObjects:
    def __init__(self, cells):
        self.cells = cells

    def draw(self, screen):
        for cell in self.cells:
            if cell.cell_type not in ["PLAYER", "FLOOR", "TARGET"]:
                sprite = sprites.get(cell.cell_type)
                screen.blit(sprite, (cell.position.line * 25, cell.position.col * 25))

    def colidesWith(self, position):
        for cell in self.cells:
            if cell.cell_type not in ["PLAYER", "FLOOR", "TARGET", "GOLDEN_KEY","TREASURE","ICE"]:
                if cell.position == position:
                    return True
        return False

    def __str__(self):
        positions_str = ", ".join(str(pos) for pos in self.cells)
        return f"NonMovingObjects Positions: [{positions_str}]"
