import importDict
from inputPuzzle import inputPuzzle
import Clue
import strategy
from output import toHTML
import ai
import textdictionary as td
import outputSteps
from model_pylist import model
from threading import Thread
from beautifulThreads import scrapeDictionDotCom, scrapeCrossNexus

def main(PUZZ, puzType, model):

   #cwe = importDict.importCSV("crosswordese.csv")
   aClues, dClues, puzzle = inputPuzzle(PUZZ)

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
        threads = []
        processB = Thread(target=strategy.getSyns, args=[aClues, puzzle, 'web', 'cn'])
        processC= Thread(target=strategy.getSyns, args=[dClues, puzzle, 'web', 'cn'])
        processB.start()
        processC.start()
        threads.append(processB)
        threads.append(processC)

        for clue in clues:
            processA = Thread(target=scrapeDictionDotCom, args=[clue])
            processA.start()
            threads.append(processA)

        for process in threads:
            process.join()


   least= ai.findLeastConnected(clues, puzzle)

   G = ai.GraphTree(least[0], puzzle)
   G.findAllArcs(clues)


   status, stepArray = G.traverse(clues,puzzle)
   if status == 1:
      for i in range(0, len(clues)):
         tempR = clues[i]
         #print("clue removed: ", tempR.name)
         clues.remove(tempR)
         least = ai.findLeastConnected(clues, puzzle)
         R = ai.GraphTree(least[0], puzzle)
         R.findAllArcs(clues)
         status, stepArray = R.traverse(clues, puzzle)
         if status == 0:
            break
         clues.insert(i, tempR)
   #puzzle.print()

   if strategy.checkDone == 1:
      return "I'm sorry, this puzzle is unsolvable with our current database"

   model.insert(stepArray, "stepArray", PUZZ)
   ## for stepArray output:
   #S = outputSteps.toHTML(stepArray)
   #return S, None

   ## for normal output:
   S = toHTML(puzzle, "Solved Puzzle: ", PUZZ, aClues, dClues, puzType)
   return S