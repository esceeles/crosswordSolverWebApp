import importDict
from inputPuzzle import inputPuzzle
import Clue
import strategy
from output import toHTML
import ai
import textdictionary as td

def main(PUZZ, puzType):

   #cwe = importDict.importCSV("crosswordese.csv")
   aClues, dClues, puzzle = inputPuzzle(PUZZ)
   #thing = inputPuzzle(PUZZ)
   #return thing
   clues = aClues + dClues
   #strategy.getSyns(clues, puzzle, cwe, 'c')          #always imports CWE dictionary
   if puzType == "synonym":
        dictionary = td.dictionary         #moby thes saved as python dict variable. 'd' for getSyns. doesn't have everything as key

        strategy.getSyns(clues, puzzle, dictionary, 'd')           #d for dictionary/csv file, l for list the moby thesaurus

        inNeed = list()                              #pulls in list type syns if there were no matches from dictionary
        for i in clues:
            if len(i.syns) == 0:
                inNeed.append(i)

        mobyPath = "/home/esceeles/mysite/mobythes.aur"
        dictionary = importDict.importAUR(mobyPath)
        strategy.getSyns(inNeed, puzzle, dictionary, 'l')

   else:
         strategy.getSyns(clues, puzzle, 'web', 'cn')
         strategy.getSyns(clues, puzzle, 'web', 's')


   least= ai.findLeastConnected(clues, puzzle)

   G = ai.GraphTree(least[0], puzzle)
   G.findAllArcs(clues)


   if G.traverse(clues,puzzle) == 1:
      for i in range(0, len(clues)):
         tempR = clues[i]
         #print("clue removed: ", tempR.name)
         clues.remove(tempR)
         least = ai.findLeastConnected(clues, puzzle)
         R = ai.GraphTree(least[0], puzzle)
         R.findAllArcs(clues)
         if R.traverse(clues, puzzle) == 0:
            break
         clues.insert(i, tempR)
   #puzzle.print()

   if strategy.checkDone == 1:
      return "I'm sorry, this puzzle is unsolvable with our current database"
   puz = ""
   for i in range(0, puzzle.size+2):
       for j in range(0, puzzle.size+2):
           puz = puz + puzzle.grid[i][j].value
   #return puz

   S = toHTML(puzzle, "Solved Puzzle: ", PUZZ, aClues, dClues, puzType)
   return S