from main import main
from output import toHTML
from flask import Flask
from flask import request, render_template
from inputPuzzle import inputPuzzle
from model_pylist import model
import outputSteps

app = Flask(__name__)
app.config["DEBUG"] = True
model = model()

@app.route('/', methods = ['GET', 'POST'])
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
            model.clear()
            model.insert(puzzle, puzType, puzzle1)
            if aClues == "nothing":
                return render_template('error.html', problem= "You didn't enter anything to process..")

            if aClues == "notNum":
                return render_template('error.html', problem= "Please enter an integer dimension as your first element")

            puzHTML, strPuzzle = toHTML(puzzle, "Does this look correct?", puzzle1, aClues, dClues, puzType)
            return puzHTML


            #result = main(puzzle1)
            #return result.format(puzzle1=puzzle1)


    return render_template('enterPuzzlePage.html', errors=errors)


@app.route('/success/', methods = ['POST', 'GET'])
def output():
    c = model.select()
    #return c[0][2]
    puzzle1 = c[0][2]
    puzType = c[0][1]
    result, trash = main(puzzle1, puzType, model)
    #model.insert(result, None, None)
    return result


@app.route('/steps/', methods = ['POST', 'GET'])
def steps():
    c = model.select()
    #return c[1][0][0]
    steps = c[1][0]     #to get second insert into model, first item (result, inserted in output())
    result = outputSteps.toHTML(steps)
    return result

@app.route('/info/', methods = ['GET'])
def info():
    return render_template('info.html')
