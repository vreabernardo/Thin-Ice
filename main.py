from decodeMaps import *
from elements.Player import Player
from elements.Floor import Floor
from elements.Target import Target
from elements.NonMovingObjects import NonMovingObjects
from text_utilities.text_utility import *
from config import *
from render.low_resolution_render import MapRender
from enum import Enum


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_NAME)

DIRECTION_UP = (-1, 0)
DIRECTION_DOWN = (1, 0)
DIRECTION_LEFT = (0, -1)
DIRECTION_RIGHT = (0, 1)

class Game:
    def __init__(self, starting_level=1, animation=True):
        # Main loop
        self.running = True

        # Start Game
        self.reset(starting_level, animation=animation)

    def reset(self, currentLevel=1, solved=0, points=0, animation=True):
        self.currentLevel = currentLevel
        self.number_of_levels_solved = solved
        self.current_points = points
        self.game_iteration = 0

        # Load Level
        self.thinIce_level = load_level(currentLevel)

        # RENDER TYPE (true for true resolution, false for low resolution)
        self.animation_status = animation

        # Initialize the positions
        self.player = Player(self.thinIce_level.player_cell.position)
        self.floor = Floor(self.thinIce_level.find_element_position(FLOOR))
        self.target = Target(self.thinIce_level.find_element_position(TARGET))
        self.nonMovingObjects = NonMovingObjects(self.thinIce_level.cells)
        self.treasure_position = self.thinIce_level.find_element_position(TREASURE)
        self.key_position = self.thinIce_level.find_element_position(GOLDEN_KEY)
        self.keyhole_position = self.thinIce_level.find_element_position(KEY_HOLE)

        # The number of floor tiles
        padding_for_text = (NUM_COLUMNS * 2) - 1
        total_number_of_floor_tiles = len([cell for cell in self.thinIce_level.cells if cell.cell_type == FLOOR])
        self.total_number_of_tiles = total_number_of_floor_tiles - padding_for_text

        # Number of Floors converted to water
        self.number_of_tiles_killed = 0

        # Last Number of points
        self.last_points = points

        # Main loop
        self.running = True

    def _draw(self):
        if self.animation_status:
            self.floor.draw(screen, self.thinIce_level.find_elements_positions(FLOOR))
            self.target.draw(screen)
            self.nonMovingObjects.draw(screen)
            self.player.draw(screen)

        self._draw_text()

    def _draw_text(self):
        text_surfaces, text_rects = initialize_text(self.currentLevel,
                                                    self.total_number_of_tiles,
                                                    self.number_of_tiles_killed,
                                                    self.number_of_levels_solved,
                                                    self.current_points)

        # Blit texts on the screen
        for text, rect in zip(text_surfaces, text_rects):
            screen.blit(text, rect)

    def _handle_key_event(self, key: int):
        match key:
            case pygame.K_UP:
                self._move_player((-1, 0))
            case pygame.K_DOWN:
                self._move_player((1, 0))
            case pygame.K_LEFT:
                self._move_player((0, -1))
            case pygame.K_RIGHT:
                self._move_player((0, 1))
            case pygame.K_n if self.currentLevel < MAX_LEVEL:
                self._level_up()
            case pygame.K_b if self.currentLevel > 1:
                self._level_down()
            case pygame.K_r:
                self._reset_game()

    def _level_up(self):
        if self.currentLevel < MAX_LEVEL:
            self.reset(self.currentLevel + 1, self.number_of_levels_solved, self.current_points)

    def _level_down(self):
        if self.currentLevel > FIRST_LEVEL:
            self.reset(self.currentLevel - 1, self.number_of_levels_solved, self.current_points)

    def _reset_game(self):
        self.reset(self.currentLevel, self.number_of_levels_solved, self.last_points)

    def _check_last_tile(self):
        last_position = self.player.lastPosition
        current_position = self.player.position
        last_element = self.thinIce_level.get_element_by_position(last_position)

        if (
                last_position != current_position
                and last_element.cell_type == FLOOR
                and last_element.pass_counter >= 1
        ):
            self.thinIce_level.kill_tile(last_position)
            self.current_points += FLOOR_KILL_POINTS
            self.number_of_tiles_killed += 1

        elif last_position != current_position and last_element.cell_type == ICE:
            self.thinIce_level.kill_tile(last_position, to_floor=True)
            self.current_points += FLOOR_KILL_POINTS

    def _check_if_theres_an_item(self, neighborhood):
        # CHECK TARGET
        if self.player.position == self.target.position and self.currentLevel < MAX_LEVEL:
            if self.number_of_tiles_killed == self.total_number_of_tiles:
                self.current_points += LEVEL_UP_POINTS
                self.reset(self.currentLevel + 1, self.number_of_levels_solved + 1, self.current_points)
            else:
                self.reset(self.currentLevel + 1, self.number_of_levels_solved, self.current_points)

        # CHECK TREASURE
        if self.treasure_position is not None and self.player.position == self.treasure_position:
            self.thinIce_level.kill_tile(self.treasure_position)
            self.current_points += TREASURE_POINTS
            # POINTS GLITCH
            self.treasure_position = None

        # CHECK KEY
        if self.key_position is not None and self.player.position == self.key_position:
            self.thinIce_level.kill_tile(self.key_position)
            self.player.pick_up_key()

        # CHECK DOR NEAR
        if self.player.has_key and KEY_HOLE in neighborhood:
            self.thinIce_level.kill_tile(self.keyhole_position, to_floor=True)

    def _move_player(self, direction):
        future_position = self.player.position.add(direction)
        if not self.nonMovingObjects.colidesWith(future_position):
            target = self.thinIce_level.get_element_by_position(future_position)
            target.pass_counter += 1
            self.player.move(future_position)

    def _is_player_stuck(self, neighborhood):
        # if not any(element in neighborhood for element in ["FLOOR", "TARGET", "ICE", "TREASURE", "GOLDEN_KEY"]):
        #   self.reset(self.currentLevel, self.number_of_levels_solved, self.last_points)
        return not any(element in neighborhood for element in ["FLOOR", "TARGET", "ICE", "TREASURE", "GOLDEN_KEY"])

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    self._handle_key_event(event.key)

            # CHECK IF THE PLAYER IS TRAPPED
            neighborhood = self.thinIce_level.get_neighborhood(self.player.position)
            player_is_stuck = self._is_player_stuck(neighborhood)

            if player_is_stuck:
                self.reset(self.currentLevel, self.number_of_levels_solved, self.last_points)

            self._check_if_theres_an_item(neighborhood)
            self._check_last_tile()

            self._draw()

            # SAVE RENDER
            if not self.animation_status:
                MapRender(self.thinIce_level, f"./render/renderImages/frame{self.game_iteration}.png").plot_maze()

            # Update the display
            pygame.display.flip()

            # Clear the screen
            screen.fill(BACKGROUNDCOLOR)

        pygame.quit()


if __name__ == "__main__":
    game = Game(FIRST_LEVEL)
    game.run()
