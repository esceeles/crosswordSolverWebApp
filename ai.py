#import copy
#import math
import strategy
#import heapq
import collections
class Queue:
   def __init__(self):
        self.elements = collections.deque()

   def empty(self):
        return len(self.elements) == 0

   def put(self, x):
        self.elements.append(x)

   def get(self):
        return self.elements.popleft()


class GraphTree:
    def __init__(self, nextClue, puzzle):
        self.root = Path(nextClue, None, None, puzzle, None,
                         list())  # root will be empty (value wise) but will hold the clue for the next syns/nexts
        self.arcList = list()
        self.edges = dict()
        self.wordToClue = dict()
        self.graph = list()
    def neighbors(self, id):
        return self.edges[id]

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


    def BFS(graph, root, puzzle, clues):
       path = Queue()
       path.put(root)
       came_from = {}
       came_from[root] = None

       while not path.empty():
           c = path.get()
           #print("current Clue: ", c)
           temp = graph.wordToClue[c]
           current = Path(temp, None, None, puzzle, None, None)
           #print("calling makeSynList for ", current.nextClue)
           graph.makeSynList(current, puzzle)
           #print("after making SynList")

           if current.synList == 0 or len(current.synList) == current.tryIndex:
               #print("######try index overflow or no synList")
               current.tryIndex = 0
               connections = graph.edges[c]
               next = None
               for link in connections:
                 #print(link)
                 clue = graph.wordToClue[link]
                 if clue.done == True:
                     #print("removing word")
                     strategy.removeWord(clue, puzzle)
                     #puzzle.print()
                     next = clue
                     #path.put(next)
                 break
               current = Path(next, None, None, puzzle, None, None)
               graph.makeSynList(current, puzzle)
               continue

           wordChosen = current.synList[current.tryIndex]
           #print("after choosing word")
           if strategy.insertWord(current.nextClue, wordChosen, puzzle) == 1:
               #print("problem inserting word")
               return 1
           current.tryIndex += 1
           #puzzle.print()
           if strategy.checkDone(clues, puzzle) == 0:
               return 0

           for next in graph.neighbors(c):
               if next not in came_from:
                  path.put(next)
                  came_from[next] = c

       return came_from

    # A function used by DFS
    def DFSUtil(self,v,visited):

        # Mark the current node as visited and print it
        visited[v]= True
        print(v)

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.DFSUtil(i, visited)


    # The function to do DFS traversal. It uses
    # recursive DFSUtil()
    def DFS(self,v):

        # Mark all the vertices as not visited
        visited = [False]*(len(self.graph))

        # Call the recursive helper function to print
        # DFS traversal
        self.DFSUtil(v,visited)

    def makeSynList(self, current, puzzle):
        #print("making syn list")
        current.nextClue.updateCells(puzzle)
        current.nextClue.print()
        #for i in current.nextClue.cells:
            #print(i.value)
        removeList = list()
        current.synList = current.nextClue.syns.copy()
        #print(current.synList)
        for syn in current.synList:
            for idx, c in enumerate(current.nextClue.cells):
                if c.value.isalpha() and syn[idx] != c.value:
                    removeList.append(syn)
        for i in removeList:
            if i in current.synList:
                current.synList.remove(i)
        removeList.clear()
        #print(current.synList)
        #print("end of making synList")

    def findNextClue(self, current):
        #print("finding next clue")
        path = None
        temparcs = current.arcList.copy()
        #print("current arcList")
        #for i in temparcs:
            #print(i[0].name, i[1].name)
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
            path, temparcs, current = self.backtrack(current)
            return path, temparcs, current

    def backtrack(self, current):
        #print("backtracking")
        revJourneyNames = current.journeyNames.copy()
        revJourneyPaths = current.journeyPaths.copy()
        revJourneyNames.reverse()
        revJourneyPaths.reverse()
        path = None
        temparcs = current.arcList.copy()
        #print(len(temparcs))
        #print(len(revJourneyNames))
        for prev in revJourneyNames:
            for i in temparcs:
                #print(i[0].name, i[1].name)
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
                            #print(path, temparcs, current)
                            return path, temparcs, current

    def traverse(self, clues, puzzle):
        current = self.root
        current.arcList = self.arcList

        while strategy.checkDone(clues, puzzle) != 0:
            #print("nextClue: ", current.nextClue.name)

            self.makeSynList(current, puzzle)
            # print("after making synList")
            if current.synList == 0 or len(current.synList) == current.tryIndex:
                #print("######try index overflow or no synList")
                #print("len of synList: ", len(current.synList))
                #print("try index: ", current.tryIndex)
                revJourney = current.journeyPaths.copy()
                revJourney.reverse()
                current.tryIndex = 0
                #print("resetting try index for: ", current.nextClue.name, "to 0")
                if not revJourney:
                    #print("I'm sorry, this puzzle is unsolvable with current guess set")
                    return 1
                #print("previously visited nodes:")
                #if revJourney:
                    #for i in revJourney:
                        #print(i.nextClue.name)
                temp = None
                for i in self.arcList:
                  if i[1].name == current.nextClue.name:
                     temp = i
                #for i in current.arcList:
                  #print(i[0].name, i[1].name)
                current = revJourney[0]
                if temp not in current.arcList:
                  current.arcList.append(temp)

               ####
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
                ###
                #print("word removed: ", current.nextClue.name)
                strategy.removeWord(current.nextClue, puzzle)
                continue

            wordChosen = current.synList[current.tryIndex]
            if strategy.insertWord(current.nextClue, wordChosen, puzzle) == 1:
                #print("problem with inserting word")
                return 1
            current.tryIndex += 1
            #puzzle.print()
            j = current.journeyNames.copy()
            jP = current.journeyPaths.copy()
            j.append(current.nextClue)
            jP.append(current)  # or current.child
            if strategy.checkDone(clues, puzzle) == 0:
                return 0
            #print("before finding next clue")
            path, temparcs, current = self.findNextClue(current)
            current.children.append(Path(path, wordChosen, current, puzzle, temparcs, j))

            current.childCount += 0
            current.children[current.childCount].journeyPaths = jP
            current = current.children[current.childCount]


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
