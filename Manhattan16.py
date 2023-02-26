class puzzle:
    def __init__(self, starting, parent):
        self.board = starting
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

    def manhattan(self):
        h = 0
        for i in range(4):
            for j in range(4):
                x, y = divmod(self.board[i][j], 4)
                h += abs(x-i) + abs(y-j)
        return h

    def goal(self):
        target_board = [[2, 3, 6, 15], [1, 8, 14, 0],
                        [4, 5, 7, 13], [11, 12, 14, 10]]
        return self.board == target_board

    def __eq__(self, other):
        return self.board == other.board


def move_function(curr):
    # Finding where 0 is
    curr = curr.board
    for i in range(4):
        for j in range(4):
            if curr[i][j] == 0:
                x, y = i, j
                break
    q = []
    directions = {'up': (-1, 0), 'down': (1, 0),
                  'left': (0, -1), 'right': (0, 1)}

    for direction, (dx, dy) in directions.items():
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 4 and 0 <= new_y < 4:
            new_board = [row[:] for row in curr]
            new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
            q.append(puzzle(new_board, curr))
    return q


def best_fvalue(openList):
    f = openList[0].f
    index = 0
    for i, item in enumerate(openList):
        if i == 0:
            continue
        if (item.f < f):
            f = item.f
            index = i

    return openList[index], index


def AStar(start):

    frontier = []
    visited = []
    frontier.append(start)

    while frontier:

        current, index = best_fvalue(frontier)
        if current.goal():
            return current
        frontier.pop(index)
        visited.append(current)

        X = move_function(current)
        for move in X:
            for item in visited:
                if item == move:
                    break
            else:
                gn = current.g + 1
                present = False

                # openList includes move
                for j, item in enumerate(frontier):
                    if item == move:
                        present = True
                        if gn < frontier[j].g:
                            frontier[j].g = gn
                            frontier[j].f = frontier[j].g + frontier[j].h
                            frontier[j].parent = current
                if not present:
                    move.g = gn
                    move.h = move.manhattan()
                    move.f = move.g + move.h
                    move.parent = current
                    frontier.append(move)

    return None


start = puzzle([[2, 3, 6, 15], [0, 1, 8, 14], [
               4, 5, 7, 13], [11, 12, 14, 10]], None)
result = AStar(start)
moves = 0

if (not result):
    print("No solution")
else:
    t = result.parent
    while t:
        moves += 1
        t = t.parent
print("Using Manhattan, moves taken until solution: " + str(moves))
