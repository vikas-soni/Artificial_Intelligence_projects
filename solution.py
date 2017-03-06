assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
    
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
left_diagonal = [rows[i]+cols[i] for i in range(0,len(rows))]
right_diagonal = [rows[i]+cols[9-i-1] for i in range(0,len(rows))]
diagonal_units = [left_diagonal, right_diagonal]
unitlist = row_units + column_units + square_units+diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    
    #we will look at each unit (row/col/square) one by one to find naked twins
    #################################################################################
    # 1. Look at all row units
    
    # assert to make sure values is a valid dic for sudoku
    assert len(values) == 81
    # iterate over each row
    for r in rows:
        #we might need to re-find naked twins in same row again.
        # this is because once we remove naked twins values from all boxes in a unit,
        #it can generate new naked twins
        redo_row = 1 #initially set this to 1
        # get the cross list of all coloumns in that row
        row_entries = cross(r, cols)
        while(redo_row == 1):
            entry_remove=[]
            redo_row = 0
            # traverse each row entry and look for naked twins
            for i in row_entries:
                if(len(values[i]) == 2): # if value is of length 2, then only it can be a part of naked twins
                    remain_row_entries = row_entries # this is done to make a list of row boxes not containing i
                    remain_row_entries.remove(i) # remove this entry i to have a list of boxes in row except i
                    for j in remain_row_entries: # iterating over remainig boxes in the row
                        if(values[j] == values[i]): # if values match
                            redo_row =1             # that means there is a naked twin and hence possibility of a new twin generation
                            entry_remove.append(i) # making a list of boxes which had naked twins. now those boxes need not be visited in 2nd pass on same row
                            entry_remove.append(j)
                            # remove naked twins from remaining entries
                            remove_list = remain_row_entries
                            remove_list.remove(j) #once twins have been found, we need to iterate over reaming box in the unit to remove those 2 values
                            for k in remove_list:
                                values[k]=values[k].replace(values[i][0],'') #remove 1st value
                                values[k]=values[k].replace(values[i][1],'') # remove 2nd value           
            # this is for 2nd pass on same row. for 2nd pass we dont need to go over twins which were already found
            for rem in entry_remove:
                if rem in row_entries:
                    row_entries.remove(rem)
    ###############################################################################################            
    # 2. Look at all col units
    
    # all comments/logic for above row is same for col and square
    
    # iterate over each col
    for c in cols:
        redo_col = 1
        # get the cross list of all coloumns in that row
        col_entries = cross(rows, c)
        while(redo_col == 1):   
            entry_remove=[]
            redo_col = 0
            # traverse each row entry and look for naked twins
            for i in col_entries:
                if(len(values[i]) == 2):
                    remain_col_entries = col_entries
                    remain_col_entries.remove(i)
                    for j in remain_col_entries:
                        if(values[j] == values[i]):
                            redo_col = 1
                            entry_remove.append(i)
                            entry_remove.append(j)
                            # remove naked twins from remaining entries
                            remove_list = remain_col_entries
                            remove_list.remove(j)
                            for k in remove_list:
                                values[k]=values[k].replace(values[i][0],'')
                                values[k]=values[k].replace(values[i][1],'')
            for rem in entry_remove:
                if rem in col_entries:
                    col_entries.remove(rem)     
    ##################################################################################################                
    # 2. Look at all square units
    
    # iterate over each square
    for rs in ('ABC','DEF','GHI'):
        for cs in ('123','456','789'):
            redo_sq = 1
            # get the cross list of all squares
            sq_entries = cross(rs, cs)
            while(redo_sq == 1):   
                entry_remove=[]
                redo_sq = 0
                # traverse each square entry and look for naked twins
                for i in sq_entries:
                    if(len(values[i]) == 2):
                        remain_sq_entries = sq_entries
                        remain_sq_entries.remove(i)
                        for j in remain_sq_entries:
                            if(values[j] == values[i]):
                                redo_sq = 1
                                entry_remove.append(i)
                                entry_remove.append(j)
                                # remove naked twins from remaining entries
                                remove_list = remain_sq_entries
                                remove_list.remove(j)
                                for k in remove_list:
                                    values[k]=values[k].replace(values[i][0],'')
                                    values[k]=values[k].replace(values[i][1],'')
                for rem in entry_remove:
                    if rem in sq_entries:
                        sq_entries.remove(rem)                    
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    result_dict = {}
    grid_len = len(grid)
    assert grid_len == 81
    
    for index in range(0,grid_len):
        if(grid[index] == '.'):
            result_dict[boxes[index]] = '123456789'
        else:
            result_dict[boxes[index]]=grid[index]
    return result_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    assert len(values)==81
    for key in values:
        val = values[key]
        if(len(val) == 1):
            """ find list of all peers"""
            peer = peers[key]
            for it in peer:
                values[it] = values[it].replace(val,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in cols:
            temp=[]
            for box in unit:
                if digit in values[box]:
                    temp.append(box)
            if(len(temp)==1):
                values[temp[0]]=digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        assert len(values)==81
        for key in values:
            val = values[key]
            if(len(val) == 1):
                """ find list of all peers"""
                peer = peers[key]
                for it in peer:
                    values[it] = values[it].replace(val,'')
        # Your code here: Use the Only Choice Strategy
        for unit in unitlist:
            for digit in cols:
                temp=[]
                for box in unit:
                    if digit in values[box]:
                        temp.append(box)
                if(len(temp)==1):
                    values[temp[0]]=digit

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    status = search(values)
    if status is False:
        return False
    return values
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
