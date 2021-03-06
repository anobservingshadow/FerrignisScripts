import random
from collections import Counter
import pandas as pd
import xlsxwriter

def genTerPossList(usedTerList):
    #This is a function that generates a Terrain Possibility List.
    #It takes the list of Terrain Objects that are being used, then appends their name the default number of times
    #It then returns the generated list
    terPossList = []
    for terrain in usedTerList:
        for i in range(terrain.default):
            terPossList.append(terrain.name)
    return terPossList

def chooseTerrain(maplist,xcoord,ycoord,usedTerList,terPossList):
    #This function chooses a Terrain type according to two factors:
    # 1. The existing Terrain Possibility List, and
    # 2. The surrounding blocks (since it's generated by row, this only looks at the top and top left cells in a 5x5 square (total of 12 cells))
    surroundCount = checkSurround(maplist,xcoord,ycoord)
    tempPossList = list(terPossList)
    terPossCount = Counter(terPossList)
    for Terrain in usedTerList:
        tempPossList = Terrain.surroundEdit(surroundCount,tempPossList)
    # So, the temporary Terrain Possibility List has been edited to reflect the possibility given the surrounding blocks, and now a type is chosen
    chosenTerrain = random.choice(tempPossList)
    # The way I've handled negative probability is by adding a '-' in front of the Terrain type (e.g. '-Grass')
    # So this makes sure one of the negative possibilities isn't chosen
    while chosenTerrain[0] == "-":
        chosenTerrain = random.choice(tempPossList)
    # And here the overall Terrain Possibility List is updated according to the chosen type
    for Terrain in usedTerList:
        terPossList = Terrain.updatePossList(chosenTerrain,terPossCount,terPossList)
    return chosenTerrain

def checkContents(maplist,xcoord,ycoord):
    # This is a function that attempts to check the Terrain type in a cell
    try:
        terrain = maplist[xcoord][ycoord]
    except IndexError:
        terrain = "N/A"
        pass
    return terrain

def checkSurround(maplist,xcoord,ycoord):
    # This is a function that checks the surrounding boxes and returns a Counter (type of dict for counting occurrences in an iterable)
    # to be passed to the different Terrain classes
    surroundList = []
    mask = [[-2,-2],[-2,-1],[-2,0],[-2,1],[-2,2],[-1,-2],[-1,-1],[-1,0],[-1,1],[-1,2],[0,-2],[0,-1]]
    mapcoords = [[coord[0]+xcoord,coord[1]+ycoord] for coord in mask]
    # After calculating the coordinates of all the nearby already filled-in cells, each cell is then checked and added to the list
    for coords in mapcoords:
        check = checkContents(maplist,coords[0],coords[1])
        surroundList.append(check)
    # And then the Counter is returned
    return Counter(surroundList)

class Terrain:
    # This is the base Terrain class
    def __init__(self):
        self.name = "ThisShouldNotExist"

    def getName(self):
        # This is a function that never gets called because I forgot I made it
        return self.name
    
    def addToList(self,terList,NoOfTimes):
        # This is a function made to increase a Terrain's probability by either appending an instance of its name to the
        # Terrain Possibility List, or removing a negative instance of its name
        for x in range(NoOfTimes):
            if str("-"+self.name) in terList:
                terList.remove(str("-"+self.name))
            else:
                terList.append(self.name)
    
    def removeFromList(self,terList,NoOfTimes):
        # This is a function made to decrease a Terrain's probability by either removing an instance of its name to the
        # Terrain Possibility LIst, or appending a negative instance of its name
        for x in range(NoOfTimes):
            try:
                terList.remove(self.name)
            except ValueError:
                terList.append("-"+self.name)
    
class Grass(Terrain):
    # This is a Terrain Class, for the Terrain-type 'Grass' in this case.
    # The initialised values are, in order:
    # - the name (used for editing the Terrain Possibility List)
    # - the default number of instances in the 
    def __init__(self):
        self.name = "Grass"
        self.default = 30
        self.minval = 20
        self.maxval = 200
        self.surrappval = 1
        self.updappval = 4
        self.updremval = 2
    
    def surroundEdit(self,surroundCount,tempPossList):
        if surroundCount[self.name] >= 1:
            self.addToList(tempPossList,self.surrappval)
        return tempPossList
    
    def updatePossList(self,chosenTerrain,terPossCount,terPossList):
        possValue = terPossCount[self.name]
        if chosenTerrain == self.name:
            if possValue < self.minval+self.updremval:
                self.removeFromList(terPossList,possValue-self.minval)
            else:
                self.removeFromList(terPossList,self.updremval)
        else:
            if possValue+self.updappval > self.maxval:
                self.addToList(terPossList,self.maxval-possValue)
            else:
                self.addToList(terPossList,self.updappval)
        return terPossList
            
class Dirt(Terrain):
    def __init__(self):
        self.name = "Dirt"
        self.default = 15
        self.minval = 5
        self.maxval = 50
        self.updappval = 1
        self.updremval = 1
    
    def surroundEdit(self,surroundCount,tempPossList):
        return tempPossList
    
    def updatePossList(self,chosenTerrain,terPossCount,terPossList):
        possValue = terPossCount[self.name]
        if chosenTerrain == self.name:
            if possValue < self.minval+self.updremval:
                self.removeFromList(terPossList,possValue-self.minval)
            else:
                self.removeFromList(terPossList,self.updremval)
        else:
            if possValue+self.updappval > self.maxval:
                self.addToList(terPossList,self.maxval-possValue)
            else:
                self.addToList(terPossList,self.updappval)
        return terPossList

class Bush(Terrain):
    def __init__(self):
        self.name = "Bush"
        self.default = 5
        self.updappval = 1
        self.updremval = 4
    
    def surroundEdit(self,surroundCount,tempPossList):
        surrBush = surroundCount[self.name]
        surrRock = surroundCount["Rock"]
        if surrBush >= 1:
            self.addToList(tempPossList,surrBush*3)
        if surrRock >= 1:
            self.removeFromList(tempPossList,surrRock*2)
        return tempPossList
    
    def updatePossList(self,chosenTerrain,terPossCount,terPossList):
        possValue = terPossCount[self.name]
        if chosenTerrain == self.name:
            self.removeFromList(terPossList,self.updremval)
        else:
            self.addToList(terPossList,self.updappval)
        return terPossList

class Tree(Terrain):
    def __init__(self):
        self.name = "Tree"
        self.default = 3
        self.surrremval = 15
        self.updappval = 1
        self.updremval = 6
    
    def surroundEdit(self,surroundCount,tempPossList):
        surrTree = surroundCount[self.name]
        if surrTree >= 1:
            self.removeFromList(tempPossList,self.surrremval*surrTree)
        return tempPossList
    
    def updatePossList(self,chosenTerrain,terPossCount,terPossList):
        possValue = terPossCount[self.name]
        if chosenTerrain == self.name:
            self.removeFromList(terPossList,self.updremval)
        else:
            self.addToList(terPossList,self.updappval)
        return terPossList

class Rock(Terrain):
    def __init__(self):
        self.name = "Rock"
        self.default = 6
        self.minval = 1
        self.maxval = 7
        self.updappval = 2
        self.updresetval = 1
    
    def surroundEdit(self,surroundCount,tempPossList):
        return tempPossList
    
    def updatePossList(self,chosenTerrain,terPossCount,terPossList):
        possValue = terPossCount[self.name]
        if chosenTerrain == self.name:
            self.removeFromList(terPossList,possValue-self.updresetval)
        else:
            if possValue+self.updappval > self.maxval:
                self.addToList(terPossList,self.maxval-possValue)
            else:
                self.addToList(terPossList,self.updappval)
        return terPossList

def FrameFormatter(cellvalue):
    colorDict = {"Grass":"#6be12f","Dirt":"#b82828","Bush":"#49a52c","Tree":"#d28443","Rock":"#9a9a9a"}
    return f"color:{colorDict[cellvalue]};background-color:{colorDict[cellvalue]}"

def GenerateMap(usedTerList,maplength):
    maplist = []
    terPossList = genTerPossList(usedTerList)
    for row in range(maplength):
        maplist.append([])
        for column in range(maplength):
            maplist[row].append(chooseTerrain(maplist,row,column,usedTerList,terPossList))
            random.shuffle(terPossList)
    print("Terrain Possibilities List")
    print(Counter(terPossList))
    fullcounter = Counter([])
    for row in maplist:
        fullcounter = fullcounter + Counter(row)
    print("Overall Amount of Each Terrain")
    print(fullcounter)
    return maplist

usedTerList = [Grass(),Bush(),Tree(),Rock()]
BasicFrame = pd.DataFrame(data=GenerateMap(usedTerList,50))
OutputFrame = BasicFrame.style.applymap(FrameFormatter)
writer = pd.ExcelWriter("Map1.xlsx",engine="xlsxwriter")
OutputFrame.to_excel(writer,index=False,header=False)
worksheet = writer.sheets["Sheet1"]
worksheet.set_default_row(36)
worksheet.set_column(0,len(OutputFrame.columns)-1,5.56)
writer.save()