from main import main
from output import toHTML
from flask import Flask, make_response
from flask import request, render_template
from inputPuzzle import inputPuzzle
import outputSteps
from nocache import nocache

app = Flask(__name__)
app.config["DEBUG"] = True

class hold:
    def __init__(self):
        self.puzzle = None
        self.puzString = None
        self.puzType = None
        self.stepArray = None
        self.guessArray = None
        self.aClues = None
        self.dClues = None
        self.form = None

c = hold()
d = hold()

#main page
@app.route('/', methods = ['GET', 'POST'])
@nocache
def hello_world():
    errors = ""
    if request.method == "POST":

        puzzle1 = None
        try:
            puzzle1 = str(request.form["puzzle1"])
            puzType = str(request.form["type"])
        except:
            errors += "<p>{!r} is not a valid input.</p>\n".format(request.form["puzzle1"])
        if puzzle1 is not None:
            puzType = str(request.form["type"])
            aClues, dClues, puzzle = inputPuzzle(puzzle1)
            #inputting puzzle information into two different objects because pythonAnywhere hosting site
            #seems to have issues with objects persisting over different files and functions
            c.form = request.form
            c.puzString = c.form["puzzle1"]
            c.puzzle = puzzle
            c.puzString = puzzle1
            c.puzType = puzType
            c.aClues = aClues
            c.dClues = dClues
            d.form = request.form
            d.puzString = c.form["puzzle1"]
            d.puzzle = puzzle
            d.puzString = puzzle1
            d.puzType = puzType
            d.aClues = aClues
            d.dClues = dClues

            if aClues == "nothing":
                return render_template('error.html', problem= "You didn't enter anything to process..")

            if aClues == "notNum":
                return render_template('error.html', problem= "Please enter an integer dimension as your first element")

            if aClues == "missing":
                return render_template('error.html', problem= "Your clues don't match with the numbers on the grid")

            puzHTML, strPuzzle = toHTML(puzzle, "Does this look correct?", puzzle1, aClues, dClues, puzType)

            return puzHTML


    #return resp
    return render_template('enterPuzzlePage.html', errors=errors)


#creates output and displays to user
@app.route('/success/', methods = ['POST', 'GET'])
@nocache
def output():

    puzzle1 = str(request.form["puzString"])
    puzType = str(request.form["puzType"])
    result, trash = main(puzzle1, puzType, c, d)
    return result


#shows the steps taken to get finished product
@app.route('/steps/', methods = ['POST', 'GET'])
@nocache
def steps():
    steps = c.stepArray
    steps = c.stepArray
    if steps is None:
        steps = d.stepArray
        if steps is None:
            handle()

    result = outputSteps.toHTML(steps, c, d)
    return result

#gives user info on project
@app.route('/info/', methods = ['GET'])
def info():
    return render_template('info.html')

@app.route('/handle/', methods = ['GET', 'POST'])
def handle():
    if c.puzString is None:
        return "Server lost your data, Please try again"
    stepArray, trash = main(c.puzString, "handle", c, d)
    if stepArray is None:
        return "Fatal Error"
    result = outputSteps.toHTML(stepArray, c, d)
    return result
