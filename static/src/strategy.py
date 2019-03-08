import copy
from itertools import combinations
import beautiful

#pulls in synonyms of the right size
def getSyns(clues, puzzle, dictionary, form):
   #gets guesses from thesaurus file and cwe that are the same length as grid. l = aur. d = csv
   if form == 'l':                  #get syns from moby thesaurus list
      for i in clues:
         for x in dictionary:
            if i.name in x:
               for item in x:
                  item = item.replace(" ", "").replace("-", "").replace("_","").lower()
                  if len(item) == i.length and item not in i.syns:
                     i.syns.append(item)

   elif form == 'd':             #get syns from csv syn list
      for i in clues:
         if i.name in dictionary:
            for syn in dictionary[i.name]:
                syn = syn.replace(" ", "").replace("-", "").replace("_", "").lower()
                if len(syn) == i.length and syn not in i.syns:
                    i.syns.append(syn)


   elif form == 'c':             #get answers from crosswordese dictionary
      for i in clues:
         if i.name in dictionary:                #is this working correctly?
            for syn in dictionary[i.name]:
               syn = syn.replace(" ", "").replace("-", "").replace("_","").lower()
               if len(syn) == i.length and syn not in i.syns:
                  i.syns.append(syn)

   elif form == 's':
        for i in clues:
            x = beautiful.scrapeDictionDotCom(i)
            for y in x:
                if len(y) == i.length and y not in i.syns:
                    i.syns.append(y)
   elif form == 'cn':
        for i in clues:
            x = beautiful.scrapeCrossNexus(i)
            for y in x:
                if len(y) == i.length and y not in i.syns:
                    i.syns.append(y)

   #for i in clues:
      #i.syns.sort(key = str.lower, reverse = True)
      #i.syns.sort(key = str.lower)


#inserts a word into a puzzle and marks the clue as done. if word conflicts with already placed guess, return 0
def insertWord(clue, guess, puzzle):
   for idx in range(0, clue.length):            #first check fo no conflict
      y, x = clue.cells[idx].pos
      if puzzle.grid[y][x].value.isalpha() and puzzle.grid[y][x].value != guess[idx]:
         return 1
   for idx in range(0, clue.length):            #if no conflict, insert word chars
      y, x = clue.cells[idx].pos
      if not puzzle.grid[y][x].value.isalpha():
         c = clue.cells[idx]
         c.valPlacedBy = clue
      puzzle.grid[y][x].value = guess[idx]
   clue.done = True
   return 0

def removeWord(clue, puzzle):
   clue.done = False
   for idx in range(0, clue.length):
      cell = clue.cells[idx]
      y, x = clue.cells[idx].pos
      if cell.numClues == 1:
         puzzle.grid[y][x].value = puzzle.origGrid[y][x].value
         cell.valPlacedBy = None
      elif cell.numClues == 2:
         canRemove = 'Yes'
         for i in cell.clues:
            if i.done == True:
               canRemove = 'No'
         if canRemove == 'Yes':
            puzzle.grid[y][x].value = puzzle.origGrid[y][x].value
            cell.valPlacedBy = None
   clue.done = False
   return 1

#if there is one left, it inserts it
def oneLeft(clues, puzzle):
   for i in clues:
      if len(i.syns) == 1:
         insertWord(i, i.syns[0], puzzle)

#compares chars with already placed letters. If the words don't match up, it deletes them
def compareChars(clues, puzzle):
   removeList = []
   for clue in clues:                    #for each clue, look at it
      for idx, c in enumerate(clue.cells):      #look at each char in the guess that is already placed
         for syn in clue.syns:                    #go through synonym list and
            if c.value.isalpha() and syn[idx] != c.value:                     #if synonym chars dont match guess chars, delete it
               removeList.append(syn)
      for i in removeList:
         if i in clue.syns:
            clue.syns.remove(i)
      removeList.clear()

#looks at all cells in clue and checks to see if all empty cells are isolated and thus can be filled with whatever syn/s are left
def checkIsolated(clue, puzzle):
   isolated = True
   for cell in clue.cells:
      if not cell.value.isalpha() and cell.numClues > 1:
         isolated = False
   return isolated

#calls combine to make list of all combinations of words remaining. then one at ta time inserts them piece by piece until one fits
def combinatoricExplosion(clues, puzzle):
   copyRemaining = list()
   realRemaining = list()
   for i in clues:
      if i.done == False:
         x = copy.deepcopy(i)
         copyRemaining.append(x)
         realRemaining.append(i)

   match = {}
   iterations = len(copyRemaining)
   combinations = []
   accum = list()
   combine(copyRemaining, puzzle, iterations, accum, combinations)
   for i in range(len(combinations)):
      temp = copy.deepcopy(puzzle)
      l = 0
      while l < len(combinations[i]) and (insertWord(copyRemaining[l], combinations[i][l], temp) != 0):
         l += 1
      if l == len(combinations[i]):
         for x in range(len(copyRemaining)):
            realRemaining[x].syns = [combinations[i][x]]
         oneLeft(clues, puzzle)
         return 0

#cited: user: duanev on stackOverflow
def combine(copyRemaining, puzzle, iterations, accum, combinations):
   last = (len(copyRemaining) == 1)
   n = len(copyRemaining[0].syns)
   for i in range (n):
      item = accum.copy()
      item.append(copyRemaining[0].syns[i])
      if last:
         combinations.append(item)
      else:
         combine(copyRemaining[1:], puzzle, iterations, item, combinations)


def checkDone(clues, puzzle):
#checking if done and showing whats left
   finished = True
   for i, row in enumerate(puzzle.grid):
      for j, column in enumerate(row):
         if puzzle.grid[i][j].value.isdigit() or puzzle.grid[i][j].value == '_':
            finished = False
   if finished == True:
      print("By George you've got it!")
      print("Completed Puzzle: ")
      puzzle.print()
      return 0
   else:
      print("We've still got some work to do.")

   return 1

#prints all clues that aren't done
def printRemainders(clues, puzzle):
   puzzle.print()
#printing leftover clues
   for i in clues:
      if i.done == False:
         i.print()