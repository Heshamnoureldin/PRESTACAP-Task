import heapq
from pylab import *

#The basic object here is a cell so we write a class for it.
#We store the coordinates x and y, the values of G and H plus the sum F.
#reachable is cell reachable? not a wall?
class Cell(object):
      def __init__(self, x, y, reachable):
         #initialize new cell
          self.reachable = reachable
          self.x = x
          self.y = y
          self.parent = None
          self.g = 0
          self.h = 0
          self.f = 0
      def __lt__(self,other):
          return(self.f <other.f)

#Next is Our Main Class Named AStar. Attributes are the Open List Heapified (Keep Cell With Lowest F at the Top)
#The Closed List Which is a Set For Fast Lookup,
#The Cells List (Grid Definition) and the Size of The Grid
#This Class Contains All Methods Needed for  A Star Alogrithm
class AStar(object):
      def __init__(self):
          # Open List (List of Cells that Need to be Checked)
          self.opened = []
	  # Here We Will Put Children Cells in the Priority Queue (Keep Cell With Lowest F at the Top-->The Highest Priority)
          heapq.heapify(self.opened) 
          # Closed List (List of Cells that Have Been Checked ).
          self.closed=set()
          # Grid Cells
          self.cells =[]
          # Grid Height
          self.grid_height = None
	  # Grid Width
          self.grid_width  = None

      # Prepare Grid Cells & Walls. 
      def init_grid(self, width, height, walls, start, end):
          # Walls are List of Obstacles x,y Tuples.
          # Start is Starting Point x,y Tuple.
          # End is Ending Point x,y Tuple. 
          self.grid_height = height
          self.grid_width = width
          # These Two Loops to Indicate Obstacles Positions in the Grid
          for x in range(self.grid_width):
              for y in range(self.grid_height):
                  if (x, y) in walls:
                      reachable = False
                  else:
                      reachable = True
                  # The Next Line Decide Any Cell In The Grid Whether Is Reachable Or Not(Obstacle)
                  self.cells.append(Cell(x, y, reachable))
          self.start = self.get_cell(*start)
          self.end = self.get_cell(*end)
      
      # Compute The Heuristic Value (H Value) For a Cell -> Distance Between This Cell and The Ending Cell Multiplied By 10.
      def get_heuristic(self, cell):
          # Cell is The Point that I Want to Check
          # Cell.End is Tuple of End Point(x,Y)   
          return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))


      # Returns a Cell From the Cells List
      def get_cell(self, x, y):
           return self.cells[x * self.grid_height + y]

      # Returns Adjacent Cells (Child Cells) to a Cell (Parent Cell).
      def get_adjacent_cells(self, cell):
           cells = []
           if cell.x < self.grid_width-1:
              cells.append(self.get_cell(cell.x+1, cell.y))
           if cell.y > 0:
              cells.append(self.get_cell(cell.x, cell.y-1))
           if cell.x > 0:
              cells.append(self.get_cell(cell.x-1, cell.y))
           if cell.y < self.grid_height-1:
              cells.append(self.get_cell(cell.x, cell.y+1))
           return cells

      # Simple Method To Print The Path Found as points ,It Follows The Parent Pointers To Go From The Ending Cell to The Starting Cell.
      def display_path(self):
           cell = self.end
           path = [(cell.x, cell.y)]
           while cell.parent is not self.start:
                 cell = cell.parent
                 path.append((cell.x, cell.y))
           path.append((self.start.x, self.start.y))
           path.reverse()
           Path_Directions = self.Get_Directions(path)
           return (Path_Directions)

      # Simple Method To Print The Path Found as Directions ,It Follows The Parent Pointers To Go From The Ending Cell to The Starting Cell.
      def Get_Directions(self,path):
            length = len(path)
            new_path =[]
            for k in range(0,length-1):
                        if(path[k+1][0]-path[k][0] == 1):
                              new_path.append('DOWN')
                        elif (path[k+1][0]-path[k][0] == -1):
                              new_path.append('UP')
                        elif (path[k+1][1]-path[k][1] == 1):
                             new_path.append('RIGHT')
                        elif (path[k+1][1]-path[k][1] == -1):
                             new_path.append('LEFT')
            return(tuple(new_path))
                  
       #Update adjacent cell with G and H
      def update_cell(self, adj, cell):
           #adj is adjacent cell to current cell
           #cell is current cell being processed
          adj.g = cell.g + 10
          adj.h = self.get_heuristic(adj)
          adj.parent = cell #dh msh fahm bi3ml a
          adj.f = adj.h + adj.g
          
       #The main method implements the algorithm itself(Astar alogrithm)
       #find path to ending cell.
       #returns path or None if not found.    
      def process(self):
           # add starting cell to open heap queue
           heapq.heappush(self.opened, (self.start.f, self.start))
           while len(self.opened):
                 # pop cell from heap queue
                 f, cell = heapq.heappop(self.opened)
                 # add cell to closed list so we don't process it twice
                 self.closed.add(cell)
                 # if ending cell, display found path
                 if cell is self.end:
                    return (self.display_path())
                    break
                 # get adjacent cells for cell
                 adj_cells = self.get_adjacent_cells(cell)
                 for adj_cell in adj_cells:
                     if adj_cell.reachable and adj_cell not in self.closed:
                        if (adj_cell.f, adj_cell) in self.opened:
                           # if adj cell in open list, check if current path is
                           # better than the one previously found for this adj cell.
                           if adj_cell.g > cell.g + 10:
                              self.update_cell(adj_cell, cell)
                        else:
                             self.update_cell(adj_cell, cell)
	                     # add adj cell to open list
                             heapq.heappush(self.opened, (adj_cell.f, adj_cell))


      





