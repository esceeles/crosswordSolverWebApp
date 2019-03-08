import Clue

#reads in the string puzzleFile and creates puzzle and clue objects
def inputPuzzle(puzzleFile):
   #gets across and down clues and puts into list of number/clue pairs: [0] is num, [1] is clue
   #puts puzzle structure into a 2D array of 1's (empty) and 2's (black)
   aClues = list()
   dClues = list()
   puzzle = list()

   puzzleFile = puzzleFile.split('\n')
   if not puzzleFile[0]:
       return "nothing", None, None
   if puzzleFile[0].isalpha():
       return "notNum", None, None
   size = int(puzzleFile[0])
   newPuzzle = list()
   for item in puzzleFile:
      item = str(item.replace("\r", ""))
      newPuzzle.append(item)
   puzzleFile = newPuzzle[2:]
   count = 0
   i = puzzleFile[count]

   #gets across clues
   while i != '':
      c = i.split(':')
      name = c[0]+'a'
      name = Clue.Clue(c[1], c[0], 'across')
      aClues.append(name)
      count += 1
      try:
        i = puzzleFile[count]
      except IndexError:
          return "Error", None, None

   count += 1
   i = puzzleFile[count]

   #gets down clues
   while i != '':
      #print(i, 'down')
      c = i.split(':')
      name = c[0]+'d'
      name = Clue.Clue(c[1], c[0], 'down')
      dClues.append(name)
      count += 1
      i = puzzleFile[count]

   count += 1

   #creates a padding for easily knowing when we reach the puzzle boundaries
   pad = [Clue.Cell(x, 0, '#') for x in range (0, size+2)]
   puzzle.append(pad)

   #gathers grid information
   for y in range(0, size):
      i = puzzleFile[count]
      i = '# ' +i+ ' #'
      i = i.split(' ')
      d = list()
      for rdx, c in enumerate(i):
         cell = Clue.Cell(y+1, rdx, c)
         d.append(cell)
      puzzle.append(d)
      count += 1

   pad = [Clue.Cell(0, i, '#') for i in range (0, size+2)]

   puzzle.append(pad)

   p = Clue.Puzzle(size, puzzle)

   #uses clue and puzzle information to infer the lengths and cell objects for each clue
   for i in aClues:
      for y in range(0, p.size+2):
         for x in range(0, p.size+2):
            if p.grid[y][x].value == i.number:
               i.start = (int(x), int(y))
               i.getLength(p)
      for j in i.cells:
         row = j.row
         column = j.column
         p.grid[row][column].numClues += 1

   for i in dClues:
      for y in range(0, p.size+2):
         for x in range(0, p.size+2):
            if p.grid[y][x].value == i.number:
               i.start = (int(x), int(y))
               i.getLength(p)
      for j in i.cells:
         row = j.row
         column = j.column
         p.grid[row][column].numClues += 1

   #makes list of intersecting cells for each clue and for puzzle in total
   for i in p.grid:
      for j in i:
         if j.numClues > 1:
            for clue in j.clues:
               clue.xCells.append(j)
               p.xCells.append(j)

   #check that the board and numbers for clues all align
   for clue in aClues + dClues:
      num = str(clue.number)
      Found = False
      for i in range (0, p.size+2):
          for j in range (0, p.size+2):
              if p.grid[i][j].value == num:
                  Found = True
      if Found == False:
          return "missing", None, None

   return (aClues, dClues, p)