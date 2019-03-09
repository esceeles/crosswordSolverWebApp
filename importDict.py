import csv
import unicodedata
#pulls in information from local databases for synonym puzzles

#reads in CSV file
def importCSV(csvfile):

   #reads in csv file as newdict
   with open(csvfile, mode = 'r') as infile:
      reader = csv.reader(infile)
      mydict = {columns[0]:columns[1].split(',') for columns in reader}

   newdict = {}
   for clue in mydict:
      newdict[clue] = []
      for items in mydict[clue]:
         head, sep, tail = items.partition('(')
         newdict[clue].append(unicodedata.normalize("NFKD", head).strip(' '))

   #new dict holds the "Clue: synonym" pair with unicode encoding...
   return newdict

#reads in thesausus as .aur file
def importAUR(aurfile):
   dictionary = list()
   with open(aurfile) as infile:
      for line in infile:
         x = infile.readline()
         x = x.strip('\n')
         x = x.split(',')
         dictionary.append(x)
   return dictionary

def importDict(oxfile):
   dictionary = dict()
   with open(oxfile, mode = "r") as infile:
      for line in infile:
         line = line.split(" ")
         if len(line) > 2:
            title = line[0]
            typ = line[2]
            t = None
            if len(typ) > 0:
               if not typ[0].isalpha():
                  typ = typ[1:]
            if typ == "n." or typ == "-n.":
               t = "noun"
            elif typ == "v." or typ == "-v.":
               t = "verb"
            elif typ == "adj." or typ == "-adj.":
               t = "adj"
            elif typ == "adv." or typ == "-adv.":
               t = "adv"
            elif typ == "abbr." or typ == "-abbr.":
               t = "abbr"
            elif typ == "symb." or typ == "-symb.":
               t = "symb"
            else:
               t = "other"
            title = title.lower()
            if title not in dictionary:
               dictionary[title] = list()
            line = line[3:]
            Glist = list()
            lst = list()
            for item in line:
               if item.isdigit():
                  Glist.append(lst)
                  lst.clear()
               else:
                  lst.append(item)
            dictionary[title].append((t, Glist))
   return dictionary


import re

class RegexDict():
   def __init__(self, dic):
      self.data = dic
   def __getitem__(self, key):
      if key in self.data: return self.data[key]
      regex = key
      if isinstance(key, str):
         regex = re.compile(key)
      ans = list()
      for k in self.data.keys():
         if regex.search(k):
            ans.append(k)
      return ans
