import fibonacci
import time

class Dijkstra():
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

        self.heap.insert(0, (self.start.x, self.start.y), None)
        self.position_to_heap[(self.start.x, self.start.y)] = self.heap.min

        while True:
            if self.heap.min.position == (self.end.x, self.end.y):
                self.victory_path()
                break

            self.current_node = self.heap.extract_min()
            self.current_cell = self.coordinates_to_rect[self.current_node.position]
            self.visited_cells[self.current_node.position] = True
            
            self.determine_neighbours()
            self.update_distances()
            if not self.heap.min:
                break

            self.repaint_cells()
            self.grid.draw_window()
            time.sleep(0.025)

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
        
    def update_distances(self):
        for (x, y) in self.current_neighbours:
            if x != self.current_cell.x and y != self.current_cell.y:
                distance = 14 + self.current_node.distance
            else:
                distance = 10 + self.current_node.distance
            
            if (x, y) not in self.position_to_heap:
                self.position_to_heap[x, y] = self.heap.insert(distance, (x, y), self.current_node)
            elif self.position_to_heap[x, y].distance > distance:
                self.heap.decrease_key(self.position_to_heap[x, y], distance)
                self.position_to_heap[x, y].predecessor = self.current_node
                
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


        