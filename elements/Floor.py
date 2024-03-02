from elements.sprites import sprites

class Floor:
    def __init__(self, cells):
        self.deadFloors = []
        self.positions = cells

    def draw(self, screen, positions):
        for position in positions:
                sprite = sprites.get("FLOOR")
                screen.blit(sprite, (position.line * 25, position.col * 25))

    def colidesWith(self, position):
        for floorPosition in self.positions:
            if position == floorPosition:
                self.deadFloors.append(floorPosition)
                return True
        return False



    def __str__(self):
        positions_str = ", ".join(str(pos) for pos in self.positions)
        return f"Floor Positions: [{positions_str}]"