"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def slide(lst):
    """
    Helper function which slides nonzero values to the left.
    """
    slide_list = [0] * len(lst)
    slide_index = 0
    #Iterate over line and slide all non-zero values to the left
    for lst_index in range(0, len(lst)):
        if lst[lst_index] != 0:
            slide_list[slide_index] = lst[lst_index]
            slide_index += 1
    return slide_list


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    #First, slide all non-zeroes to the left
    slid_line = slide(line)
    #For each pair of identical numbers [n,n], replace with [2n,0], move to next pair
    #If not identical, shift frame by 1 and keep searching
    #Edge case - if last index with no pair, put in as-is to avoid errors
    copy_list = [0] * len(slid_line)
    index = 0
    while index < len(slid_line):
        if index == len(slid_line) - 1:
            copy_list[index] = slid_line[index]
            index += 1
        elif slid_line[index] == slid_line[index + 1]:
            copy_list[index] = 2 * slid_line[index]
            copy_list[index + 1] = 0
            index += 2
        else:
            copy_list[index] = slid_line[index]
            index += 1
    #Lastly, slide all non-zeroes to the left
    return slide(copy_list)

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self._grid = 0
        self.reset()
        self._initial_tiles = {UP:[(0, dummy_col) for dummy_col in range(self._width)], 
                         DOWN:[(self._height - 1, dummy_col) for dummy_col in range(self._width)], 
                         LEFT:[(dummy_row, 0) for dummy_row in range(self._height)], 
                         RIGHT:[(dummy_row, self._width - 1) for dummy_row in range(self._height)]}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._width)] for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        moves_dict = {UP: self._height, DOWN: self._height, LEFT: self._width, RIGHT: self._width}
        changed = False #Our flag
        
        for initial_tile_coord in self._initial_tiles[direction]:
            holding_list = [] #This will hold our temporary list of values for each line
            holding_list_coords = [] #This will store the coordinates of the temp list components
            for step in range(moves_dict[direction]): #Iterate through grid and generate temp list and store coordinates
                row = initial_tile_coord[0] + step * OFFSETS[direction][0]
                col = initial_tile_coord[1] + step * OFFSETS[direction][1]
                holding_list_coords.append((row,col))
                holding_list.append(self._grid[row][col])
            merged_holding_list = merge(holding_list) #Merge the values
            for coords in holding_list_coords: #Replace all values in each line with the merged values in the same order
                self._grid[coords[0]][coords[1]] = merged_holding_list[holding_list_coords.index(coords)]
            for merged_value in merged_holding_list: #Check if anything has changed at all by comparing initial and merged values
                if merged_value != holding_list[merged_holding_list.index(merged_value)]:
                    changed = True
        if changed: #If something has changed, call a new tile
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        rand_row = random.randrange(self._height)
        rand_col = random.randrange(self._width)
        rand_value = random.choice((2,2,2,2,2,2,2,2,2,4))
        if self._grid[rand_row][rand_col] == 0:
            self._grid[rand_row][rand_col] = rand_value
        else:
            self.new_tile() #If the call fails by sheer chance, redo
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

board = TwentyFortyEight(4,4)
poc_2048_gui.run_gui(board)
