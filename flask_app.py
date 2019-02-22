from main import main
from output import toHTML
from flask import Flask
from flask import request, render_template
from inputPuzzle import inputPuzzle
from model_pylist import model

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
            puzType="synonym"
            aClues, dClues, puzzle = inputPuzzle(puzzle1)
            model.insert(puzzle, puzType, puzzle1)
            if aClues == "nothing":
                return '''
                <h4>You didn't enter anything to process...</h4>
                <p><a href=\"/\">Click here to do another one</a></div></p>
                '''
            if aClues == "notNum":
                return '''
                <h4> Please enter an integer dimension as your first element. </h4>
                <p><a href=\"/\">Click here to do another one</a></div></p>
                '''
            puzHTML, strPuzzle = toHTML(puzzle, "Does this look correct?", puzzle1, aClues, dClues, puzType)
            return puzHTML


            result = main(puzzle1)
            return result.format(puzzle1=puzzle1)


    return render_template('enterPuzzlePage.html', errors=errors)


@app.route('/success/', methods = ['POST', 'GET'])
def output():
    c = model.select()
    puzzle1 = c[0][2]
    puzType = c[0][1]
    #puzzle1 = request.form['puzzlestring']
    #return puzzle1
    #puzType = request.form["type"]
    result, trash = main(puzzle1, puzType)
    return result


