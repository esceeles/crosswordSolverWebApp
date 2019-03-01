def toHTML(puzzle, status, puzzle1, aClues, dClues, puzType):

   sz = (puzzle.size+2) * 30

   header = """<html>
   <head>
   <style>
      #wrapper {border: 1px solid black; width: """+ str(sz) + """px; height: """ + str(sz) + """px; margin: 0 auto;}
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
   <h1>""" + status + """</h1>
   </head>
   <body>
   <div style = \"float:left\"><p><h3 style = \"float:left\">Across Clues: </h3><br><br><ul style = \"width: 350px\">"""
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


   form = "<form action=\"/success/\" method=\"post\"><input type=\"submit\" value= \"Looks good!\"  name=\"button\" id=\"name\" /> </form>"

   if status == "Does this look correct?":
        #footer = form + "<button><a href=\"/\">No, I'll fix it</a></button></div>" + "</body></html>"
        footer = form + "<form action=\"/\"> <input type=\"submit\" value= \"No, I'll fix it\"  name=\"button\" id=\"name\" /> </form> </a></button></div>" + "</body></html>"
   else:
        footer = "<p><a href=\"/\">Click here to do another one</a></div></p>"
        if puzType == "synonym":
            footer = "<form action=\"/steps/\" method=\"post\"><input type=\"submit\" value= \"How'd we get here?\"  name=\"button\" id=\"name\" /> </form>" + footer
   S = S + footer

   return S, puzzle1





