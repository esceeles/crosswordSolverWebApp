from main import main
from output import toHTML
from flask import Flask
from flask import request, render_template
from inputPuzzle import inputPuzzle
from model_pylist import model
import outputSteps
from nocache import nocache

app = Flask(__name__)
app.config["DEBUG"] = True
m = model()

class hold:
    def __init__(self):
        self.puzzle = None
        self.puzString = None
        self.puzType = None
        self.stepArray = None
        self.aClues = None
        self.dClues = None

c = hold()

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
            c.puzzle = puzzle
            c.puzString = puzzle1
            c.puzType = puzType
            if c.puzzle == None or c.puzString == None or c.puzType == None:
                return "Error with insert"
            if c.puzzle != puzzle or c.puzString != puzzle1 or c.puzType != puzType:
                return "Copy remained"
            #while len(model.entries) != 0:
                #m.entries.clear()
            #while len(m.entries) == 0:
                #params = [puzzle, puzType, puzzle1]
                #m.entries.append(params)
                #m.insert(puzzle, puzType, puzzle1)
            if aClues == "nothing":
                return render_template('error.html', problem= "You didn't enter anything to process..")

            if aClues == "notNum":
                return render_template('error.html', problem= "Please enter an integer dimension as your first element")

            puzHTML, strPuzzle = toHTML(puzzle, "Does this look correct?", puzzle1, aClues, dClues, puzType)
            for i in range(0,3):
                c.puzString = puzzle1
                c.puzzle = puzzle
                c.puzType = puzType
            while c.puzString != puzzle1:
                c.puzString = puzzle1
            while c.puzzle != puzzle:
                c.puzzle = puzzle
            while c.puzType != puzType:
                c.puzType = puzType
            return puzHTML

    return render_template('enterPuzzlePage.html', errors=errors)


@app.route('/success/', methods = ['POST', 'GET'])
@nocache
def output():
    #c = m.select()
    #return c[0][2]
    """
    try:
        puzzle1=c[0][2]
    except IndexError:
        try:
            x = c[0]
            return x
        except IndexError:
            return c
    """
    #puzzle1 = c[0][2]
    #puzType = c[0][1]
    #return c.puzString
    puzzle1 = c.puzString
    puzType = c.puzType
    result, trash = main(puzzle1, puzType, c)
    #model.insert(result, None, None)
    return result


@app.route('/steps/', methods = ['POST', 'GET'])
@nocache
def steps():
    #c = m.select()
    #return c[1][0][0]
    """
    try:
        steps = c[1][0]     #to get second insert into model, first item (result, inserted in output())
    except IndexError:
        try:
            x = c[1]
            return x
        except IndexError:
            return c
    """
    steps = c.stepArray
    result = outputSteps.toHTML(steps)
    return result

@app.route('/info/', methods = ['GET'])
def info():
    return render_template('info.html')
