import time
import pygame
from settings import *
from sprites import *
import random
import time


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(400, 100)
        self.start_Start = False
        self.Start_time = 0
        self.previous_choice = ""
        self.choice = ""
        self.start_timer = False
        self.start_game = False
        self.elapsed_time = 0
        self.tiles = []
        self.high_score_easy = float(self.get_high_scores()[0])
        self.high_score_medium = float(self.get_high_scores()[1])
        self.high_score_hard = float(self.get_high_scores()[2])

    def get_high_scores(self):
        with open("high_scores.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_scores.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score_easy))
            file.write(str("%.3f\n" % self.high_score_medium))
            file.write(str("%.3f" % self.high_score_hard))

    def create_game(self, game_size):
        grid = [
            [x + y * game_size for x in range(1, game_size + 1)] for y in range(game_size)]
        grid[-1][-1] = 0
        return grid

    def Start(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove(
                "left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove(
                "right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove(
                "down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove(
                "up") if "up" in possible_moves else possible_moves

        self.choice = random.choice(possible_moves)
        self.previous_choice = self.choice
        if self.choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                self.tiles_grid[row][col]
        elif self.choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                self.tiles_grid[row][col]
        elif self.choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                self.tiles_grid[row][col]
        elif self.choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                self.tiles_grid[row][col]

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game(self.game_size)
        self.tiles_grid_completed = self.create_game(self.game_size)
        self.elapsed_time = 0
        self.moves = 0
        self.start_timer = False
        self.start_game = False
        self.draw_buttons()
        self.draw_tiles()

    def draw_timer(self, timer):
        UIElement(825, 35, timer).draw(self.screen, 40)

    def draw_high_score(self, score):
        UIElement(710, 380, score).draw(self.screen, 30)

    def draw_buttons(self):
        self.buttons_list = []
        self.buttons_list.append(
            Button(self, 775, 100, "Start", 200, 50))
        Button(self, 775, 450, "Auto solve", 200, 50)
        self.buttons_list.append(Button(self, 775, 170, "Reset", 200, 50))
        self.buttons_list.append(Button(self, 690, 240, "Easy", 100, 50))
        self.buttons_list.append(Button(self, 800, 240, "Medium", 150, 50))
        self.buttons_list.append(Button(self, 960, 240, "Hard", 100, 50))

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.game_choice == EASY:
                    if self.high_score_easy > 0:
                        self.high_score_easy = self.elapsed_time if self.elapsed_time < self.high_score_easy else self.high_score_easy
                    else:
                        self.high_score_easy = self.elapsed_time
                elif self.game_choice == MEDIUM:
                    if self.high_score_medium > 0:
                        self.high_score_medium = self.elapsed_time if self.elapsed_time < self.high_score_medium else self.high_score_medium
                    else:
                        self.high_score_medium = self.elapsed_time
                elif self.game_choice == HARD:
                    if self.high_score_hard > 0:
                        self.high_score_hard = self.elapsed_time if self.elapsed_time < self.high_score_hard else self.high_score_hard
                    else:
                        self.high_score_hard = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_Start:
            self.Start()
            self.draw_tiles()
            self.Start_time += 1
            if self.Start_time > 100:
                self.start_Start = False
                self.start_timer = True
                self.start_game = True

        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, self.game_choice, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0),
                             (row, self.game_choice))
        for col in range(-1, self.game_choice, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col),
                             (self.game_choice, col))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        if self.game_choice == EASY:
            UIElement(840, 320, "Easy").draw(self.screen, 30)
            self.draw_high_score(
                "High Score - %.3f" % (self.high_score_easy if self.high_score_easy > 0 else 0))
        elif self.game_choice == MEDIUM:
            UIElement(820, 320, "Medium").draw(self.screen, 30)
            self.draw_high_score(
                "High Score - %.3f" % (self.high_score_medium if self.high_score_medium > 0 else 0))
        elif self.game_choice == HARD:
            UIElement(840, 320, "Hard").draw(self.screen, 30)
            self.draw_high_score(
                "High Score - %.3f" % (self.high_score_hard if self.high_score_hard > 0 else 0))
        self.draw_timer("%.3f" % self.elapsed_time)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][
                                    col + 1], \
                                    self.tiles_grid[row][col]

                            elif tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][
                                    col - 1], \
                                    self.tiles_grid[row][col]

                            elif tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][
                                    col], \
                                    self.tiles_grid[row][col]

                            elif tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][
                                    col], \
                                    self.tiles_grid[row][col]
                            self.draw_tiles()
                            self.moves += 1

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Easy":
                            self.game_choice = EASY
                            self.game_size = 3
                            self.new()
                        elif button.text == "Medium":
                            self.game_choice = MEDIUM
                            self.game_size = 4
                            self.new()
                        elif button.text == "Hard":
                            self.game_choice = HARD
                            self.game_size = 5
                            self.new()
                        if button.text == "Start":
                            self.Start_time = 0
                            self.start_Start = True
                        if button.text == "Reset":
                            self.new()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start_Start = not self.start_Start

    def show_start_screen(self):
        self.game_choice = EASY
        self.game_size = 3

    def show_go_screen(self):
        pass


game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
    game.show_go_screen()
