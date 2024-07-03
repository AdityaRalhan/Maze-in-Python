import sys

class Node():
    def __init__(self,state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state): # checks if frontier has any state
        # any() returns true if any item in an iterable are true

        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0 # return true if length of frontier list is ZERO

    def remove(self):

        if self.empty():
            raise Exception("Empty frontier")

        else:
            
            # removing the last item in a frontier as we are doing using STACK. 
            # In STACK it is LAST IN FIRST OUT so we remove the last item in frontier
            node = self.frontier[-1]


            # now frontier is from 0th index to second last
            self.frontier = self.frontier[:-1] 
            return node
                        

# new class QueueFrontier INHERITS from stack frontier
# it will do everything stack frontier did EXCEPT it will remove a node from the start and not the end as in QUEUE search it is first in first out 
class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty(): # basically if self.empty is true 
            raise Exception("empty frontier")
        
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        

# it will take a maze like text file and figure out how to solve it
class Maze():

    def __init__(self, filename):
        
        # read file and set height and width of maze
        with open(filename) as f:
            contents = f.read() # contents is a string variable

        # validate start and goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal")
        
        # determine height and width of maze
        # contents.splitlines() puts each line as a string in a list
        contents = contents.splitlines()

        # so finding the length of this list would tell us how many lines there are
        self.height = len(contents)

        # This line calculates the width of the file's contents by finding the length of the longest line. The max function is used with a generator expression len(line) for line in contents, which computes the length of each line in the contents list. max then returns the maximum length found.
        self.width = max(len(line) for line in contents)


        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range (self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False) # to show this position is NOT A WALL

                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)

                    elif contents[i][j] == " ":
                        row.append(False)

                    else :
                        row.append(True)

                # If an IndexError occurs (which can happen if a line is shorter than the maximum width), False is appended to row, treating the out-of-bound area as an open space.
                except IndexError:
                    row.append(False)

            # After processing all columns in a row, the ROW LIST is appended to self.walls LIST
            self.walls.append(row)

        self.solution = None # just initializing solution
        # The solution is expected to be a list or set of coordinates (tuples) that represent the path from the start to the goal.


    # printing a path of the solution if it exists
    def print(self):

        # If self.solution is not None, it extracts the solution path (assumed to be at index 1). Otherwise, solution is set to None.
        solution = self.solution[1] if self.solution is not None else None

        print() # used to create a blank line


        # The outer loop iterates through each row in self.walls, with i as the row index and row as the row itself.
        # The inner loop iterates through each column in the current row, with j as the column index and col as the cell value (either True or False).
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # If col is True, it means the cell is a wall, so it prints "$".
                if col :
                    print("$", end="") 
                # specifying end="" changes this behavior to not add a newline at the end of each print call.


                # If the current position (i, j) matches self.start, it prints "A".
                elif (i, j) == self.start: 
                    print ("A", end="")


                elif (i, j) == self.goal:
                    print ("B", end="")


                #  If a solution exists and the current position (i, j) is part of the solution path, it prints "*"
                elif solution is not None and (i, j) in solution:
                    print ("*", end="")


                # for all other open spaces
                else :
                    print(" ", end="")
            print()
        print()

        # BASICALLY
        # "$" for walls
        # "A" for the start position
        # "B" for the goal position
        # "*" for the solution path (if it exists)
        # " " for open spaces     

    def neighbors(self, state):
        row, col = state # state is a tuple. Tuple unpacking


        # A list of tuples representing the possible movements ("up", "down", "left", "right") and their corresponding new positions after the movement.
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))

        ]


        # ENSURE actions are valid

        # The function initializes an empty list result to store valid moves.
        result = [] 
        for action, (r, c) in candidates: # candidates is the list right above we made
            try :
                # For each candidate move, it checks whether the new position (r, c) is within the bounds of the grid and not blocked by a wall.
                if not self.walls[r][c]:

                    result.append((action, (r, c))) # If the new position (r, c) is valid (i.e., not blocked by a wall and within bounds), the move is appended to the result list as a tuple of action and (r, c).
            
            # If the move results in an out-of-bounds position, it will raise an IndexError
            except IndexError:
                continue

        return result # the list of valid moves
    

    def solve(self):
        # finds a solution to maze, if it exists.

        # keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        # node represents start state
        start = Node(state =self.start, parent =None, action =None) 
        frontier = StackFrontier()
        frontier.add(start) # initially it only contains the start state


        # initialize an empty explored set
        self.explored = set()


        # keeping loop until solution is found
        while True:

            # if frontier is empty, then no solution
            if frontier.empty():
                raise Exception("No Solution")
            

            # choose a node from the frontier 
            node = frontier.remove()
            # adding 1 to the number of states explored
            self.num_explored += 1

            # if node is the goal, then we have a solution 
            if node.state == self.goal:
                actions = []
                cells = []


                # follow parent nodes to find the solution 
                # while loop ends when initial state is reached, which has NO parent, hence the node.parent is not None
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                # we reverse it cause we have backtracked the path, but we need path from start to end not end to start
                actions.reverse()
                cells.reverse()

                self.solution = (actions, cells)
                return
            
            # mark the node as explored
            # if the state is not the goal
            self.explored.add(node.state)


            # add neighbors to frontier
            for action, state in self.neighbors(node.state):

                # checking if state is already in frontier and state is already in explored
                # if NOT, then we will add this new child to the frontier
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

                
    def output_image(self, filename, show_solution = True, show_explored = False):
        # PIL is Python Imaging Library
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2


        # create a blank canvas 
        img = Image.new(
            "RGBA", # mode

            # The width of the image is calculated by multiplying the number of columns (self.width) by the size of each cell (cell_size). Same for height
            (self.width * cell_size, self.height * cell_size),

            "black" # background color
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col: 
                    fill = (40, 40, 40) # this is the color (dark grey here)

                
                # start
                elif (i, j) == self.start:
                    fill = (255, 0, 0) # start cell is filled with red
                            
                            
                # GOAL 
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.solution:
                    fill = (212, 97, 85)

                # Empty cell
                else :
                    fill = (237, 240, 252)

                # draw cell
                # draw rectangle draws a rectangle representing each cell
                draw.rectangle(
                [ # this is some calculation about the top left and bottom right corners
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)
                ],
                    fill=fill
                )

        
        # saves generated image to filename
        img.save(filename)


# sys.argv is a list in Python that contains command-line arguments passed to the script.
# len(sys.argv) != 2 checks if there is exactly ONE command-line argument in addition to the script name itself.
if len(sys.argv) != 2:
    sys.exit("Usage : python maze.py maze.txt")

m = Maze(sys.argv[1]) # creating Maze object
print("Maze : ")

m.print() # Calls the print method of the Maze object (m) to print the maze.
print("Solving ...")
m.solve()
print("Status Explored :", m.num_explored) #  Prints the number of cells explored during the solving process
print("Solution : ")
m.print()
m.output_image("maze.png", show_explored=True) # calls output image function and saves image file as maze.png


# /usr/local/bin/python3 /Users/adityapc/Desktop/Coding/maze.py /Users/adityapc/Desktop/Coding/maze.txt





        


