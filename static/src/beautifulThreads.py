import requests
from bs4 import BeautifulSoup

#scrapes dictionary.com on a per clue basis and appends that clue to the current synonym list
def scrapeDictionDotCom(clue):
    length = clue.length
    c = clue.name
    URL = "https://www.dictionary.com/e/crosswordsolver/?query=" + c + "&pattern=&l=" + str(length)

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    syns = list()
    x = soup.findAll("div", {"class": "solver-cell"})
    print(clue.number, clue.direction, clue.name)

    l = (len(x))

    for i in range(2, l, 2):
        x = (soup.findAll("div", {"class": "solver-cell"})[i].text)
        syns.append(x)
    print(syns)
    for i in syns:
      i = i.replace(" ", "").replace("-", "").replace("_","")
      if len(i) == clue.length:
         clue.syns.append(i)

#scrapes crosswordNexus on a per clue basis and appends clue to current synonym list
def scrapeCrossNexus(clue):
    print(clue.number, clue.direction, clue.name)
    c = clue.name
    URL = "https://crosswordnexus.com/finder.php?clue=" + c + "&pattern="
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    tag = soup.tbody
    r = soup.findAll('big')
    x = soup.findAll('a')
    l = len(x) - 7
    syns = list()
    for i in range(18, l):
        temp = x[i].string
        syns.append(temp)
        #print(temp)
    print(syns)
    for i in syns:
      i = i.replace(" ", "").replace("-", "").replace("_","")
      if len(i) == clue.length:
         clue.syns.append(i)
