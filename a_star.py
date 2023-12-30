import fibonacci
import time
import math

class AStar():
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

        self.pathing()
    
    def pathing(self):
        self.heap = fibonacci.Heap()
        self.position_to_heap = {}

        h = self.calculate_h((self.start.x, self.start.y))
        self.heap.insert(distance=h, position=(self.start.x, self.start.y), predecessor=None, g=0, h=h)
        self.position_to_heap[(self.start.x, self.start.y)] = self.heap.min

        while True:
            self.tie_break_min()
            if self.heap.min.position == (self.end.x, self.end.y):
                self.victory_path()
                break

            self.current_node = self.heap.extract_min()
            self.current_cell = self.coordinates_to_rect[self.current_node.position]
            self.visited_cells[self.current_node.position] = True

            self.determine_neighbours()
            self.update_heap()

            if not self.heap.min:
                break
            
            self.repaint_cells()
            self.grid.draw_window()
            time.sleep(0.1)
    
    def tie_break_min(self):
        root_list = self.heap.find_roots()

        for root in root_list:
            if root.distance == self.heap.min.distance and root.g > self.heap.min.g:
                self.heap.min = root 

    def determine_neighbours(self):
        self.current_neighbours = []

        for x in range(self.current_cell.x - self.cell_size, self.current_cell.x + self.cell_size + 1, self.cell_size):
            if x < 0 or x >= self.grid.WIDTH:
                continue
            for y in range(self.current_cell.y - self.cell_size, self.current_cell.y + self.cell_size + 1, self.cell_size):
                # The collidepoint just serves as extra verification
                if y < self.cell_size  or y >= self.grid.HEIGHT or self.current_cell.collidepoint(x, y) or self.cells_color_mapping[x, y] == "BLACK" or self.visited_cells[x, y]:
                    continue
                else:
                    self.current_neighbours.append((x, y))
    
    def update_heap(self):
        for cell_position in self.current_neighbours:
            g = self.calculate_g(cell_position)

            if cell_position not in self.position_to_heap:
                h = self.calculate_h(cell_position)

                self.position_to_heap[cell_position] = self.heap.insert(distance=h+g, position=cell_position, predecessor=self.current_node, g=g, h=h)

            elif self.position_to_heap[cell_position].g > g:
                node = self.position_to_heap[cell_position]
                node.predecessor = self.current_node
                node.g = g
                self.heap.decrease_key(node, node.g+node.h)

    def calculate_g(self, cell_position):
        x, y = cell_position[0], cell_position[1]

        if x != self.current_cell.x and y != self.current_cell.y:
            new_g = (self.cell_size * math.sqrt(2)) + self.current_node.g
        else:
            new_g = self.cell_size + self.current_node.g

        return new_g

    def calculate_h(self, cell_position):
        x2, x1 = self.end.x, cell_position[0]
        y2, y1 = self.end.y, cell_position[1]

        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def repaint_cells(self):
        for (x, y) in self.current_neighbours:
            index = self.coordinates_to_index[(x, y)]
            cell = self.coordinates_to_rect[(x, y)]

            if self.cells[index][1] == (255, 255, 255):
                self.cells[index] = (cell, (0, 255, 255), True)
        
        if self.current_cell not in [self.start, self.end]:
            index = self.coordinates_to_index[(self.current_cell.x, self.current_cell.y)]
            cell = self.coordinates_to_rect[(self.current_cell.x, self.current_cell.y)]

            self.cells[index] = (cell, (255, 100, 100), True)

    def victory_path(self):
        self.current_node = self.heap.min
        self.current_cell = self.coordinates_to_rect[self.current_node.position]
        while True:
            index = self.coordinates_to_index[(self.current_cell.x, self.current_cell.y)]
            self.cells[index] = (self.current_cell, (0, 0, 255), True)

            if self.current_node.predecessor.position == (self.start.x, self.start.y):
                break

            self.current_node = self.current_node.predecessor
            self.current_cell = self.coordinates_to_rect[self.current_node.position]

            self.grid.draw_window()
            time.sleep(0.05)