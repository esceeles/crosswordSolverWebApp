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
