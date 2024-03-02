from elements.sprites import sprites

class Player:
    def __init__(self, position):
        self.position = position
        self.lastPosition = position
        self.has_key = False

    def move(self, newPosition):
        self.lastPosition = self.position
        self.position = newPosition

    def draw(self, screen):
        sprite = sprites.get("PLAYER")
        screen.blit(sprite, (self.position.line * 25, self.position.col * 25))

    def pick_up_key(self):
        self.has_key = True

    def __str__(self):
        return (f"Player Position: {self.position}"
                f"Player Last Position: {self.lastPosition}")
