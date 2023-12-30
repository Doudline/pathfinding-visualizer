import time

class DepthFirst():
    def initialize(self, gui_instance):
        self.grid = gui_instance
        
        self.start = self.grid.start
        self.end = self.grid.end
        self.cell_size = self.grid.CELL_SIZE

        self.cells = self.grid.cells_list
        self.visited_cells = {(cell.x, cell.y): False for (cell, color, _) in self.cells if color == (255, 255, 255)}
        self.cells_color_mapping = {(cell.x, cell.y): "WHITE" if color == (255, 255, 255) else "BLACK" for (cell, color, _) in self.cells}

        self.coordinates_to_rect = self.grid.coordinates_to_rect
        self.coordinates_to_index = {(cell.x, cell.y): index for index, (cell, _, _) in enumerate(self.cells)}

        self.found_end = False
        self.pathing(self.start)

    def pathing(self, current_cell):
        self.visited_cells[current_cell.x, current_cell.y] = True
        self.repaint_cell((current_cell.x, current_cell.y), (255, 100, 100))
        current_neighbours = []

        for x in range(current_cell.x - self.cell_size, current_cell.x + self.cell_size + 1, self.cell_size):
            if x < 0 or x >= self.grid.WIDTH:
                continue
            for y in range(current_cell.y - self.cell_size, current_cell.y + self.cell_size + 1, self.cell_size):
                if (x, y) == (self.end.x, self.end.y):
                    self.found_end = True
                    break
                if y < self.cell_size  or y >= self.grid.HEIGHT or current_cell.collidepoint(x, y) or self.cells_color_mapping[x, y] == "BLACK" or self.visited_cells[x, y]:
                    continue
                else:
                    self.repaint_cell((x, y), (0, 255, 255))
                    current_neighbours.append((x, y))
        
        for cell in current_neighbours:
            if not self.found_end:
                self.pathing(self.coordinates_to_rect[cell])
            else:
                if (current_cell.x, current_cell.y) != (self.end.x, self.end.y):
                    self.repaint_cell((current_cell.x, current_cell.y), (0, 0, 255))
                break
        
    def repaint_cell(self, cell, color):
        index = self.coordinates_to_index[cell]
        cell_object = self.coordinates_to_rect[cell]
        self.cells[index] = (cell_object, color, True)

        self.grid.draw_window()
        time.sleep(0.01)