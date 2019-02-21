import Clue

def inputPuzzle(puzzleFile):
   #gets across and down clues and puts into list of number/clue pairs: [0] is num, [1] is clue
   #puts puzzle structure into a 2D array of 1's (empty) and 2's (black)
   aClues = list()
   dClues = list()
   puzzle = list()

   puzzleFile = puzzleFile.split('\n')
   size = int(puzzleFile[0])
   newPuzzle = list()
   for item in puzzleFile:
      item = str(item.replace("\r", ""))
      newPuzzle.append(item)
   puzzleFile = newPuzzle[2:]

   count = 0
   i = puzzleFile[count]

   while i != '':
      #print(i, 'across')
      c = i.split(':')
      name = c[0]+'a'
      name = Clue.Clue(c[1], c[0], 'across')
      aClues.append(name)
      count += 1
      i = puzzleFile[count]

   #print("done with across")
   count += 1
   i = puzzleFile[count]

   while i != '':
      #print(i, 'down')
      c = i.split(':')
      name = c[0]+'d'
      name = Clue.Clue(c[1], c[0], 'down')
      dClues.append(name)
      count += 1
      i = puzzleFile[count]

   #print("done with down")
   count += 1
   pad = [Clue.Cell(x, 0, '#') for x in range (0, size+2)]
   puzzle.append(pad)
   index = 0

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
   """
   puz = ""
   for i in range(0, size + 2):
      for j in range (0, size + 2):
        puz = puz + puzzle[i][j].value
   return puz
   """

   p = Clue.Puzzle(size, puzzle)
   #print(i, "done")
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

   return (aClues, dClues, p)