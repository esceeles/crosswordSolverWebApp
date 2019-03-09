import copy
import strategy

#holds the puzzle information as a graph
class GraphTree:
    def __init__(self, nextClue, puzzle):
        # root will be empty (value wise) but will hold the clue for the next syns/nexts
        self.root = Path(nextClue, None, None, puzzle, None, list())
        self.arcList = list()
        self.edges = dict()
        self.wordToClue = dict()
        self.graph = list()

    #returns neighbors of vertex
    def neighbors(self, id):
        return self.edges[id]

    #finds all edges/arcs for puzzle
    def findAllArcs(self, clues):
        for clue in clues:
            if len(clue.xCells) > 0:
                for xCell in clue.xCells:
                    temp = xCell.clues
                    if temp not in self.arcList and temp[0] in clues and temp[1] in clues:
                        self.arcList.append(temp)
                        x, y = temp[0].name, temp[1].name
                        a, b = temp[1], temp[0]
                        t = [a, b]
                        if x not in self.edges:
                            self.edges[x] = [y]
                            self.wordToClue[x] = temp[0]
                        else:
                            self.edges[x].append(y)
                        if t not in self.arcList:
                            self.arcList.append(t)
                            if a.name not in self.edges:
                                self.wordToClue[a.name] = temp[1]
                                self.edges[a.name] = [b.name]
                            else:
                                self.edges[a.name].append(b.name)

    #finds feasible guesses for clue based on information already in puzzle
    def makeSynList(self, current, puzzle):
        current.nextClue.updateCells(puzzle)
        #current.nextClue.print()
        removeList = list()
        current.synList = current.nextClue.syns.copy()
        for syn in current.synList:
            for idx, c in enumerate(current.nextClue.cells):
                if c.value.isalpha() and syn[idx] != c.value:
                    removeList.append(syn)
        for i in removeList:
            if i in current.synList:
                current.synList.remove(i)
        removeList.clear()

    #finds the next clue to process based on arcs in graph
    def findNextClue(self, current):
        path = None
        temparcs = current.arcList.copy()
        for i in temparcs:
            if i[0] == current.nextClue and i[1] not in current.journeyNames:
                path = i[1]
                x = i.copy()
                temparcs.remove(i)
                x.reverse()
                if x in temparcs:
                  temparcs.remove(x)
                return path, temparcs, current

        if path == None:
            ret = self.backtrack(current)
            if ret is None:
                return 2, None, None
            else:
                path = ret[0]
                temparcs = ret[1]
                current = ret[2]

            return path, temparcs, current

    #finds next clue to process when you've completed all the current node's arcs
    def backtrack(self, current):
        revJourneyNames = current.journeyNames.copy()
        revJourneyPaths = current.journeyPaths.copy()
        revJourneyNames.reverse()
        revJourneyPaths.reverse()
        path = None
        temparcs = current.arcList.copy()
        for prev in revJourneyNames:
            for i in temparcs:
                if i[0] == prev and i[1] not in current.journeyNames:
                    for j in revJourneyPaths:
                        if j.nextClue == prev:
                            path = i[1]
                            x = i.copy()
                            temparcs.remove(i)
                            x.reverse()
                            if x in temparcs:
                              temparcs.remove(x)
                            old = current
                            current = j
                            current.arcList = old.arcList
                            return path, temparcs, current

    #traverses the graph and finds a solution
    def traverse(self, clues, puzzle, puzType):
        current = self.root
        current.arcList = self.arcList
        stepArray = list()
        stepArray.clear()
        guessArray = list()
        guessArray.clear()

        while strategy.checkDone(clues, puzzle) != 0:

            self.makeSynList(current, puzzle)

            #removes words and backtracks when a dead end is reached
            if current.synList == 0 or len(current.synList) == current.tryIndex:
                revJourney = current.journeyPaths.copy()
                revJourney.reverse()
                current.tryIndex = 0
                if not revJourney:
                    return 1, None, None
                temp = None
                for i in self.arcList:
                  if i[1].name == current.nextClue.name:
                     temp = i
                current = revJourney[0]
                if temp not in current.arcList:
                  current.arcList.append(temp)

                needList = list()
                for i in clues:
                  if i.done == False:
                     needList.append(i)
                for i in needList:
                  accountedFor = False
                  for x in current.arcList:
                     if i == x[1]:
                        accountedFor = True
                  if accountedFor == False:
                     for z in self.arcList:
                        if z[1] == i:
                           temp = z
                     if temp not in current.arcList:
                              current.arcList.append(temp)

                strategy.removeWord(current.nextClue, puzzle)
                continue

            wordChosen = current.synList[current.tryIndex]
            if strategy.insertWord(current.nextClue, wordChosen, puzzle) == 1:
                return 1, None, None
            current.tryIndex += 1
            j = current.journeyNames.copy()
            jP = current.journeyPaths.copy()
            j.append(current.nextClue)
            jP.append(current)
            if puzType == "synonym":
                stepArray.append(copy.deepcopy(puzzle))
                l = copy.deepcopy(current.synList)
                m = current.nextClue.number + " " + current.nextClue.direction + ": " + current.nextClue.name
                l.insert(0, str(m))
                guessArray.append(l)
                del l
            if strategy.checkDone(clues, puzzle) == 0:
                return 0, stepArray, guessArray
            path, temparcs, current = self.findNextClue(current)
            if path == 2:
                return 2, None, None
            current.children.append(Path(path, wordChosen, current, puzzle, temparcs, j))

            current.childCount += 0
            current.children[current.childCount].journeyPaths = jP
            current = current.children[current.childCount]

#holds path information for traversal
class Path:
    def __init__(self, nextClue, value, parent, puzzle, arcList, journey):
        self.parentCount = -1
        self.childCount = -1
        self.parent = parent  # who do we go back to if we need to backtrack
        self.value = value  # this will hold the synonym chosen
        self.children = list()  # this will be pointers to child next
        self.SynList = list()  # holds the syns that will become children
        self.nextClue = nextClue  # this will hold the clue for which children are chosen
        self.tryIndex = 0  # for keeping track of which children we've tried when we are when backtracking
        self.arcList = arcList
        self.journeyPaths = list()
        self.journeyNames = journey  # need to find a way to track all the nodes that have come before

#finds the least connected node to start the search
def findLeastConnected(clues,
                       puzzle):  # might want to do "most connected". why else would i want one from the middle???
    leastConnected = list()
    for clue in clues:
        if len(leastConnected) == 0:
            leastConnected.append(clue)
        elif len(clue.xCells) < len(leastConnected[0].xCells):
            leastConnected.insert(0, clue)
        else:
            i = 0
            while len(clue.xCells) > len(leastConnected[i].xCells) and i < len(leastConnected) - 1:
                i += 1
            leastConnected.insert(i + 1, clue)
    return leastConnected  # list of square in order of least connected to most, leastConnected[0] is root
