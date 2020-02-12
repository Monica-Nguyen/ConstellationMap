#Name: Monica Nguyen
#Date: Nov 15, 2019
#The following program plots stars and constellations from input files. Turtle is used to make the drawing window and users can choose what constellations to plot. The coordinates of the box around each drawn constellation is written out to a text file. Includes error handling. 
#Usage Example: python ConstellationMap.py stars_1.dat -names
#After drawing all the stars, the user is prompted for the name of the star file. It could be UrsaMajor.dat that is entered next. 

import sys
import os
import turtle

WIDTH = 600
HEIGHT = 600
PIXELSTEP = 75 #8 steps of 75 pixels makes an axis of 600 pixels
SCREENSTEPS = 8
TICK = 5
AXISINCREMENT = 0.25 #Axes increase by 0.25 for each tick
TEXTGAP = 20
INCREMENT = 1
AXISCOLOR = "blue"
BACKGROUNDCOLOR = "black"


#Purpose: Handle the arguments. Error handles incorrect stars-location-file inputs and exits if the user enters something invalid.
#Parameters: pointer #I had to pass pointer as a parameter for the rest of the program to function properly!! Otherwise, error handling was not correct.
#Return: starsLocationFile
def handleArguments(pointer):
    try:
        if len(sys.argv) == 1:
            starsLocationFile = input("Enter stars-location-file: ")
            readStarFiles(starsLocationFile)

        elif len(sys.argv) == 2:
            if sys.argv[1]=="-names":
                starsLocationFile = input("Enter stars-location-file: ")
                noNameStars, namedStars = readStarFiles(starsLocationFile)
                drawStars(noNameStars, namedStars, pointer) #Calls function to draw stars
                labelStars(namedStars, pointer) 
             
            else:
                starsLocationFile = sys.argv[1]
                readStarFiles(starsLocationFile)
               
        elif len(sys.argv) == 3:
        
            if sys.argv[1]!="-names" and sys.argv[2]!="-names":
                print("Error. At least one input must be -names.")
                sys.exit(1)
                
            else:
                if sys.argv[1]=="-names":
                    starsLocationFile = sys.argv[2] #sys.argv[2] is argument(file_name)
                    noNameStars, namedStars = readStarFiles(starsLocationFile)
                    drawStars(noNameStars, namedStars, pointer)
                    labelStars(namedStars, pointer) 
                    
                else:
                    starsLocationFile = sys.argv[1] #sys.argv[1] is argument(file name)
                    noNameStars, namedStars = readStarFiles(starsLocationFile)
                    drawStars(noNameStars, namedStars, pointer) #Calls function to draw stars
                    labelStars(namedStars, pointer) 
                            
           
        else: #More than 3 arguments produces an error
            print("Error: too many arguments.")
            sys.exit(1)
        return starsLocationFile
    except:
        print("The stars-location-file you entered is invalid.")
        sys.exit(1)


#Purpose: Drawing the blue x-axis and y-axis with 0.25 increments within the (0,0) and (600,600) pixel window
#Parameters: pointer
#Return: none        
def drawAxes(pointer):
    pointer.color(AXISCOLOR)
    pointer.up()
    SCREENTEXTX = -1 #Axes start at -1 
    for i in range(0, SCREENSTEPS + 1, INCREMENT): #drawing x-axis
        screenStep = PIXELSTEP * i   
        pointer.goto(screenStep,HEIGHT/2)
        pointer.down()
        pointer.goto(screenStep,HEIGHT/2 + TICK)
        pointer.goto(screenStep,HEIGHT/2 - TICK)
        pointer.up()
        pointer.goto(screenStep,HEIGHT/2 - TEXTGAP)
        if SCREENTEXTX != 0:
            pointer.write(SCREENTEXTX, False, align = 'center')
        pointer.goto(screenStep,HEIGHT/2)
        SCREENTEXTX = SCREENTEXTX + AXISINCREMENT
        pointer.down()
        
    pointer.up()
    SCREENTEXTY = -1 #Axes start at -1 
    for i in range(0, SCREENSTEPS + 1, INCREMENT): #drawing y-axis
        screenStep = PIXELSTEP * i   
        pointer.goto(WIDTH/2,screenStep)
        pointer.down()
        pointer.goto(WIDTH/2 + TICK,screenStep)
        pointer.goto(WIDTH/2 - TICK,screenStep)
        pointer.up()
        pointer.goto(WIDTH/2 - TEXTGAP,screenStep - TICK)
        if SCREENTEXTY != 0:
            pointer.write(SCREENTEXTY, False, align = 'center')
        pointer.goto(WIDTH/2,screenStep)
        SCREENTEXTY = SCREENTEXTY + AXISINCREMENT
        pointer.down()

#Purpose: Read star files
#Parameters: starsLocationFile
#Return: noNameStars, namedStars which is a list of tuples
def readStarFiles(starsLocationFile): 
    x = []
    y = []
    mag = []
    names = []
    noNameStars = [] #some stars have no name
    namedStars = {} #dictionary for stars with names
    

    starsOpen = open(starsLocationFile, "r")
    starLocationLines = starsOpen.readlines()


    for line in starLocationLines:
        line = line.strip("\n") #removing blank space
        line = line.split(",") 
        x = line[0]
        y = line[1]
        mag = line[4]
        names = line[6]
        
        if names != "": #one name and two named stars drawn in white
            names = names.split(";") #splitting the two named stars into a list called names
            for starName in names: #looping through names and assigning x,y,mag to each 
                namedStars[starName] = (x,y,mag)
                print(f'{starName} is at ({x},{y}) with magnitude {mag}.')
        else: #len(line) < 6 so unnamed stars drawn in grey
            noNameStars.append((x,y,mag))

    return noNameStars, namedStars
   
    starLocationLines.close()
    
#Purpose: Drawing the stars
#Parameters: noNameStars, namedStars, pointer
#Return: none    
def drawStars(noNameStars, namedStars, pointer):
    pointer.up()
    pointer.color("white")
    for key in namedStars:
        x = float(namedStars[key][0])
        y = float(namedStars[key][1])
        mag = float(namedStars[key][2])
        
        screenX = x * (WIDTH / 2) + WIDTH/2 #WIDTH/2 is the ratio, + WIDTH is XO
        screenY = y * (HEIGHT / 2) + HEIGHT/2 #HEIGHT/2 is the ratio, + HEIGHT is YO
        
        radius = (10/(mag + 2)) / 2
        pointer.goto(screenX,screenY)
        pointer.begin_fill()
        pointer.circle(radius)
        pointer.end_fill()
        pointer.up()

    pointer.color("grey")
    for num in noNameStars: #num has x,y,mag of stars without a name 
        x = float(num[0])
        y = float(num[1])
        mag = float(num[2])
        
        screenX = x * (WIDTH / 2) + WIDTH/2 #WIDTH/2 is the ratio, + WIDTH is XO
        screenY = y * (HEIGHT / 2) + HEIGHT/2 #HEIGHT/2 is the ratio, + HEIGHT is YO
        
        radius = (10/(mag + 2)) / 2
        pointer.goto(screenX,screenY)
        pointer.begin_fill()
        pointer.circle(radius)
        pointer.end_fill()
        pointer.up()

#Purpose: Labels the named stars if there is -names as input 
#Parameters: namedStars, pointer
#Return: none          
def labelStars(namedStars, pointer):
    pointer.up()
    pointer.color("white")
    
    for key in namedStars:
        x = float(namedStars[key][0])
        y = float(namedStars[key][1])
        
        screenX = x * (WIDTH / 2) + WIDTH/2 
        screenY = y * (HEIGHT / 2) + HEIGHT/2
    
        pointer.goto(screenX,screenY+TEXTGAP/6)
        pointer.write(key,font=("Arial", 5, "normal"), align = 'center')
        
#Purpose: Read constellation files
#Parameters: constellationsLines
#Return: constellationName, edgesList 
def readConstellationFiles(constellationsLines):
    starsEdge1 = []
    starsEdge2 = []
    starsList = [] #for printing purposes 
    edgesList = []
    constellationNames = ''
    
    constellationNames= constellationsLines[0].strip('\n')
    
    del constellationsLines[0] #Remove first line of constellation file, which is only a name, to loop through rest without index errors

    i = 0 #Initializing while loop, not a magic number
    helpsplit = []
    helpertuple = ('','')
    restline = ''
    while i < len(constellationsLines):
        restline = constellationsLines[i].strip('\n')
        helpsplit = restline.split(",")
        starsEdge1.append(helpsplit[0])
        starsEdge2.append(helpsplit[1])
        helpertuple = (helpsplit[0],helpsplit[1])
        
        edgesList.append(helpertuple)
        i = i + 1
    for star in starsEdge1:
        if star not in starsList:
            starsList.append(star)
    for star in starsEdge2:
        if star not in starsList:
            starsList.append(star)
    printlist = constellationNames + " constellation contains {"
    for star in starsList:
        printlist = printlist + "'" + star + "'" + "," #This was for the sole stylistic purpose of having the string inside curly brackets {} as written on the assignment page, otherwise could have just printed a list of unique stars with []
    
    printlist = printlist[:-1] + "}"
    print(printlist)

    return constellationNames, edgesList
    
#Purpose: Draw the constellations onto the black blackground.
#Parameters: constellationNames, edgesList, namedStars, pointer
#Return: none
def drawConstellation(constellationNames, edgesList, namedStars, pointer):
    listwithxytuples = []
    helper_tuple_3 = (0,0,0)
    
    for starset in edgesList:
        helper_tuple_3 = namedStars.get(starset[0])
        helper_tuple_2 = (float(helper_tuple_3[0]),float(helper_tuple_3[1]))
        listwithxytuples.append(helper_tuple_2)
        helper_tuple_3 = namedStars.get(starset[1])
        helper_tuple_2 = (float(helper_tuple_3[0]),float(helper_tuple_3[1]))
        listwithxytuples.append(helper_tuple_2)
    
    star1 = 0 #Initializing for the while loop.. not a magic number and same for the function below as well
    star2 = 1 #Same here

    while star1 < len(listwithxytuples)-1:
        screenX1 = listwithxytuples[star1][0] * (WIDTH / 2) + WIDTH/2 
        screenY1 = listwithxytuples[star1][1] * (HEIGHT / 2) + HEIGHT/2 
        screenX2 = listwithxytuples[star2][0] * (WIDTH / 2) + WIDTH/2 
        screenY2 = listwithxytuples[star2][1] * (HEIGHT / 2) + HEIGHT/2 
        
        pointer.goto(screenX1,screenY1)
        pointer.down()
        pointer.goto(screenX2,screenY2)
        pointer.up()
         
        star1 = star1 + 2
        star2 = star1 + 1

#Purpose: Create orange borders around the constellations without changing other functions as specified on assignment page. This function is called in main().
#Parameters: constellationNames, edgesList, namedStars, pointer
#Return: none    
def bordersBox(constellationNames, edgesList, namedStars, pointer):
    BORDERCOLOR = "orange"    
    listwithxytuples = []
    helper_tuple_3 = (0,0,0) #putting x,y,mag into but then only using [0] and [1]
    allX = []
    allY = []
    
    for starset in edgesList: 
        helper_tuple_3 = namedStars.get(starset[0])
        listwithxytuples.append(helper_tuple_3)
        helper_tuple_3 = namedStars.get(starset[1])
        listwithxytuples.append(helper_tuple_3)

    star1 = 0 
    star2 = 1 
 
    while star1 < len(listwithxytuples)-1:
        screenX1 = float(listwithxytuples[star1][0]) * (WIDTH / 2) + WIDTH/2 
        screenY1 = float(listwithxytuples[star1][1]) * (HEIGHT / 2) + HEIGHT/2 
        screenX2 = float(listwithxytuples[star2][0]) * (WIDTH / 2) + WIDTH/2 
        screenY2 = float(listwithxytuples[star2][1]) * (HEIGHT / 2) + HEIGHT/2 
   
        allX.append(screenX1)
        allX.append(screenX2)
        allY.append(screenY1)
        allY.append(screenY2)
        
        star1 = star1 + 2
        star2 = star1 + 1
    
    xmin = float(min(allX))
    xmax = float(max(allX))
    ymin = float(min(allY))
    ymax = float(max(allY))

    textSize = 10 #Drawing an orange box around constellations counterclockwise and labelling at top middle
    pointer.color(BORDERCOLOR)
    pointer.up()
    pointer.goto(xmin,ymin)
    pointer.down()
    pointer.goto(xmax,ymin)
    pointer.goto(xmax,ymax)
    pointer.goto(xmin,ymax)
    pointer.goto(xmin,ymin)
    pointer.up()
    pointer.goto(xmin + ((xmax-xmin)/2), ymax + TEXTGAP/2)
    pointer.write(constellationNames, font=("Arial", textSize), align="center")
    
    writeOut = open(f"{constellationNames}_box.dat", "w")
    writeOut.write(f"{constellationNames}\n{xmin}, {xmax}, {ymin}, {ymax}")
    writeOut.close()


#Purpose: Set up the turtle window with (0,0) as the bottom left and (600,600) as the top right 
#Parameters: none
#Return: pointer
def setup():
    pointer = turtle.Turtle()
    screen = turtle.getscreen()
    screen.setup(WIDTH, HEIGHT, 0, 0)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    pointer.hideturtle()
    screen.delay(delay=0)
    turtle.bgcolor(BACKGROUNDCOLOR)
    pointer.up()
    return pointer

#Purpose: The main function that calls functions, catch returns and pass parameters to other functions to plot stars and constellations. Loop for constellation prompt, drawing constellations and the borders drawing is here, as well as error handling for incorrect constellation prompts or opening/closing files.
#Parameters: none 
#Return: none
def main():
    pointer = setup() #The order of these calls were changed from the startercode to allow handleArguments() to error handle stars location file inputs properly!!
    drawAxes(pointer)
    starsLocationFile = handleArguments(pointer)
    noNameStars, namedStars = readStarFiles(starsLocationFile) #Read star information from file (function)
    drawStars(noNameStars, namedStars, pointer)

    constellationFileName = input("Enter constellation filename: ")
    
    CONSTELLATIONCOLOR1 = "red"
    CONSTELLATIONCOLOR2 = "green"
    CONSTELLATIONCOLOR3 = "yellow"

    counter = 0
    while constellationFileName != "":  
        if counter % 3 == 0:
            pointer.color(CONSTELLATIONCOLOR1)
        elif counter % 3 == 1: 
            pointer.color(CONSTELLATIONCOLOR2)
        else:  
            pointer.color(CONSTELLATIONCOLOR3)
        try: #This try checks if the input is valid, then if it isn't then the user is told it was not valid and reprompted. 
            constellationsOpen = open(constellationFileName, "r")

            constellationsLines = constellationsOpen.readlines()    
       
            constellationNames, edgesList = readConstellationFiles(constellationsLines)
            
            drawConstellation(constellationNames, edgesList, namedStars, pointer) #Draw constellations between each prompt
            
            bordersBox(constellationNames, edgesList, namedStars, pointer) #Draw borders immediately after constellations
            
            constellationFileName = input("Enter constellation filename: ")
            
            counter = counter + 1
        except: #Goes here when (os.path.isfile(constellationsOpen) == False) which means the entry was invalid
            constellationFileName = input("Your file input is invalid. Enter another constellation filename: ")
        
    
main()
