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
from importDict import RegexDict

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

        for clue in clues:
            processA = Thread(target=scrapeDictionDotCom, args=[clue])
            processB = Thread(target=scrapeCrossNexus, args=[clue])
            processB.start()
            threads.append(processB)
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
   if allReturn is None:
       return "Sorry, there was a Fatal Error <br><a href ='/'>Please enter your puzzle again</a>", None
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

   #last ditch effort incase the above doesn't work:
   if strategy.checkDone(clues, puzzle) != 0:
      strategy.oneLeft(clues, puzzle)
      count = 0

      #try oneLeft/compareChars approach to narrow down what's missing in puzzle
      while strategy.checkDone(clues, puzzle) != 0 and count < 11:
         strategy.compareChars(clues, puzzle)
         strategy.oneLeft(clues,puzzle)
         count += 1

      if strategy.checkDone(clues, puzzle) == 0:
         S = toHTML(puzzle, "Solved Puzzle: ", PUZZ, aClues, dClues, puzType)
         return S

      #narrow down who's still actually not done based on grid
      for clue in clues:
         clue.done = True
         for cell in clue.cells:
            if cell.value.isalpha():
               continue
            else:
               clue.done = False

      notDone = list()
      for clue in clues:
         if clue.done != True:
            notDone.append(clue)

      #if we still don't have an answer, try finding dictionary words that fit
      for clue in notDone:
         clue.reg = ""
         for cell in clue.cells:
            if cell.value.isalpha():
                clue.reg = clue.reg + cell.value
            else:
                clue.reg = clue.reg + "."

      oxPath = "/home/esceeles/mysite/Oxford.txt"
      D = importDict.importDict(oxPath)
      T = td.dictionary
      words = RegexDict(D)
      syns = RegexDict(T)

      for clue in notDone:
         for word in words[clue.reg]:
            if len(word) == clue.length and word not in clue.syns:
                clue.syns.append(word.upper())
         for syn in syns[clue.reg]:
            if len(syn) == clue.length and syn not in clue.syns:
                clue.syns.append(syn.upper())

      #try traversing one last time
      status = G.traverse(clues, puzzle, puzType)
      if status == 0:
         S = toHTML(puzzle, "Solved Puzzle: ", PUZZ, aClues, dClues, puzType)
         return S
      strategy.oneLeft(clues, puzzle)
      strategy.compareChars(clues, puzzle)
      strategy.oneLeft(clues, puzzle)

   S = toHTML(puzzle, "Solved Puzzle: ", PUZZ, aClues, dClues, puzType)
   return S



