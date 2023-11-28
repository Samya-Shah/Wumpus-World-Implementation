from enum import Enum

#  Enum class for game elements
class GameElement(Enum):
    GOLD   = 'G'
    PIT    = 'P'
    WUMPUS = 'W'
    BREEZE = 'B'
    STENCH = 'S'
    AGENT  = 'A'
    EMPTY  = '-'
    
# Class for game cell
class GameCell:
    # Constructor for GameCell
    def __init__(self, grid_position, grid_size):
        self.grid_position = grid_position                                  
        self.map_position = grid_position[1] + 1, grid_size - grid_position[0]          
        self.index_position = grid_size * (self.map_position[1] - 1) + self.map_position[0]    
        self.grid_size = grid_size

        self.is_cell_explored = False
        self.perception = [False, False, False, False, False]  # [-G, -P, -W, -B, -S]

        self.parent = None
        self.child_list = []

        self.elements_str = None  
 
    # Method to initialize elements
    def initialize(self, elements_str):
        for element in elements_str:
            if element == GameElement.GOLD.value:
                self.perception[0] = True
            elif element == GameElement.PIT.value:
                self.perception[1] = True
            elif element == GameElement.WUMPUS.value:
                self.perception[2] = True
            elif element == GameElement.BREEZE.value:
                self.perception[3] = True
            elif element == GameElement.STENCH.value:
                self.perception[4] = True
            elif element == GameElement.AGENT.value:
                continue
            elif element == GameElement.EMPTY.value:
                continue
            else:
                raise TypeError('Error: GameCell.initialize')
    
    # Method to set elements
    def set_elements(self, elements_str):
        self.elements_str = elements_str
    # Modify this method
    def generate_perception(self):
        # Ask for user input
        perception_input = input("Please enter the perception sequence for the cell (e.g., False,False,False,False,False): ")
        # Convert the input string to a list of boolean values
        self.perception = [s.strip().lower() == 'true' for s in perception_input.split(',')]
    # Method to check if cell has gold
    def has_gold(self):
        return self.perception[0]

    # Method to check if cell has pit
    def has_pit(self):
        return self.perception[1]

    # Method to check if cell has wumpus
    def has_wumpus(self):
        return self.perception[2]

    # Method to check if cell has breeze
    def has_breeze(self):
        return self.perception[3]

    # Method to check if cell has stench
    def has_stench(self):
        return self.perception[4]

    # Method to check if cell is OK
    def is_OK(self):
        return not self.has_breeze() and not self.has_stench()


    # Method to update parent cell
    def update_parent(self, parent_cell):
        self.parent = parent_cell


    # Method to collect gold
    def collect_gold(self):
        self.perception[0] = False


    # Method to eliminate wumpus
    def eliminate_wumpus(self, game_cell_grid, knowledge_base):
        # Remove Wumpus.
        self.perception[2] = False

        # Remove Stench from adjacent cells.
        adj_cell_list_of_wumpus_cell = self.get_adjacent_cells(game_cell_grid)
        for stench_cell in adj_cell_list_of_wumpus_cell:
            remove_stench_flag = True
            adjacent_cells_of_stench_cell = stench_cell.get_adjacent_cells(game_cell_grid)
            for adjacent_cell in adjacent_cells_of_stench_cell:
                if adjacent_cell.has_wumpus():
                    remove_stench_flag = False
                    break
            if remove_stench_flag:
                stench_cell.perception[4] = False
                literal = self.get_literal(GameElement.STENCH, '+')
                knowledge_base.del_clause([literal])
                literal = self.get_literal(GameElement.STENCH, '-')
                knowledge_base.add_clause([literal])

                adjacent_cells = stench_cell.get_adjacent_cells(game_cell_grid)
                # S => Wa v Wb v Wc v Wd
                clause = [stench_cell.get_literal(GameElement.STENCH, '-')]
                for adjacent_cell in adjacent_cells:
                    clause.append(adjacent_cell.get_literal(GameElement.WUMPUS, '+'))
                knowledge_base.del_clause(clause)

                # Wa v Wb v Wc v Wd => S
                for adjacent_cell in adjacent_cells:
                    clause = [stench_cell.get_literal(GameElement.STENCH, '+'),
                              adjacent_cell.get_literal(GameElement.WUMPUS, '-')]
                    knowledge_base.del_clause(clause)

     # Method to get adjacent cells
    def get_adjacent_cells(self, game_cell_grid):
        adjacent_cells = []
        adjacent_grid_positions = [(self.grid_position[0], self.grid_position[1] + 1),   # Right
                                    (self.grid_position[0], self.grid_position[1] - 1),   # Left
                                    (self.grid_position[0] - 1, self.grid_position[1]),   # Up
                                    (self.grid_position[0] + 1, self.grid_position[1])]   # Down

        for adjacent_grid_position in adjacent_grid_positions:
            if 0 <= adjacent_grid_position[0] < self.grid_size and 0 <= adjacent_grid_position[1] < self.grid_size:
                adjacent_cells.append(game_cell_grid[adjacent_grid_position[0]][adjacent_grid_position[1]])

        return adjacent_cells


    # Method to check if cell is explored
    def is_explored(self):
        return self.is_cell_explored

    # Method to mark cell as explored
    def mark_as_explored(self):
        self.is_cell_explored = True


    # Method to update child list
    def update_child_list(self, valid_adjacent_cells):
        for adjacent_cell in valid_adjacent_cells:
            if adjacent_cell.parent is None:
                self.child_list.append(adjacent_cell)
                adjacent_cell.update_parent(self)


    # Method to get literal
    def get_literal(self, game_element: GameElement, sign='+'):    # sign='-': not operator
        if game_element == GameElement.PIT:
            i = 1
        elif game_element == GameElement.WUMPUS:
            i = 2
        elif game_element == GameElement.BREEZE:
            i = 3
        elif game_element == GameElement.STENCH:
            i = 4
        else:
            raise TypeError('Error: ' + self.get_literal.__name__)

        factor = 10 ** len(str(self.grid_size * self.grid_size))
        literal = i * factor + self.index_position
        if sign == '-':
            literal *= -1

        return literal

