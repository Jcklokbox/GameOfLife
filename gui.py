import pygame
import pygame_widgets
from pygame_widgets.slider import Slider

from gameoflife import GameOfLife


class GUI:
    def __init__(self, width, height, cell_size=20, gui=True):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.window_size = (width * cell_size, height * cell_size)
        self.gui = gui
        self.grid = GameOfLife(width, height)
        if gui:
            pygame.init()
            self.screen = pygame.display.set_mode(self.window_size)
            pygame.display.set_caption("Game of Life")
            # Create slider if GUI is enabled
            self.slider = Slider(self.screen, 50, height * cell_size - 40,
                                 width * cell_size - 100, 20, min=1, max=60,
                                 handleColour=(255, 255, 255), initial=50)
            self.font = pygame.font.Font(None, 36)
            self.running = True
            self.frame_count = 0
            self.clock = pygame.time.Clock()

    def draw_cell(self, x, y, color):
        if self.gui:
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                               self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, color, rect)

    def draw_grid(self):
        if self.gui:
            for row in range(self.height):
                for col in range(self.width):
                    cell_value = self.grid.grid[row][col]
                    if cell_value == 1:
                        self.draw_cell(col, row,
                                       (255, 255, 255))  # White color
                    else:
                        self.draw_cell(col, row, (0, 0, 0))  # Black color

    def run_gui(self):
        self.grid.fill_random()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # Update slider
            self.slider.listen(pygame.event.get())
            speed = int(self.slider.getValue())  # Get value from slider

            self.frame_count += 1
            if self.frame_count % (61 - speed) == 0:
                self.grid.update()
                self.screen.fill((255, 255, 255))
                self.draw_grid()
                frame_num_text = self.font.render(f'{self.frame_count}',
                                                  True, (255, 255, 255))
                self.screen.blit(frame_num_text, (10, 10))

            # Draw slider
            self.slider.draw()

            pygame.display.flip()
            self.clock.tick(60)

            pygame_widgets.update(events)

        pygame.quit()

    def run_no_gui(self, num_iterations):
        self.grid.fill_random()
        for _ in range(num_iterations):
            self.grid.update()

    def run(self, num_iterations=None):
        if self.gui:
            self.run_gui()
        else:
            if num_iterations is None:
                raise ValueError("Please provide the number of "
                                 "iterations for the non-GUI mode.")
            self.run_no_gui(num_iterations)