import flask_app
#uses puzzle information from step array to create an graphical output of what steps were taken to complete the puzzle

def toHTML(stepArray, c, d):
   if stepArray is None:
       return "Puzzle lost <br><a href =\'/\'>Please enter puzzle again</a>", None
   try:
      puzzle = stepArray[0]
   except IndexError:
      flask_app.handle()
      return "Puzzle lost <br><a href =\'/\'>Please enter puzzle again</a>", None
   sz = (puzzle.size+2) * 30

   header = """<html>
   <head>
   <style>
      #wrapper {background-color: right; border: 1px solid black; width: """+ str(sz) + """px; height: """ + str(sz) + """px; margin: 0 auto; color: black}
      div {contentEditable: true}
      .filled {width: 28px; height: 28px; background: black; border: 1px solid black; padding: 0; margin: 0; float: left;}
      .empty {width: 28px; height: 28px; border: 1px solid black; padding: 0; margin: 0; float: left;}
      .answered {width: 28px; height: 28px; border: 1px solid black; padding: 0; margin: 0; float: left;}
      .numbered {counter-increment: value;}
      .numbered:nth-of-type(n)::before {content: counter(value); font-size: 10px; position: absolute;}
      .btn {border: none; background-color: inherit; padding: 14px 28px; font-size: 16px; cursor: pointer; display: inline-block;}
      .btn:hover {background: #eee;}
      .success {color: green;}
   </style>
   <h1 style=\"color:white\">""" + "Steps: " + """</h1>
   </head>
   <body style = \"background-color:black\">"""
   S = header

   for idx, step in enumerate(stepArray):
      if c.guessArray is not None:
        if c.guessArray[idx] is not None:
            S = S + "<p>"
            for edx, guess in enumerate(c.guessArray[idx]):
                if edx == 0:
                    S = S + guess + "<br>"
                else:
                    S = S + guess + ". "
            S = S + "</p>"
      S = S + "<p><div style=\"background-color:white\" id = \"wrapper\"> "
      puzzle = step
      for i in range(0, puzzle.size+2):
         for j in range(0, puzzle.size+2):
            if puzzle.grid[i][j].value == '#':
                S = S + "<div class = \"filled\"></div>""\n"
            elif puzzle.grid[i][j].value.isdigit():
                S = S + "<div class = \"empty numbered\"></div>""\n"
            elif puzzle.grid[i][j].value.isalpha():
            #return puzzle.grid[i][j].value
                S = S + "<div class = \"empty answered\">" + puzzle.grid[i][j].value + "</div>""\n"
            else:
                S = S + "<div class = \"empty\"></div>""\n"
      S = S + "</div></p><br>"

   S = S + """<img style = \"height: 700; display: block; margin-left: auto; margin-right: auto\"
   src = \"https://unixtitan.net/images/clip-crossword-3.png\"> <p><a href=\"/\">Click here to do another
   one</a></div></p></body></html>"""

   return S