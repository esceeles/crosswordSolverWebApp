
# A very simple Flask Hello World app for you to get started with...
from main import main
from output import toHTML
from flask import Flask
from flask import request, render_template
from inputPuzzle import inputPuzzle

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    errors = ""
    if request.method == "POST":
        puzzle1 = None
        try:
            puzzle1 = str(request.form["puzzle1"])
        except:
            errors += "<p>{!r} is not a valid input.</p>\n".format(request.form["puzzle1"])
        if puzzle1 is not None:
            aClues, dClues, puzzle = inputPuzzle(puzzle1)
            puzHTML, strPuzzle = toHTML(puzzle, "Does this look correct?", puzzle1, aClues, dClues)
            #output(strPuzzle)
            return puzHTML
            result = main(puzzle1)
            return result.format(puzzle1=puzzle1)


    return render_template('enterPuzzlePage.html', errors=errors)


@app.route('/success/', methods = ['POST', 'GET'])
def output():
    puzzle1 = request.form['puzzlestring']
    result, trash = main(puzzle1)
    return result




