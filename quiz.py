import doctest

# NO OTHER IMPORTS!



##################################################
#  Problem 1
##################################################


def coolest(nrows, ncols, heaters):
    """
    >>> c = coolest(3, 2, [(0, 0), (1, 1)])
    >>> c == {(2, 0), (2, 1)}
    True
    >>> c = coolest(3, 2, [(1, 0)])
    >>> c == {(0, 1), (0, 0), (2, 1), (2, 0), (1, 0), (1, 1)}
    True
    >>> c = coolest(3, 2, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)])
    >>> c == {(0, 1), (2, 0), (0, 0), (2, 1)}
    True
    >>> c = coolest(3, 2, [(0, 0), (0, 1), (2, 0), (2, 1)])
    >>> c == {(0, 1), (2, 0), (0, 0), (2, 1)}
    True
    """
    
    def get_adjacent(pos, nrows, ncols):
        """
        Given a position, get all its adjacent cells
        """

        row, col = pos
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row + i < nrows and 0 <= col + j < ncols:
                    yield (row + i, col + j)

    def set_cell(grid, pos, val):

        row, col = pos
        grid[row][col] = val

    def get_value(grid, pos):
        
        row, col = pos
        return grid[row][col]

    grid = [[0 for i in range(ncols)] for j in range(nrows)]
    
    for heater in heaters:

        for other in get_adjacent(heater, nrows, ncols):
            current = get_value(grid, other)
            set_cell(grid, other, current + 1)

    sums = {}

    for i in range(nrows):
        for j in range(ncols):
            current = get_value(grid, (i, j))
            if current not in sums:
                sums[current] = {(i, j)}
            else:
                sums[current].add((i, j))

    return sums[min(sums.keys())]

##################################################
#  Problem 2
##################################################

def complete_nary(tree, n):
    """
    >>> t = [1, [2], [3], [4]]
    >>> complete_nary(t, 3)
    True
    >>> complete_nary(t, 2)
    False
    >>> t = [13, [7], [8, [99], [16, [77]], [42]]]
    >>> complete_nary(t, 2)
    False
    >>> t = [13, [7], [8, [99], [16, [77], [78], [79], [80]], [42], [43]], [9], [19]]
    >>> complete_nary(t, 4)
    True
    """
    
    def generator_bools(tree, n):

        sub_tree = tree[1:]
        if len(sub_tree) == 0:
            yield {True}

        elif len(sub_tree) == n:
            for child in sub_tree:
                for other in generator_bools(child, n):
                    yield other
        else:
            yield False


    for boolean in generator_bools(tree, n):
        if boolean == False:
            return False
    else:
        return True
    

##################################################
#  Problem 3
##################################################


def cups_puzzle(capacities, target):
    """
    >>> cups_puzzle([1, 2, 3], 0)
    [(0, 0, 0)]
    >>> cups_puzzle([3, 7], 2)
    [(0, 0), (3, 0), (0, 3), (3, 3), (0, 6), (3, 6), (2, 7)]
    """

    # In my initial code, I failed to come up with an efficient algorithm to come up 
    # with a solution. My initial thought was to take all the two element combinations
    # from all the cups and try out all of them to find a solution but this does
    # not guarantee a solution since more than 2 cups might be needed to give a
    # solution. My next thought was touse a DFS but then I realized it would be extremely
    # inefficient as I would have to enumerate all the sequences that give the target
    # and then loop through to get the shortest one. When I thought of implementind
    # a BFS, I had run out of time and I guess I managed to come with a quite 
    # efficient algorithm though I believe there are ways to make it faster.

    # In the BFS, I add to agenda, all the possible cup sequences and their new capacitites
    # in a way that finds the shortest sequence first.


    def generate_sequences(capacities, seq):
        """
        Given a sequence, generate all the possible sequences from the three actions:
        - Fill a cup
        - Empty a cup in river
        - Pour into another cup
        """

        for i in range(len(seq)):
            
            filled = seq[:i] + [capacities[i]] + seq[i+1:]
            yield filled
            
            emptied = seq[:i] + [0] + seq[i+1:]
            yield emptied
                        
            for j in range(len(seq)):
                poured = list(seq)
                if j != i and seq[i] != 0 and seq[j] != capacities[j]:
                    to_fill = capacities[j] - seq[j]

                    if to_fill >= seq[i]:
                        poured[j] += seq[i]
                        poured[i] = 0
                        
                    else:
                        poured[j] = capacities[j]
                        poured[i] -= to_fill
                    
                    yield poured


    n = len(capacities)
    start = [0] * n
    parents = {}
    seen = {tuple(start)} #takes tuples of sequences
    agenda = [start]
    found = False

    if target == 0:
        return [tuple(start)]

    while agenda and not found:
        cup = agenda.pop(0)
        for child in generate_sequences(capacities, cup):
            if tuple(child) not in seen:
                agenda.append(child)
                seen.add(tuple(child))
                parents[tuple(child)] = tuple(cup)
                if target in child:
                    found = True
                    break

    if not found:
        return None  
                
    sequence = [tuple(child)]
    end = tuple(child)
    
    while tuple(start) not in sequence:
        parent = parents[end]
        sequence.append(parent)
        end = parent

    sequence.reverse()
    return sequence


    

if __name__ == "__main__":
    doctest.testmod()
    result = cups_puzzle([4,3,10,20,13], 11)
    print(result)
