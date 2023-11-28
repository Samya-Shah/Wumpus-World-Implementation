from enum import Enum
import copy
import GameCell
import KnowledgeBase

class BrainofAgent:
    def __init__(self, map_filename, output_filename):
        self.output_filename = output_filename
        self.has_arrow = True
        self.grid_size = None
        self.cell_matrix = None
        self.init_cell_matrix = None
        self.wumpus_isalive=True
        self.cave_cell = GameCell.GameCell((-1, -1), 4)
        self.cave_cell.set_elements(GameCell.GameElement.EMPTY.value)
        self.agent_cell = None
        self.init_agent_cell = None
        self.KB = KnowledgeBase.KnowledgeBase()
        self.path = []
        self.action_list = []
        self.score = 0

        self.read_map(map_filename)

    def append_event_to_output_file(self, text: str):
        out_file = open(self.output_filename, 'a')
        out_file.write(text + '\n')
        out_file.close()


    def add_action(self, action):
        self.action_list.append(action)
        print(action)
        self.append_event_to_output_file(action.name)

        action_dict = {
            Action.GO_LEFT: self.handle_go_left,
            Action.GO_RIGHT: self.handle_go_right,
            Action.GO_UPWARDS: self.handle_go_upwards,
            Action.GO_DOWNWARDS: self.handle_go_downwards,
            Action.PROCEED: self.handle_proceed,
            Action.COLLECT_GOLD: self.handle_collect_gold,
            Action.SENSE_BREEZE: self.handle_sense_breeze,
            Action.SENSE_STENCH: self.handle_sense_stench,
            Action.FIRE_ARROW: self.handle_fire_arrow,
            Action.DEFEAT_WUMPUS: self.handle_defeat_wumpus,
            Action.BE_CONSUMED_BY_WUMPUS: self.handle_be_consumed_by_wumpus,
            Action.PLUNGE_INTO_PIT: self.handle_plunge_into_pit,
            Action.ELIMINATE_WUMPUS_AND_READY_TO_ESCAPE_CAVE: self.handle_eliminate_wumpus_and_ready_to_escape_cave,
            Action.EXIT_CAVE: self.handle_exit_cave,
            Action.DISCOVER_PIT: self.handle_discover_pit,
            Action.DISCOVER_WUMPUS: self.handle_discover_wumpus,
            Action.DISCOVER_NO_PIT: self.handle_discover_no_pit,
            Action.DISCOVER_NO_WUMPUS: self.handle_discover_no_wumpus,
            Action.DEDUCE_PIT: self.handle_deduce_pit,
            Action.DEDUCE_NOT_PIT: self.handle_deduce_not_pit,
            Action.DEDUCE_WUMPUS: self.handle_deduce_wumpus,
            Action.DEDUCE_NOT_WUMPUS: self.handle_deduce_not_wumpus,
        }

        # Get the function from action_dict dictionary
        func = action_dict.get(action, lambda: "Invalid action")

        # Execute the function
        func()

    def handle_go_left(self):
        pass

    def handle_go_right(self):
        pass

    def handle_go_upwards(self):
        pass

    def handle_go_downwards(self):
        pass

    def handle_proceed(self):
        self.score -= 10
        print("arrow: " + str(self.has_arrow))
        print("Wumpus is Alive:" + str(self.wumpus_isalive))
        print('Score: ' + str(self.score))
        self.append_event_to_output_file('Score: ' + str(self.score))

    def handle_collect_gold(self):
        self.score += 100
        print('Score: ' + str(self.score))
        self.append_event_to_output_file('Score: ' + str(self.score))

    def handle_sense_breeze(self):
        pass

    def handle_sense_stench(self):
        pass

    def handle_fire_arrow(self):
        self.has_arrow=False
        self.wumpus_isalive=False
        self.score += 100
        print('Score: ' + str(self.score))
        self.append_event_to_output_file('Score: ' + str(self.score))

    def handle_defeat_wumpus(self):
        pass

    def handle_be_consumed_by_wumpus(self):
        self.score -= 10000
        print('Score: ' + str(self.score))
        self.append_event_to_output_file('Score: ' + str(self.score))

    def handle_plunge_into_pit(self):
        self.score -= 10000
        print('Score: ' + str(self.score))
        self.append_event_to_output_file('Score: ' + str(self.score))

    def handle_eliminate_wumpus_and_ready_to_escape_cave(self):
        pass

    def handle_exit_cave(self):
        self.score += 10
        print('Score: ' + str(self.score))
        self.append_event_to_output_file('Score: ' + str(self.score))

    def handle_discover_pit(self):
        pass

    def handle_discover_wumpus(self):
        pass

    def handle_discover_no_pit(self):
        pass

    def handle_discover_no_wumpus(self):
        pass

    def handle_deduce_pit(self):
        pass

    def handle_deduce_not_pit(self):
        pass

    def handle_deduce_wumpus(self):
        pass

    def handle_deduce_not_wumpus(self):
        pass

    def turn_to(self, next_cell):
        if next_cell.map_position[0] == self.agent_cell.map_position[0]:
            if next_cell.map_position[1] - self.agent_cell.map_position[1] == 1:
                self.add_action(Action.GO_UPWARDS)
            else:
                self.add_action(Action.GO_DOWNWARDS)
        elif next_cell.map_position[1] == self.agent_cell.map_position[1]:
            if next_cell.map_position[0] - self.agent_cell.map_position[0] == 1:
                self.add_action(Action.GO_RIGHT)
            else:
                self.add_action(Action.GO_LEFT)
        else:
            raise TypeError('Error: ' + self.turn_to.__name__)


    def move_to(self, next_cell):
        self.turn_to(next_cell)
        self.add_action(Action.PROCEED)
        self.agent_cell = next_cell


    def backtracking_search(self):
        
        self.agent_cell.generate_perception()
        # If there is a Pit, Agent dies.
        if self.agent_cell.has_pit():
            self.add_action(Action.PLUNGE_INTO_PIT)
            return False

        # If there is a Wumpus, Agent dies.
        if self.agent_cell.has_wumpus():
            self.add_action(Action.BE_CONSUMED_BY_WUMPUS )
            return False

        # If there is Gold, Agent grabs Gold.
        if self.agent_cell.has_gold():
            self.add_action(Action.COLLECT_GOLD)
            self.agent_cell.collect_gold()  

        # If there is Breeze, Agent perceives Breeze.
        if self.agent_cell.has_breeze():
            self.add_action(Action.SENSE_BREEZE)

        # If there is Stench, Agent perceives Stench.
        if self.agent_cell.has_stench():
            self.add_action(Action.SENSE_STENCH)

        # If this cell is not explored, mark this cell as explored then add new percepts to the KB.
        if not self.agent_cell.is_explored():
            self.agent_cell.mark_as_explored()
            self.add_new_percepts_to_KB(self.agent_cell)

        # Initialize valid_adj_cell_list.
        valid_adj_cell_list = self.agent_cell.get_adjacent_cells(self.cell_matrix)

        # Discard the parent_cell from the valid_adj_cell_list.
        temp_adj_cell_list = []
        if self.agent_cell.parent in valid_adj_cell_list:
            valid_adj_cell_list.remove(self.agent_cell.parent)

        # Store previos agent's cell.
        pre_agent_cell = self.agent_cell

        # If the current cell is OK (there is no Breeze or Stench), Agent move to all of valid adjacent cells.
        # If the current cell has Breeze or/and Stench, Agent infers base on the KB to make a decision.
        if not self.agent_cell.is_OK():
            # Discard all of explored cells having Pit from the valid_adj_cell_list.
            temp_adj_cell_list = []
            for valid_adj_cell in valid_adj_cell_list:
                if valid_adj_cell.is_explored() and valid_adj_cell.has_pit():
                    temp_adj_cell_list.append(valid_adj_cell)
            for adj_cell in temp_adj_cell_list:
                valid_adj_cell_list.remove(adj_cell)

            temp_adj_cell_list = []

            # If the current cell has Stench, Agent infers whether the valid adjacent cells have Wumpus.
            if self.agent_cell.has_stench():
                valid_adj_cell: GameCell.GameCell
                for valid_adj_cell in valid_adj_cell_list:
                    print("Infer: ", end='')
                    print(valid_adj_cell.map_position)
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_position))
                    # self.turn_to(valid_adj_cell)

                    # Infer Wumpus.
                    self.add_action(Action.DEDUCE_WUMPUS)
                    not_alpha = [[valid_adj_cell.get_literal(GameCell.GameElement.WUMPUS, '-')]]
                    have_wumpus = self.KB.infer(not_alpha)

                    # If we can infer Wumpus.
                    if have_wumpus:
                        # Dectect Wumpus.
                        self.add_action(Action.DISCOVER_WUMPUS)

                        # FIRE_ARROW   this Wumpus.
                        self.add_action(Action.FIRE_ARROW )
                        self.add_action(Action.DEFEAT_WUMPUS)
                        valid_adj_cell.eliminate_wumpus(self.cell_matrix, self.KB)
                        self.append_event_to_output_file('KB: ' + str(self.KB.KB))

                    # If we can not infer Wumpus.
                    else:
                        # Infer not Wumpus.
                        self.add_action(Action.DEDUCE_NOT_WUMPUS)
                        not_alpha = [[valid_adj_cell.get_literal(GameCell.GameElement.WUMPUS, '+')]]
                        have_no_wumpus = self.KB.infer(not_alpha)

                        # If we can infer not Wumpus.
                        if have_no_wumpus:
                            # Detect no Wumpus.
                            self.add_action(Action.DISCOVER_NO_WUMPUS)

                        # If we can not infer not Wumpus.
                        else:
                            # Discard these cells from the valid_adj_cell_list.
                            if valid_adj_cell not in temp_adj_cell_list:
                                temp_adj_cell_list.append(valid_adj_cell)


            # If this cell still has Stench after trying to infer,
            # the Agent will try to fire arrow all of valid directions till Stench disappear.
            if self.agent_cell.has_stench():
                adj_cell_list = self.agent_cell.get_adjacent_cells(self.cell_matrix)
                if self.agent_cell.parent in adj_cell_list:
                    adj_cell_list.remove(self.agent_cell.parent)

                explored_cell_list = []
                for adj_cell in adj_cell_list:
                    if adj_cell.is_explored():
                        explored_cell_list.append(adj_cell)
                for explored_cell in explored_cell_list:
                    adj_cell_list.remove(explored_cell)

                for adj_cell in adj_cell_list:
                    print("Try: ", end='')
                    print(adj_cell.map_position)
                    self.append_event_to_output_file('Try: ' + str(adj_cell.map_position))
                    # self.turn_to(adj_cell)

                    self.add_action(Action.FIRE_ARROW )
                    if adj_cell.has_wumpus():
                        self.add_action(Action.DEFEAT_WUMPUS)
                        adj_cell.eliminate_wumpus(self.cell_matrix, self.KB)
                        self.append_event_to_output_file('KB: ' + str(self.KB.KB))

                    if not self.agent_cell.has_stench():
                        self.agent_cell.update_child_list([adj_cell])
                        break


            # If the current cell has Breeze, Agent infers whether the adjacent cells have Pit.
            if self.agent_cell.has_breeze():
                valid_adj_cell: GameCell.GameCell
                for valid_adj_cell in valid_adj_cell_list:
                    print("Infer: ", end='')
                    print(valid_adj_cell.map_position)
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_position))
                    # self.turn_to(valid_adj_cell)

                    # Infer Pit.
                    self.add_action(Action.DEDUCE_PIT)
                    not_alpha = [[valid_adj_cell.get_literal(GameCell.GameElement.PIT, '-')]]
                    have_pit = self.KB.infer(not_alpha)

                    # If we can infer Pit.
                    if have_pit:
                        # Detect Pit.
                        self.add_action(Action.DISCOVER_PIT)

                        # Mark these cells as explored.
                        valid_adj_cell.mark_as_explored()

                        # Add new percepts of these cells to the KB.
                        self.add_new_percepts_to_KB(valid_adj_cell)

                        # Update parent for this cell.
                        valid_adj_cell.update_parent(valid_adj_cell)

                        # Discard these cells from the valid_adj_cell_list.
                        temp_adj_cell_list.append(valid_adj_cell)

                    # If we can not infer Pit.
                    else:
                        # Infer not Pit.
                        self.add_action(Action.DEDUCE_NOT_PIT)
                        not_alpha = [[valid_adj_cell.get_literal(GameCell.GameElement.PIT, '+')]]
                        have_no_pit = self.KB.infer(not_alpha)

                        # If we can infer not Pit.
                        if have_no_pit:
                            # Detect no Pit.
                            self.add_action(Action.DISCOVER_NO_PIT)

                        # If we can not infer not Pit.
                        else:
                            # Discard these cells from the valid_adj_cell_list.
                            temp_adj_cell_list.append(valid_adj_cell)

        temp_adj_cell_list = list(set(temp_adj_cell_list))

        # Select all of the valid nexts cell from the current cell.
        for adj_cell in temp_adj_cell_list:
            valid_adj_cell_list.remove(adj_cell)
        self.agent_cell.update_child_list(valid_adj_cell_list)

        # Move to all of the valid next cells sequentially.
        for next_cell in self.agent_cell.child_list:
            self.move_to(next_cell)
            print("Move to: ", end='')
            print(self.agent_cell.map_position)
            self.append_event_to_output_file('Move to: ' + str(self.agent_cell.map_position))

            if not self.backtracking_search():
                return False

            self.move_to(pre_agent_cell)
            print("Backtrack: ", end='')
            print(pre_agent_cell.map_position)
            self.append_event_to_output_file('Backtrack: ' + str(pre_agent_cell.map_position))

        return True
    
    def add_new_percepts_to_KB(self, cell):
        adj_cell_list = cell.get_adjacent_cells(self.cell_matrix)

        # Note: Pit and Wumpus can not appear at the same cell.
        # Hence: * If a cell has Pit, then it can not have Wumpus.
        #        * If a cell has Wumpus, then it can not have Pit.

        # PL: Pit?
        sign = '-'
        if cell.has_pit():
            sign = '+'
            self.KB.add_clause([cell.get_literal(GameCell.GameElement.WUMPUS, '-')])
        self.KB.add_clause([cell.get_literal(GameCell.GameElement.PIT, sign)])
        sign_pit = sign

        # PL: Wumpus?
        sign = '-'
        if cell.has_wumpus():
            sign = '+'
            self.KB.add_clause([cell.get_literal(GameCell.GameElement.PIT, '-')])
        self.KB.add_clause([cell.get_literal(GameCell.GameElement.WUMPUS, sign)])
        sign_wumpus = sign

        # Check the above constraint.
        if sign_pit == sign_wumpus == '+':
            raise TypeError('Logic Error: Pit and Wumpus can not appear at the same cell.')

        # PL: Breeze?
        sign = '-'
        if cell.has_breeze():
            sign = '+'
        self.KB.add_clause([cell.get_literal(GameCell.GameElement.BREEZE, sign)])

        # PL: Stench?
        sign = '-'
        if cell.has_stench():
            sign = '+'
        self.KB.add_clause([cell.get_literal(GameCell.GameElement.STENCH, sign)])

        # PL: This cell has Breeze iff At least one of all of adjacent cells has a Pit.
        # B <=> Pa v Pb v Pc v Pd
        if cell.has_breeze():
            # B => Pa v Pb v Pc v Pd
            clause = [cell.get_literal(GameCell.GameElement.BREEZE, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(GameCell.GameElement.PIT, '+'))
            self.KB.add_clause(clause)

            # Pa v Pb v Pc v Pd => B
            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(GameCell.GameElement.BREEZE, '+'),
                          adj_cell.get_literal(GameCell.GameElement.PIT, '-')]
                self.KB.add_clause(clause)

        # PL: This cell has no Breeze then all of adjacent cells has no Pit.
        # -Pa ^ -Pb ^ -Pc ^ -Pd
        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(GameCell.GameElement.PIT, '-')]
                self.KB.add_clause(clause)

        # PL: This cell has Stench iff At least one of all of adjacent cells has a Wumpus.
        if cell.has_stench():
            # S => Wa v Wb v Wc v Wd
            clause = [cell.get_literal(GameCell.GameElement.STENCH, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(GameCell.GameElement.WUMPUS, '+'))
            self.KB.add_clause(clause)

            # Wa v Wb v Wc v Wd => S
            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(GameCell.GameElement.STENCH, '+'),
                          adj_cell.get_literal(GameCell.GameElement.WUMPUS, '-')]
                self.KB.add_clause(clause)

        # PL: This cell has no Stench then all of adjacent cells has no Wumpus.
        # -Wa ^ -Wb ^ -Wc ^ -Wd
        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(GameCell.GameElement.WUMPUS, '-')]
                self.KB.add_clause(clause)

        print(self.KB.KB)
        self.append_event_to_output_file(str(self.KB.KB))

    def read_map(self, map_filename):
        file = open(map_filename, 'r')

        self.grid_size = int(file.readline())
        raw_map = [line.split('.') for line in file.read().splitlines()]

        self.cell_matrix = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for ir in range(self.grid_size):
            for ic in range(self.grid_size):
                self.cell_matrix[ir][ic] = GameCell.GameCell((ir, ic), self.grid_size)
                self.cell_matrix[ir][ic].set_elements(raw_map[ir][ic])
                if GameCell.GameElement.AGENT.value in raw_map[ir][ic]:
                    if GameCell.GameElement.AGENT.value == 'A':
                        print("Currently agent is at positon : (1,1) ")
                    self.agent_cell = self.cell_matrix[ir][ic]
                    self.agent_cell.update_parent(self.cave_cell)
                    self.init_agent_cell = copy.deepcopy(self.agent_cell)

        file.close()
        self.init_cell_matrix = copy.deepcopy(self.cell_matrix)

    def solve_wumpus_world(self):
        # Reset file output
        out_file = open(self.output_filename, 'w')
        out_file.close()

        self.backtracking_search()

        victory_flag = True
        for cell_row in self.cell_matrix:
            for cell in cell_row:
                if cell.has_gold() or cell.has_wumpus():
                    victory_flag = False
                    break
        if victory_flag:
            self.add_action(Action.ELIMINATE_WUMPUS_AND_READY_TO_ESCAPE_CAVE )

        if self.agent_cell.parent == self.cave_cell:
            self.add_action(Action.EXIT_CAVE)

        return self.action_list, self.init_agent_cell, self.init_cell_matrix

 class Action(Enum):
    GO_LEFT= 1
    GO_RIGHT = 2
    GO_UPWARDS = 3
    GO_DOWNWARDS = 4
    PROCEED = 5
    COLLECT_GOLD = 6
    SENSE_BREEZE = 7
    SENSE_STENCH = 8
    FIRE_ARROW = 9
    DEFEAT_WUMPUS = 10
    BE_CONSUMED_BY_WUMPUS = 11
    PLUNGE_INTO_PIT = 12
    ELIMINATE_WUMPUS_AND_READY_TO_ESCAPE_CAVE = 13
    EXIT_CAVE = 14
    DISCOVER_PIT = 15
    DISCOVER_WUMPUS = 16
    DISCOVER_NO_PIT = 17
    DISCOVER_NO_WUMPUS = 18
    DEDUCE_PIT = 19
    DEDUCE_NOT_PIT = 20
    DEDUCE_WUMPUS = 21
    DEDUCE_NOT_WUMPUS = 22   
