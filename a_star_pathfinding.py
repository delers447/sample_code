from tkinter import*
import math, random, time

grid_size = 30
cell_size = 5
canvas_width, canvas_height = (grid_size + 2) * cell_size, (grid_size + 2) * cell_size

root = Tk()
root.geometry(f"{canvas_width}x{canvas_height}")

class cell:
    def __init__(self, canvas, index):
        self.canvas = canvas
        self.index = index
        color_choices = ['white', 'white', 'white', 'black']
        self.color = random.choice(color_choices)
        self.f =  9999999999.0 #combined values of h and g. f = g + h
        self.h = 0.0  #heristical value
        self.g = 0.0 #path travel value
        self.parent = [0,0]
        self.rect = True

    def draw_cell(self):
        x0, y0 = (self.index[0] + 1) * cell_size, (self.index[1] + 1) * cell_size
        x1, y1 = x0 + cell_size, y0 + cell_size
        self.rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.color, width=0)

    def set_h(self):
        x0, y0 = self.index[0], self.index[1]
        x1, y1 = grid_size-1, grid_size-1
        self.h = math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
        print(self.h)

    def set_g(self, maze):
        self.g = maze[self.parent[0]][self.parent[1]].g + 1.0

    def set_f(self):
        print(self.h)
        self.f = float(self.g) + self.h

    def set_parent(self, parent):
        self.parent = parent

    def report_f(self):
        return self.f

    def test_better_g(self, maze, current_cell):
        # test if using the current G score make the aSquare F score lower, if yes update the parent because it means its a better path
        #print("I am testing a better G.")
        current_g = self.g
        potential_g = maze[current_cell[0]][current_cell[1]].g + 1.0
        print(f"Gs: {potential_g} and {current_g}")
        if potential_g < current_g:
            return True
        else: False

    def paint_parent(self, maze):
        print("painting yellow")
        if self.parent == [0,0]:
            self.color = 'yellow'
            return
        self.color = 'yellow'
        if self.index == [grid_size-1, grid_size-1]:
            self.color = 'red'
        #self.canvas.itemconfig(maze[self.parent[0]][self.parent[1]].rect, fill='yellow')
        maze[self.parent[0]][self.parent[1]].paint_parent(maze)

    def report_for_debugging(self):
        print(f"For cell[{self.index[0]}][{self.index[1]}]:")
        print(f"    f:{type(self.f)}")
        print(f"    g:{type(self.g)}")
        print(f"    h:{type(self.h)}")
        print(f"    f({self.f}) = g({self.g}) + h({self.h})")

def make_maze(canvas):
    #matrix = [[0 for i in range(5)] for i in range(5)]
    maze = [[cell(canvas, [i, j]) for j in range(grid_size)] for i in range(grid_size)]
    maze[0][0].color = 'green'
    maze[0][0].f = 0.0
    maze[grid_size-1][grid_size-1].color = 'red'
    for i in range(grid_size):
        for j in range(grid_size):
            maze[i][j].set_h()
    return maze

def draw_maze(maze):
    for i in range(grid_size):
        for j in range(grid_size):
            #print(f"{i}, {j}")
            maze[i][j].draw_cell()

def get_neighbors(maze, current):
    x, y = current[0], current[1]
    neighbors = []

    try:
        #print(f"left: {maze[x-1][y].color}")
        if x > 0 and maze[x-1][y].color != 'black': #check left
            neighbors.append([x-1, y])
            #print("There is a neighbor to the left.")

        #print(f"right: {maze[x+1][y].color}")
        if x < grid_size-1 and maze[x+1][y].color != 'black': #check right
            neighbors.append([x+1, y])
            #print("There is a neighbor to the right.")

        #print(f"up: {maze[x][y-1].color}")
        if y > 0 and maze[x][y-1].color != 'black': #check up
            neighbors.append([x, y-1])
            #print("There is a neighbor upwards.")

        #print(f"down: {maze[x][y+1].color}")
        if y < grid_size-1 and maze[x][y+1].color != 'black': #check down
            neighbors.append([x, y+1])
            #print("There is a neighbor downards.")
    except:
        pass
    if len(neighbors) is 0:
        print("NO NEIGHBORS")
    return neighbors

def lowest_f(maze, listed):
    # return the cell that has the lowest f value.
    for element in listed:
        print(f"One of the Opened List: [{element[0]}][{[element[1]]}]:{maze[element[0]][element[1]].f}")
    lowest = listed[0]
    for element in listed:
        if maze[element[0]][element[1]].report_f() < maze[lowest[0]][lowest[1]].report_f():
            lowest = element
    print(f"Lowest: [{lowest[0]}][{[lowest[1]]}]:{maze[lowest[0]][lowest[1]].report_f()}")
    return lowest

def check_ending(maze, closed_list):
    for cell in closed_list:
        if maze[cell[0]][cell[1]].color == 'red':
            return True
    return False

def a_star(maze):
    open_list = list()
    closed_list = list()
    open_list.append([0,0])
    counter = 0
    while open_list:
        counter += 1
        current_cell = lowest_f(maze, open_list)
        maze[current_cell[0]][current_cell[1]].color = 'lightgreen'
        print(f"Next Cell in A*.  Counter:{counter}, len of open:{len(open_list)}. Current: [{current_cell[0]}][{current_cell[1]}] Color:{maze[current_cell[0]][current_cell[1]].color}")
        open_list.remove(current_cell)
        closed_list.append(current_cell)
        if current_cell == [grid_size-1, grid_size-1]:
            print("A path was found.")
            maze[current_cell[0]][current_cell[1]].paint_parent(maze)
            break
        adjacent_cells = get_neighbors(maze, current_cell)
        for neighbor in adjacent_cells:
            if maze[neighbor[0]][neighbor[1]].color != 'lightgreen':
                maze[neighbor[0]][neighbor[1]].color = 'lightblue'
            if neighbor in closed_list:
                continue
            if neighbor not in open_list: #compute its f score, set the parent, add to the open list(done)
                maze[neighbor[0]][neighbor[1]].set_parent(current_cell)
                maze[neighbor[0]][neighbor[1]].set_g(maze)
                maze[neighbor[0]][neighbor[1]].set_f()
                open_list.append(neighbor)
            else: # test if using the current G score make the aSquare F score lower, if yes update the parent because it means its a better path
                if maze[neighbor[0]][neighbor[1]].test_better_g(maze, current_cell): #need to write this function
                    maze[neighbor[0]][neighbor[1]].set_parent(current_cell)
                    print('-'*10 + "I found a better way!" + '-'*10) #this shit is bugged.
    print("No Path Found.")
    return maze

def main():
    canvas = Canvas(root, height=canvas_height, width=canvas_width, bg="grey")
    canvas.pack()

    maze = make_maze(canvas)
    #maze[0][1].color='blue'

    a_star(maze)
    maze[0][0].color = 'green'
    draw_maze(maze)

    #for i in range(grid_size):
    #    for j in range(grid_size):
    #        maze[i][j].report_for_debugging()

    while True:
        root.update_idletasks()
        root.update()
        time.sleep(.01)

main()
