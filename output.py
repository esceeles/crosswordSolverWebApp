def toHTML(puzzle, status, puzzle1, aClues, dClues, puzType):

   sz = (puzzle.size+2) * 30

   header = """<html>
   <head>
   <style>
      #wrapper {background-color: white; border: 1px solid black; width: """+ str(sz) + """px; height: """ + str(sz) + """px; margin: 0 auto; color:black}
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
   </head>
   <body style = \"display:flex; background-color:black; color:white; font-family:"Courier New", Courier, monospace\">
   <div style = \"float:left; margin-left: 30px\"><h1>""" + status + """</h1><p><h3>Across Clues: </h3><ul style = \"width: 300px\">"""
   S = header

   for i in aClues:
       S = S + "<li>" + i.number + ": " + i.name + "</li>"

   S = S + "</ul><h3> Down Clues:</h3><ul>"

   for i in dClues:
       S = S + "<li>" + i.number + ": " + i.name + "</li>"


   S = S + "</ul></p></div><p><div id = \"wrapper\"> "

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


   footer = " <p><a href=\"/\">Click here to do another one</a></div></p>"


   S = S + "</body></html><div style=\"float:right\"> "

   #button = "<button class=\"btn success\">Success</button>"


   form = "<div style = \"float:right; margin-right: 0px\"><form action=\"/success/\" method=\"post\"><input style = \"float:right\" type=\"submit\" value= \"Looks good!\"  name=\"button\" id=\"name\" /> </form>"

   if status == "Does this look correct?":
        #footer = form + "<button><a href=\"/\">No, I'll fix it</a></button></div>" + "</body></html>"
        footer = form + "<form action=\"/\"> <input style = \"float:right; margin-right: 0px; margin-top:10px\" type=\"submit\" value= \"No, I'll fix it\"  name=\"button\" id=\"name\" /> </form> </a></button></div></div>" + "</body></html>"
   else:
        img = "<img style = \"float:right\" src=\"https://unixtitan.net/images/clip-crossword-3.png\">"
        footer = "<p style = \"float:right; margin-right:0px;\"><a href=\"/\">Click here to do another one</a></p></div>"
        if puzType == "synonym":
            footer = "<p style = \"float:right; margin-right:0px\"><a href=\"/steps/\">How'd we get here?</a></p><br>" + footer
   S = S + footer

   return S, puzzle1





