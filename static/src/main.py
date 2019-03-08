import importDict
from inputPuzzle import inputPuzzle
import Clue
import strategy
from output import toHTML
import ai
import textdictionary as td
import outputSteps
from threading import Thread
from beautifulThreads import scrapeDictionDotCom, scrapeCrossNexus

def main(PUZZ, puzType, m, n):
   m.puzString = PUZZ
   m.puzType = puzType
   puzzle = m.puzzle
   aClues = m.aClues
   dClues = m.dClues
   flag = False

   if puzType == "handle":
       flag = True
       puzType = "synonym"
       del m.puzzle
       del n.puzzle

   if puzzle is None:
       puzzle = n.puzzle
       m.puzzle = puzzle
       if puzzle is None:
            aClues, dClues, puzzle = inputPuzzle(PUZZ)
            if aClues == "Error":
                return "Sorry, there was a Fatal Error <br><a href ='/'>Please enter your puzzle again</a>", None
            m.puzzle = puzzle
            n.puzzle = puzzle
            m.aClues = aClues
            n.aClues = aClues
            m.dClues = dClues
            n.dClues = dClues

   clues = aClues + dClues

   #if a synonym puzzle, get guesses from dictionary
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

   #if "other" puzzle, get guesses from databases
   else:
        #uses threading to speed up API scraping
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

   #creates a graph using puzzle data with the root as the least connected clue
   G = ai.GraphTree(least[0], puzzle)
   G.findAllArcs(clues)

   if clues is None or puzzle is None or puzType is None:
      return "Sorry, there was a Fatal Error <br><a href ='/'>Please enter your puzzle again</a>", None

   #traverses the graph once to see if all guesses have been placed correctly

   allReturn = G.traverse(clues, puzzle, puzType)
   if len(allReturn) < 3:
       return "Sorry, there was a Fatal Error <br><a href ='/'>Please enter your puzzle again</a>", None
   status = allReturn[0]
   stepArray = allReturn[1]
   guessArray = allReturn[2]

   #if no correct placement is found, will try to solve puzzle leaving one word out
   #due to the intensely overlapped nature of puzzle, can still solve most with only one correct guess missing
   if status == 1:
      for i in range(0, len(clues)):
         tempR = clues[i]
         clues.remove(tempR)
         least = ai.findLeastConnected(clues, puzzle)
         R = ai.GraphTree(least[0], puzzle)
         R.findAllArcs(clues)
         status, stepArray, guessArray = R.traverse(clues, puzzle, puzType)
         if status == 0:
            break
         clues.insert(i, tempR)

   if strategy.checkDone == 1:
      return "I'm sorry, this puzzle is unsolvable with our current database"

   #adds step array to held object
   m.stepArray = stepArray
   n.stepArray = stepArray
   m.guessArray = guessArray
   n.guessArray = guessArray

   if flag == True:
       return stepArray, None

   S = toHTML(puzzle, "Solved Puzzle: ", PUZZ, aClues, dClues, puzType)
   return S



