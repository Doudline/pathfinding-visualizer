from collections import deque
import time

class BidirectionalBFS():
    class Node():
        def __init__(self, cell_object, coordinates, predecessor):
            self.cell_object = cell_object
            self.coordinates = coordinates
            self.predecessor = predecessor

    def initialize(self, gui_instance):
        self.grid = gui_instance
        
        self.start = self.grid.start
        self.end = self.grid.end
        self.cell_size = self.grid.CELL_SIZE

        self.cells = self.grid.cells_list
        self.cells_color_mapping = {(cell.x, cell.y): "WHITE" if color == (255, 255, 255) else "BLACK" for (cell, color, _) in self.cells}

        self.start_visited_cells = {(cell.x, cell.y): False for (cell, color, _) in self.cells if color == (255, 255, 255)}
        self.end_visited_cells = {(cell.x, cell.y): False for (cell, color, _) in self.cells if color == (255, 255, 255)}

        self.start_visited_nodes = {}
        self.end_visited_nodes = {}

        self.coordinates_to_rect = self.grid.coordinates_to_rect
        self.coordinates_to_index = {(cell.x, cell.y): index for index, (cell, _, _) in enumerate(self.cells)}

        self.pathing()
    
    def pathing(self):
        self.launch_queues()
        self.start_neighbours = set()
        self.end_neighbours = set()

        self.path_found = False
        while self.path_found is False:
            if not (self.start_queue and self.end_queue):
                break
            self.get_current_nodes()
            self.get_neighbours()

    def launch_queues(self):
        start_node = self.Node(self.start, (self.start.x, self.start.y), None)
        end_node = self.Node(self.end, (self.end.x, self.end.y), None)

        self.start_queue = deque([start_node])
        self.end_queue = deque([end_node])

    def get_current_nodes(self):
        self.current_start_node = self.start_queue.popleft()                
        self.current_end_node = self.end_queue.popleft()                

        self.start_visited_cells[(self.current_start_node.coordinates)] = True
        self.end_visited_cells[(self.current_end_node.coordinates)] = True

        self.start_visited_nodes[(self.current_start_node.coordinates)] = self.current_start_node
        self.end_visited_nodes[(self.current_end_node.coordinates)] = self.current_end_node

        self.repaint_cell((self.current_start_node.coordinates), (255, 100, 100))
        self.repaint_cell((self.current_end_node.coordinates), (255, 100, 100))

    def get_neighbours(self):
        self.determine_start_neighbours()
        self.determine_end_neighbours()

    def determine_start_neighbours(self):
        current_x, current_y = self.current_start_node.coordinates

        for x in range(current_x - self.cell_size, current_x + self.cell_size + 1, self.cell_size):
            if x < 0 or x >= self.grid.WIDTH:
                continue
            for y in range(current_y - self.cell_size, current_y + self.cell_size + 1, self.cell_size):
                if y < self.cell_size  or y >= self.grid.HEIGHT or self.current_start_node.cell_object.collidepoint(x, y) or self.cells_color_mapping[x, y] == "BLACK" or self.start_visited_cells[x, y] or (x, y) in self.start_neighbours:
                    continue
                elif self.end_visited_cells[x, y]:
                    self.victory_path((x, y), "start")
                    break 
                else:
                    neighbour_object = self.coordinates_to_rect[(x, y)]
                    self.start_queue.append(self.Node(neighbour_object, (x, y), self.current_start_node))
                    
                    self.start_neighbours.add((x, y))
                    self.repaint_cell((x, y), (0, 255, 255))
    
    def determine_end_neighbours(self):
        current_x, current_y = self.current_end_node.coordinates

        for x in range(current_x - self.cell_size, current_x + self.cell_size + 1, self.cell_size):
            if x < 0 or x >= self.grid.WIDTH:
                continue
            for y in range(current_y - self.cell_size, current_y + self.cell_size + 1, self.cell_size):
                if y < self.cell_size  or y >= self.grid.HEIGHT or self.current_end_node.cell_object.collidepoint(x, y) or self.cells_color_mapping[x, y] == "BLACK" or self.end_visited_cells[x, y] or (x, y) in self.end_neighbours:
                    continue
                elif self.start_visited_cells[x, y]:
                    self.victory_path((x, y), "end")
                    break
                else:
                    neighbour_object = self.coordinates_to_rect[(x, y)]
                    self.end_queue.append(self.Node(neighbour_object, (x, y), self.current_end_node))

                    self.end_neighbours.add((x, y))
                    self.repaint_cell((x, y), (0, 255, 255))
                    
    def repaint_cell(self, cell, color):
        index = self.coordinates_to_index[cell]
        cell_object = self.coordinates_to_rect[cell]
        self.cells[index] = (cell_object, color, True)

        self.grid.draw_window()
        time.sleep(0.02)

    def victory_path(self, coordinates, start_or_end):
        if start_or_end == "end":
            self.current_start_node = self.start_visited_nodes[coordinates]
        else:
            self.current_end_node = self.end_visited_nodes[coordinates]

        while True:
            if not (self.current_start_node.predecessor or self.current_end_node.predecessor):
                break

            if self.current_start_node.predecessor:
                self.repaint_cell(self.current_start_node.coordinates, (0, 0, 255))
                self.current_start_node = self.current_start_node.predecessor

            if self.current_end_node.predecessor:
                self.repaint_cell(self.current_end_node.coordinates, (0, 0, 255))
                self.current_end_node = self.current_end_node.predecessor

            self.grid.draw_window()
            time.sleep(0.02)

        self.path_found = True