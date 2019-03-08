# Crossword Solver Web App

This project was designed to solve easy crossword puzzles. It can solve two
kinds: First, it can use a thesaurus to solve vocabulary puzzles.  Second, when
the API cooperates, it can solve newspaper crossword puzzles. This program uses
constraint-satisfaction problem algorithms, such as forward-checking and
backtracking, to select proper-fitting answers out of the potential guesses.

## Getting Started
Synonym Puzzles:
The clues for these puzzles need to be synonyms of the answers. Some of the
answers may not seem to be a perfect fit, but it's important to remember that
words can have a variety of meanings depending on how and it what time period
they are used.

Other Puzzles:
Clues cannot be interconnected or themed. This feature is in beta and success depends
on the strength of the databases being used. Currently, those databases are
CrosswordNexus.com and Dictionary.com. If two or more clue answers are missing
from the database, the algorithm is unable to find a solution, so it's best to
stick to smaller or easier puzzles, those occurring earlier in the week.

##Deployment
Before running the source code, you'll need to clone the moby thesaurus from
https://github.com/words/moby.git and save it as mobythes.aur with your source
code.

## Built With

* [PythonAnywhere](http://www.pythonanywhere.com/) - The web framework used
* [Vim](https://www.vim.org/) - Text Editor
* [Moby](http://moby-thesaurus.org/) - Local Thesaurus
* [Crossword Nexus](https://crosswordnexus.com/dictionary) - Online crossword clue database
* [Dictionary.com](https://www.dictionary.com/e/crosswordsolver/) - Online crossword clue database

## Author

* **Ellie Sceeles** - [GitHub](https://github.com/esceeles/crosswordSolverWebApp.git)

