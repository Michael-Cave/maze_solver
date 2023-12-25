from tkinter import Tk, BOTH, Canvas
import time
import random

# Class definition for the window itself
class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running == True:
            self.redraw()

    def close(self):
        self.__running = False
        print("window closed...")

    def draw_line(self, Line, fill_color):
        Line.draw(self.__canvas, fill_color)


# Point Class
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

# Line Class
class Line:
    def __init__(self, point_1, point_2):
        self.point1 = point_1
        self.point2 = point_2
        self.line = None

    def draw(self, Canvas, fill_color):
        self.line = Canvas.create_line(self.point1._x, self.point1._y, self.point2._x, self.point2._y, fill=fill_color, width=2)
        Canvas.pack(fill=BOTH, expand=1)

# Cell Class
class Cell:
    def __init__(self, x1, x2, y1, y2, win=None):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.visited = False

        # Wall bools
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        # Corner Points
        self.top_left = Point(self._x1, self._y1)
        self.top_right = Point(self._x2, self._y1)
        self.bottom_left = Point(self._x1, self._y2)
        self.bottom_right = Point(self._x2, self._y2)

        # Cell Mid Point
        self.mid_x = (self._x1 + self._x2) / 2
        self.mid_y = (self._y1 + self._y2) / 2
        self.mid_point = Point(self.mid_x, self.mid_y)

    # Draws the walls of the cells
    def draw(self):
        # Left wall status
        if self.has_left_wall is True:
            left_wall = Line(self.top_left, self.bottom_left)
            self._win.draw_line(left_wall, "black")
        elif self.has_left_wall is False:
            left_wall = Line(self.top_left, self.bottom_left)
            self._win.draw_line(left_wall, "white")
        # Top wall status
        if self.has_top_wall is True:
            top_wall = Line(self.top_left, self.top_right)
            self._win.draw_line(top_wall, "black")
        elif self.has_top_wall is False:
            top_wall = Line(self.top_left, self.top_right)
            self._win.draw_line(top_wall, "white")
        # Right wall status
        if self.has_right_wall is True:
            right_wall = Line(self.top_right, self.bottom_right)
            self._win.draw_line(right_wall, "black")
        elif self.has_right_wall is False:
            right_wall = Line(self.top_right, self.bottom_right)
            self._win.draw_line(right_wall, "white")
        # Bottom wall status
        if self.has_bottom_wall is True:
            bottom_wall = Line(self.bottom_left, self.bottom_right)
            self._win.draw_line(bottom_wall, "black")
        elif self.has_bottom_wall is False:
            bottom_wall = Line(self.bottom_left, self.bottom_right)
            self._win.draw_line(bottom_wall, "white")

    # Draws the path through the maze
    def draw_move(self, to_cell, undo=False):
        if not undo:
            red_line = Line(self.mid_point, to_cell.mid_point)
            self._win.draw_line(red_line, "red")
        else :
            grey_line = Line(self.mid_point, to_cell.mid_point)
            self._win.draw_line(grey_line, "grey")


# Maze Class
class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed
        self._cells = []
        self._create_cells()
        if self._seed != None:
            random.seed(self._seed)

    def _create_cells(self):
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                cell_x1 = self._x1 + i * self._cell_size_x
                cell_x2 = cell_x1 + self._cell_size_x
                cell_y1 = self._y1 + j * self._cell_size_y
                cell_y2 = cell_y1 + self._cell_size_y

                cell = Cell(cell_x1, cell_x2, cell_y1, cell_y2, self._win)
                column.append(cell)
            self._cells.append(column)
        for i, column in enumerate(self._cells):
            for j, cell in enumerate(column):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        cell_x = self._x1 + i * self._cell_size_x
        cell_y = self._y1 + j * self._cell_size_y
        cell = self._cells[i][j]
        cell.draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        entrance_cell.draw()
        exit_cell = self._cells[-1][-1]
        exit_cell.has_bottom_wall = False
        exit_cell.draw()
        self._animate()
    
    # Breaks cell walls to construct the maze itself
    def _break_walls_r(self, i, j):
        

        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        random.shuffle(directions)


        for di, dj in directions:
            next_i, next_j = i + di, j + dj

            if (
                0 <= next_i < len(self._cells) and
                0 <= next_j < len(self._cells[i]) and
                not self._cells[next_i][next_j].visited
            ):
                # Determines the walls to knock down and removes them
                if dj == -1:
                    # The next Cell is above
                    if next_i == 0:
                        self._cells[next_i][next_j].has_top_wall = True
                    self._cells[i][j].has_top_wall = False
                    self._cells[next_i][next_j].has_bottom_wall = False
                elif dj == 1:
                    # The next Cell is below
                    if next_i == len(self._cells) - 1:
                        self._cells[next_i][next_j].has_bottom_wall = True
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[next_i][next_j].has_top_wall = False
                elif di == -1:
                    # The next Cell is to the left
                    if next_j == 0:
                        self._cells[next_i][next_j].has_left_wall = True
                    self._cells[i][j].has_left_wall = False
                    self._cells[next_i][next_j].has_right_wall = False
                elif di == 1:
                    # The next Cell is to the right
                    if next_j == len(self._cells[i]) - 1:
                        self._cells[next_i][next_j].has_right_wall = True
                    self._cells[i][j].has_right_wall = False
                    self._cells[next_i][next_j].has_left_wall = False
                # Recursively moves to the next cell
                self._cells[i][j].visited = True
                self._break_walls_r(next_i, next_j)
            
        self._cells[i][j].draw()
        self._animate()
    
    # Resets the visited property for future use
    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    # Returns the solved state of the Maze
    def solve(self):
        result = self._solve_r(0, 0)
        return result
    
    # Attempts to solve the Maze
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if self._cells[i][j] == self._cells[-1][-1]:
            return True
        
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

        for di, dj in directions:
            next_i, next_j = i + di, j + dj


            if 0 <= next_i < self._num_cols and 0 <= next_j < self._num_rows:
                
                # Debugging if the next cell has been visited
                visited_value = self._cells[next_i][next_j].visited
                if self._cells[next_i][next_j].visited == False:
                    if dj == -1:
                        # The next Cell is above
                        if not self._cells[i][j].has_top_wall and not self._cells[next_i][next_j].has_bottom_wall:
                            self._cells[i][j].draw_move(self._cells[next_i][next_j])

                            if self._solve_r(next_i, next_j):
                                return True
                            else :
                                self._cells[i][j].draw_move(self._cells[next_i][next_j], True)
                    elif dj == 1:
                        # The next Cell is below
                        if not self._cells[i][j].has_bottom_wall and not self._cells[next_i][next_j].has_top_wall:
                            self._cells[i][j].draw_move(self._cells[next_i][next_j])

                            if self._solve_r(next_i, next_j):
                                return True
                            else :
                                self._cells[i][j].draw_move(self._cells[next_i][next_j], True)
                    elif di == -1:
                        # The next Cell is to the left
                        if not self._cells[i][j].has_left_wall and not self._cells[next_i][next_j].has_right_wall:
                            self._cells[i][j].draw_move(self._cells[next_i][next_j])

                            if self._solve_r(next_i, next_j):
                                return True
                            else :
                                self._cells[i][j].draw_move(self._cells[next_i][next_j], True)
                    elif di == 1:
                        # The next Cell is to the right
                        if not self._cells[i][j].has_right_wall and not self._cells[next_i][next_j].has_left_wall:
                            self._cells[i][j].draw_move(self._cells[next_i][next_j])

                            if self._solve_r(next_i, next_j):
                                return True
                            else :
                                self._cells[i][j].draw_move(self._cells[next_i][next_j], True)

        return False


# Main function
def main():
    win = Window(800, 600)
    num_cols = 12
    num_rows = 10
    m1 = Maze(20, 20, num_rows, num_cols, 50, 50, win, 10)
    for i in range(0, num_cols):
        for j in range(0, num_rows):
            m1._break_walls_r(i, j)
    m1._break_entrance_and_exit()
    m1._reset_cells_visited()
    m1.solve()
    win.wait_for_close()

main()