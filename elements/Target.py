from elements.sprites import sprites
class Target:
    def __init__(self, position):
        self.position = position

    def draw(self, screen):
        sprite = sprites.get("TARGET")
        screen.blit(sprite, (self.position.line * 25, self.position.col * 25))

    def __str__(self):
        return f"Target Position:{self.position}"