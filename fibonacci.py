# A simple Fibonacci min-ordered heap implementation that I learned for my
# pathfinder visualizer project. 

# Has insert for new individual nodes, consolidate, extract min and decrease
# key.

import math

class Heap():
    class Node():
        def __init__(self, distance=float("inf"), position=None, predecessor=None, g=float("inf"), h=float("inf")):
            self.distance = distance
            self.position = position
            self.predecessor = predecessor
            self.g = g
            self.h = h

            self.degree = 0
            self.parent = None
            self.child = None
            self.left = None
            self.right = None
            self.mark = False
    
    def __init__(self):
        self.min = None
        self.node_count = 0

    def find_roots(self):
        roots_list = []
        root = self.min
        if root:
            roots_list.append(root)
            while root.right is not self.min:
                root = root.right
                roots_list.append(root)
        
        return roots_list

    def print_roots(self):
        roots_list = self.find_roots()
        for root in roots_list:
            print(root.distance)

    def print_trees(self):
        roots_list = self.find_roots()
        for root in roots_list:
            print(root.distance)
            self._print_tree(root.child, root.child)

    def _print_tree(self, root, initial_child, indent=1):
        if not root:
            return
        print("  " * indent + str(root.distance))

        if root.child:
            self._print_tree(root.child, root.child, indent + 1)
        if root.right is not initial_child:
            self._print_tree(root.right, initial_child, indent)

    def insert(self, distance, position, predecessor, g=None, h=None):
        new_node = self.Node(distance, position, predecessor, g, h)
        self.node_count += 1

        if not self.min:
            new_node.right = new_node
            new_node.left = new_node
            self.min = new_node

        new_node.right = self.min.right 
        new_node.right.left = new_node

        self.min.right = new_node
        new_node.left = self.min

        if self.min.distance > new_node.distance:
            self.min = new_node
        
        return new_node
    
    def extract_min(self):
        self.node_to_extract = self.min
        if not self.node_to_extract:
            print("Root list is empty.")
            return

        self._update_root()

        if self.min:
            # i.e. only consolidate if number root nodes > 1
            if self.min.right is not self.min:
                self.consolidate()
            self._update_min()

        self.node_to_extract.child = None
        self.node_to_extract.right = None
        self.node_to_extract.left = None
        self.node_count -= 1

        return self.node_to_extract

    def _update_root(self):
        child_node = self.node_to_extract.child

        # Four cases depending on the state of the root list and self.min.
        # if self.min has a child:
        #       1. if also has root neighbours:
        #           - we attach the root neighbours to the leftmost and
        #             rightmost root neighbours
        #       2. else:
        #           - the children list keeps its current attachments; it will
        #             become the new root list
        #       - the child becomes self.min
        # if self.min has no child:
        #       3. if has root neighbours:
        #           - we attach the left-right neighbours together
        #           - self.min = self.min.right  
        #       4. else (i.e. self.min was the only node):
        #           - self.min = None, as the+ will be empty

        if child_node:
            self.min = child_node
            while True:
                child_node.parent = None
                child_node = child_node.right
                if child_node is self.node_to_extract.child:
                    break
            
            child_node = self.node_to_extract.child
            last_child_node = child_node.left

            if self.node_to_extract.right is not self.node_to_extract:
                self.node_to_extract.left.right = child_node
                self.node_to_extract.right.left = last_child_node

                child_node.left = self.node_to_extract.left
                last_child_node.right = self.node_to_extract.right

        elif self.node_to_extract.right is not self.node_to_extract:
            self.min = self.node_to_extract.right
            self.node_to_extract.left.right = self.node_to_extract.right
            self.node_to_extract.right.left = self.node_to_extract.left
            
        else:
            self.min = None

    def consolidate(self):
        golden_ratio = (1 + math.sqrt(5)) / 2
        max_degree = int(math.log(self.node_count, golden_ratio))

        self.trees_by_degree = [None] * (max_degree + 1)

        roots_list = self.find_roots()
        for root in roots_list:
            if not self.trees_by_degree[root.degree]:
                self.trees_by_degree[root.degree] = root
            else:
                self._consolidate_helper(root)
        
        self._update_min()

    def _consolidate_helper(self, child):
        tree = self.trees_by_degree[child.degree]
        if tree.distance > child.distance:
            tree, child = child, tree

        self._unlink_child(child)
        self._link_child_to_tree(child, tree)
        self._update_degree_and_recurse(child, tree)

    def _unlink_child(self, child):
        child.left.right = child.right
        child.right.left = child.left
        child.right, child.left = child, child

        child.parent = None

    def _link_child_to_tree(self, child, tree):
        child.parent = tree
        if not tree.child:
            tree.child = child
        else:
            child.right = tree.child.right
            child.left = tree.child

            tree.child.right.left = child
            tree.child.right = child

    def _update_degree_and_recurse(self, child, tree):
        self.trees_by_degree[tree.degree] = None
        tree.degree += 1

        if child is self.min:
            self.min = tree
        if self.trees_by_degree[tree.degree]:
            self._consolidate_helper(tree)
        else:
            self.trees_by_degree[tree.degree] = tree

    def _update_min(self):
        if not self.min:
            return

        # First we check the initial root list for a new min
        root_node = self.min
        min_node = root_node
        while root_node.right is not self.min:
            root_node = root_node. right
            if root_node.distance < min_node.distance:
                min_node = root_node

        # Then we check self.min's initial children
        if self.min.child:
            current_child = self.min.child
            while True:
                if current_child.distance < min_node.distance:
                    min_node = current_child
                if current_child.right is self.min.child:
                    break
                current_child = current_child.right

        self.min = min_node
    
    def decrease_key(self, node, new_value):
        if node and isinstance(new_value, (int, float)) and new_value < node.distance:
            node.distance = new_value
        
        if not node or not isinstance(new_value, (int, float)) or not node.parent or node.distance >= node.parent.distance:
            return
        
        while True:
            parent_node = node.parent
            marked = parent_node.mark if parent_node else None

            self._cut_node(node, parent_node)

            if parent_node:
                parent_node.degree -= 1
                # i.e. set the parent mark iff parent is not a root
                if parent_node.parent and not parent_node.mark:
                    parent_node.mark = True
            if marked:
                node = node.parent
            else:
                break
        
        self._update_min()

    def _cut_node(self, node, parent_node):
        if node.right is not node:
            parent_node.child = node.right
        else:
            parent_node.child = None

        node.mark = False

        self._unlink_child(node)
        self._add_node_to_root_list(node)

    def _add_node_to_root_list(self, node):
        node.right = self.min.right
        node.right.left = node

        node.left = self.min
        self.min.right = node

a = Heap()