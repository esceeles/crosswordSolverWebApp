import copy
class Clue():
   def __init__(self, name, number, direction):
      self.name = name
      self.number = number
      self.direction = direction
      self.length = int()
      self.start = list()           #row, column.
      self.cells = list()              #list of cells in clue
      self.tree = None              #huffman tree of for compression
      self.syns =[]                       #right now list of syns as strings
      self.cmpSyns = list()                 #list of syns as bit stings. compressed baby!
      self.done = False                   #have we found this answer?
      self.xCells = list()                #cells that overlap with other clues
   def getLength(self, puzzle):
      x = self.start[0]
      y = self.start[1]
      current = puzzle.grid[y][x].value
      count = 0
      while current != '#':
         count += 1
         if self.direction == "down":
            y = y+1
         elif self.direction == "across":
            x = x+1
         else:
            print("ERROR GETTING LENGTH")
         current = puzzle.grid[y][x].value
      self.length = count
      #builds clue.cells
      for i in range(0, count):
         if self.direction == 'across':
            r, c = self.start[1], self.start[0]+i
            cell = puzzle.grid[r][c]
            cell.clues.append(self)
            self.cells.append(cell)
         elif self.direction == 'down':
            cell = puzzle.grid[self.start[1]+i][self.start[0]]
            cell.clues.append(self)
            self.cells.append(cell)
   def updateCells(self, puzzle):
      #x = self.start[0]
      #y = self.start[1]
      self.cells.clear()
      for i in range(0, self.length):
         if self.direction == 'across':
            r, c = self.start[1], self.start[0]+i
            cell = puzzle.grid[r][c]
            #print(cell)
            #cell.clues.append(self)
            self.cells.append(cell)
         elif self.direction == 'down':
            cell = puzzle.grid[self.start[1]+i][self.start[0]]
            #print(cell)
            #cell.clues.append(self)
            self.cells.append(cell)
      #print(self.cells)


   def print(self):                       #print everything
      print(self.number + " " + self.direction + ": " + self.name + ": " + str(self.length))
      #print(self.syns)
      print("\n")

#grid will be the puzzle passed in. update everything in main and inputPuzzle.py to reflect this. guess should be a pointer to each cell in here. ccell is pointer to clue it is reflected to?
class Puzzle():
   def __init__(self, n, g):
      self.size = n
      self.grid = g
      self.xCells = list()
      self.origGrid = copy.deepcopy(g)
   def print(self):
      for i in range(0, self.size+2):
         for j in range (0, self.size+2):
            print(self.grid[i][j].value, " ", end = '')
         print("\n")

class Cell():
   def __init__ (self, row, column, v):
      self.row = row
      self.column = column
      self.x = column
      self.y = row
      self.pos = row, column                 #gives down and then over coordinates
      self.value = v
      self.numClues = int(0)
      self.guesses = {}
      self.clues = list()
      self.valPlacedBy = None
