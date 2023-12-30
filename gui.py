import pygame
import os

class Gui():
    def __init__(self, dijkstra, a_star, depth_first, bi_bfs):
        pygame.init()
        self.dijkstra = dijkstra
        self.a_star = a_star
        self.depth_first = depth_first
        self.bi_bfs = bi_bfs

        self.FPS = 60
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.WIDTH = 600
        self.HEIGHT = 640
        self.CELL_SIZE = 40

        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        START_FLAG_IMAGE = pygame.image.load(os.path.join('Images', 'start_flag.png'))
        END_FLAG_IMAGE = pygame.image.load(os.path.join('Images', 'end_flag.png'))

        self.START_FLAG = pygame.transform.scale(START_FLAG_IMAGE, (self.CELL_SIZE - 1, self.CELL_SIZE - 1))
        self.END_FLAG = pygame.transform.scale(END_FLAG_IMAGE, (self.CELL_SIZE - 1, self.CELL_SIZE - 1))

        self.start = pygame.Rect(0, 40, self.CELL_SIZE - 1, self.CELL_SIZE - 1)
        self.end = pygame.Rect(self.WIDTH - self.CELL_SIZE, self.HEIGHT - self.CELL_SIZE , self.CELL_SIZE - 1, self.CELL_SIZE - 1)

        self.BUTTON_FONT = pygame.font.SysFont("comicsans", self.CELL_SIZE // 3 * 2)

        self.initialize_grid()

    def initialize_grid(self):
        self.generate_grid()
        self.generate_buttons()

        self.button_pressed = False
        self.flag_has_moved_cells = False
        self.initial_flag_collision = False
        self.initial_event = None

        clock = pygame.time.Clock()
        self.run = True
        while self.run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit() #here to avoid closing if "game" ends
                else:
                    self.event_manager(event)

            if self.run:
                self.draw_window()
    
    def generate_grid(self):
        self.cells_list = []
        # I use coordinate_to_rect in algorithms
        self.coordinates_to_rect = {}
        rows, cols = self.WIDTH//self.CELL_SIZE, self.HEIGHT//self.CELL_SIZE

        for x in range(rows):
            for y in range(1, cols):
                cell = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1)
                self.cells_list.append((cell, self.WHITE, False))
                self.coordinates_to_rect[(x * self.CELL_SIZE, y * self.CELL_SIZE)] = cell
        
        for cell, color, _ in self.cells_list:
            pygame.draw.rect(self.WIN, color, cell, self.CELL_SIZE - 1)

    def generate_buttons(self):
        self.star_button = pygame.Rect(0, 0, self.CELL_SIZE * 1, self.CELL_SIZE)
        self.dijkstra_button = pygame.Rect(40, 0, self.CELL_SIZE * 3, self.CELL_SIZE)
        self.depth_button = pygame.Rect(160, 0, self.CELL_SIZE * 4, self.CELL_SIZE)
        self.bi_bfs_button = pygame.Rect(300, 0, self.CELL_SIZE * 6, self.CELL_SIZE)
        #self.clear_button = pygame.Rect(360, 0, self.CELL_SIZE * 4, self.CELL_SIZE)
        #self.reset_path_button = pygame.Rect(360, 0, self.CELL_SIZE * 4, self.CELL_SIZE)

        pygame.draw.rect(self.WIN, self.WHITE, self.star_button, self.CELL_SIZE)
        pygame.draw.rect(self.WIN, self.WHITE, self.dijkstra_button, self.CELL_SIZE)
        pygame.draw.rect(self.WIN, self.WHITE, self.depth_button, self.CELL_SIZE)
        pygame.draw.rect(self.WIN, self.WHITE, self.bi_bfs_button, self.CELL_SIZE)

        star_text = self.BUTTON_FONT.render("A*", 1, (0, 0, 255))
        dijkstra_text = self.BUTTON_FONT.render("Dijkstra", 1, (0, 0, 255))
        depth_text = self.BUTTON_FONT.render("Depth-First", 1, (0, 0, 255))
        bi_bfs_text = self.BUTTON_FONT.render("Bidirectional BFS", 1, (0, 0, 255))

        self.WIN.blit(star_text, (self.star_button.x + self.star_button.width // 2 - star_text.get_width() // 2 , 0))
        self.WIN.blit(dijkstra_text, (self.dijkstra_button.x + self.dijkstra_button.width // 2 - dijkstra_text.get_width() // 2 , 0))
        self.WIN.blit(depth_text, (self.depth_button.x + self.depth_button.width // 2 - depth_text.get_width() // 2 , 0))
        self.WIN.blit(bi_bfs_text, (self.bi_bfs_button.x + self.bi_bfs_button.width // 2 - depth_text.get_width() // 2 , 0))

    def event_manager(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.dijkstra_button.collidepoint(event.pos):
                self.dijkstra.initialize(self)
            elif self.star_button.collidepoint(event.pos):
                self.a_star.initialize(self)
                # Can't have this because I'm going into draw_window
                # after quitting, having lost the data
                #pygame.quit()
            elif self.depth_button.collidepoint(event.pos):
                self.depth_first.initialize(self)
            elif self.bi_bfs_button.collidepoint(event.pos):
                self.bi_bfs.initialize(self)
            else:
                self.button_pressed = True
                self.initial_flag_collision = True if self.start.collidepoint(event.pos) or self.end.collidepoint(event.pos) else False
                self.initial_event = event if self.initial_flag_collision else None

                if not self.initial_flag_collision:
                    self.modify_cell_color(event) 

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.button_pressed = False
            if self.flag_has_moved_cells:
                self.move_flags(event, self.initial_event)
                self.flag_has_moved_cells = False
            else:
                self.modify_changed_var()

        if event.type == pygame.MOUSEMOTION and self.button_pressed:
            # if we collided with the initial flag AND the cursor holding
            # the flag isn't in the same cell anymore
            self.flag_has_moved_cells = True if self.initial_flag_collision and not (self.start.collidepoint(event.pos) or self.end.collidepoint(event.pos)) else False
            if not self.initial_flag_collision:
                self.modify_cell_color(event) 

    def modify_cell_color(self, event):
        for index, (cell, color, changed) in enumerate(self.cells_list):
            if cell.collidepoint(event.pos) and not changed:
                new_color = self.WHITE if color == self.BLACK else self.BLACK
                self.cells_list[index] = (cell, new_color, True)
                break

    # Need this to avoid flickering when passing over a cell
    def modify_changed_var(self):
        for index, (cell, color, changed) in enumerate(self.cells_list):
            if changed:
                self.cells_list[index] = (cell, color, False)

    def move_flags(self, event, initial_event):
        flag = self.start if self.start.collidepoint(initial_event.pos) else self.end
        initial_index = None
        endpoint_cell_position = None

        # if the end pos isn't in the same cell as the initial pos
        if not flag.collidepoint(event.pos):
            for index, (cell, color, _) in enumerate(self.cells_list):
                # turn initial flag cell self.WHITE
                if cell.collidepoint((flag.x, flag.y)):
                    initial_index = index
                    # this just repaints the initial flag cell
                    new_initial_cell = (cell, color, True)
                # give the flag the cell of the final cursor pos
                elif cell.collidepoint(event.pos):
                    endpoint_cell_position = cell

        # do it outside the function to avoid modifying the flag AND the list # items while looping
        self.cells_list[initial_index] = new_initial_cell
        if endpoint_cell_position:
            flag.x, flag.y = endpoint_cell_position.x, endpoint_cell_position.y
        # in case the cursor exits the window, we leave the flag to its initial pos
        else :
            flag.x, flag.y = (self.start.x, self.start.y) if flag is self.start else (self.end.x, self.end.y)

    def draw_window(self):
        for cell, color, changed in self.cells_list:
            if changed:
                pygame.draw.rect(self.WIN, color, cell, self.CELL_SIZE - 1)

        self.WIN.blit(self.START_FLAG, (self.start.x, self.start.y))
        self.WIN.blit(self.END_FLAG, (self.end.x, self.end.y))

        pygame.display.update()