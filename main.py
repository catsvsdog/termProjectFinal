from cmu_graphics import *
#from interface2 import *
from loadImageFunction import loadImage
#from itemObject import Item
import os
from PIL import Image, ImageDraw,ImageFont
from clothingObjects import Item
import datetime
from outfitGenerator import get_calendar_data, generateAllGoodOutfits, get4UserPreferredOutfits, recycleDisplayedOutfits, get4Outfits, getSeasonTops, getSeasonBottoms, getSeasonFromTemp

def get_current_directory():
  return os.getcwd()

def construct_file_path(directory, filename):
  return os.path.join(directory, filename)
#source: https://www.geeksforgeeks.org/os-module-python-examples/ + chatgpt

def onAppStart(app):
   # app.url = "\Users\\irisy\\Downloads\\cropflower.png"
    # current_dir is term-project-v2 directory
    #images
    current_dir = get_current_directory()
    app.b1 = construct_file_path(current_dir, 'item.png')
    app.b2 = construct_file_path(current_dir, 'outfit.png')
    app.b3 = construct_file_path(current_dir, 'closet.png')
    app.dislike = construct_file_path(current_dir, 'dislike.jpg')
    app.url = construct_file_path(current_dir, "start.png")

    '''    
    image sources: https://shopee.tw/buyer/login?next=https%3A%2F%2Fshopee.tw%2FCNN-%E4%BA%92%E5%8B%95%E8%8B%B1%E8%AA%9E-%E9%9B%9C%E8%AA%8C-%E9%9B%9C%E8%AA%8C%E5%96%AE%E6%9C%AC-%E6%9C%97%E8%AE%80CD%E7%89%88-%E9%81%8E%E5%88%8A-2018%E5%B9%B48-11%E6%9C%88-2019%E5%B9%B41-2%E6%9C%88-%E9%BB%9E%E8%AE%80%E7%89%88-i.291477252.25356590599%3Fsp_atk%3D0d94157f-a510-4f15-8339-201b6580fb4d%26xptdk%3D0d94157f-a510-4f15-8339-201b6580fb4d
    https://pin.it/4Nf59G5Rt
    https://images.app.goo.gl/7KPUozcbYxDXsTEWA
    https://www.maryandjarvis.com/post/10-steps-to-turn-your-closet-into-your-everyday-ally
    '''

    app.width = 900
    app.height = 650
    app.scrollOffset = 0


    #toggles
    app.itemMode = False
    app.addItemMode = False
    app.files = None
    app.genMode = False
    app.warMode = False
    app.home = True
    app.moveOn = False
    app.done = False
    app.finDone = False
    
    #Colors
    app.bgCol = rgb(129,137,120)
    app.gray = rgb(100,100,100) 
    app.lightg = rgb(173,173,173)
    app.buttonCol = rgb(109, 119, 99)

    app.numCols = 4
    app.itemSize = (app.width//app.numCols, 230) 
    app.itemsPerRow = app.numCols
    app.items = []
    app.noFiles = True
    app.images = None
    
    app.word = "Enter here:"
    app.type = False
    app.targetSeason = ""

    app.typeC = ""
    app.tops = []
    app.bottoms = []
    app.seen = []
    app.rename = False
    app.curr = ""
    app.recycled = []
    app.stepsPerSecond = 60

    app.offset = 30
    app.saved_outfits = []
    app.userPrefMode = False
    app.userPrefColors = []
    app.my_good_outfits = []
    app.displayed_outfits = []

    #get date --chat gpt
    app.current_date = datetime.date.today()
    app.month = app.current_date.month
    app.year = app.current_date.year
    app.title = f"{app.current_date.strftime('%B %Y')}"

    #calendar variables
    app.calendarOutfits = {} 
    app.outfitsAvailable = []
    app.outfitsWorn = []
    app.calendarMode = False
    app.selectedOutfit = None
    app.addToCalendar = False
    app.added = False
    app.day = ""
    app.needsWash = False


def drawButton(x, y, width, height, radius, fill='black'):
    drawRect(x + radius, y, width - 2 * radius, height, fill=fill)
    drawRect(x, y + radius, width, height - 2 * radius, fill=fill)
    drawCircle(x + radius, y + radius, radius, fill=fill)
    drawCircle(x + width - radius, y + radius, radius, fill=fill) 
    drawCircle(x + radius, y + height - radius, radius, fill=fill)
    drawCircle(x + width - radius, y + height - radius, radius, fill=fill) 

def get_row_and_col(index, cols):
    return index//cols, index % cols


#start screen
def start_redrawAll(app):
    draw_background(app.width, app.height, app.bgCol)
    drawImage(app.url, 620,300, align = "center", width = 400, height = 400)
    drawStar(480, 180, 20, 4, fill = "white", roundness = 50)
    drawStar(730, 410, 20, 4, fill = "white", roundness = 50)
    drawLabel("Welcome to ", 280, 290, size = 50, fill = "white", align = "center", font ="Lora")
    drawLabel("Outfit Planner", 300, 350, size = 55, fill = "white", align = "center", font ="Lora")
    drawButton(287.5 - 90, 397 + 20, 205-30,65-10,20, fill = "white")
    drawButton(290 -90,400 + 20,200-30,60-10,20,fill = app.buttonCol)
    drawLabel("Start", 280, 445, size = 25, fill = "white", bold = True, font = "Lora", align = "center")

#switch to item screen
def start_onMousePress(app,mouseX,mouseY):
    if (mouseX >= 198 and mouseX <= 372) and (mouseY >= 416 and mouseY <= 472):
        setActiveScreen("item")

def main_redrawAll(app):
    draw_background(app.width, app.height, app.bgCol)
    drawLabel("Select One: ", 300, 200, size = 50, fill = "white", font = "Lora", align = "center" )
    #add item
    drawImage(app.b1, 200, 400, align = "center", width = 250, height = 250) 
    drawLabel("Add an item", 170, 540, align = "center", fill = "white", size = 25, font = "Lora")
    drawLine(90, 555, 250, 555, fill = "white")
    #create outfit
    drawImage(app.b2, 460, 400, align = "center", width = 250, height = 250)
    drawLabel("Create an Outfit", 450, 540, align = "center", fill = "white", size = 25, font = "Lora")
    drawLine(350, 555, 550, 555, fill = "white")
    #wardrobe
    drawImage(app.b3, 720, 400, align = "center", width = 250, height = 250)
    drawLabel("Wardrobe", 700, 540, align = "center", fill = "white", size = 25, font = "Lora")
    drawLine(640, 555, 760, 555, fill = "white")

def main_onMousePress(app, mouseX, mouseY):
    if (mouseX >= 90 and mouseX <= 250) and (mouseY >= 530 and mouseY <= 555):
        setActiveScreen("item")
    if (mouseX >= 350 and mouseX <= 550) and (mouseY >= 530 and mouseY <= 555):
        if Item.instances["top"] != set() and Item.instances["bottom"] != set():
            print("insance: ", Item.instances)
            if app.my_good_outfits == [] and app.displayed_outfits == []:
                app.my_good_outfits = generateAllGoodOutfits(Item.instances['top'], Item.instances['bottom'])
                if app.my_good_outfits != []:
                    unique_list = list(dict.fromkeys(app.my_good_outfits))
                    app.my_good_outfits = unique_list 
                    get4Outfits(app.my_good_outfits, app.displayed_outfits)
            setActiveScreen("gen")
        else:
            setActiveScreen("noOutfits")
        
    if (mouseX >= 640 and mouseX <= 760) and  (mouseY >= 530 and mouseY <= 555):
        setActiveScreen("wardrobe")

#no possible outftis screen
def noOutfits_redrawAll(app):
    drawLine(150, 140, 750, 140, fill="white", lineWidth=2)
    draw_background(app.width, app.height, app.bgCol)
    drawLabel("No outfits right now, click to update wardrobe!", 150, 180, size = 30, align = "left", fill = "white", font = "Lora", bold= True)
    drawButton(450 - 30, 300,50, 50, 5, fill = app.lightg)
    drawLine(450 - 30, 325, 500-30, 325, fill = "white")
    drawLine(475 - 30, 300, 475-30, 350, fill = "white")
    drawLabel("Back", 80,80,align = "center", fill = "white", font = "Lora", size = 20)

def noOutfits_onMousePress(app, mouseX, mouseY):
    if (mouseX >= 50 and mouseX <= 100) and (mouseY >= 60 and mouseY <= 100):
        setActiveScreen("main")
    elif (mouseX >= 325 and mouseX <= 450) and (mouseY >= 300 and mouseY <= 350):
        setActiveScreen("wardrobe")

#Item screen
def item_redrawAll(app):
    draw_background(app.width, app.height, app.bgCol)
    drawLabel("Add an item", 450, 90, align = "center", size = 30, font = "Lora", bold = True, fill = "white")
    drawLine(150, 140, 750, 140, fill="white", lineWidth=2)
    drawRect(300,180, 300, 350, fill = None, border = "white", borderWidth = 3)
    drawButton(347.5,298,205,65,20,fill = "white")
    drawButton(350,300,200,60,20,fill = app.buttonCol )
    drawLabel("Upload files", 450, 330, align = "center", font = "Lora", fill = "white", size = 25)
    drawLabel("Back", 50+30,50+30,align = "center", fill = "white", font = "Lora", size = 20)

def item_onMousePress(app, mouseX, mouseY):
    if (mouseX >= 347.5 and mouseX <= 347.5 + 205) and (mouseY >= 298 and mouseY <= 298 + 65):
        if app.files != None:
            app.showMessage("Already uploaded!")
        while app.files == None:
            file_path = app.getTextInput("Enter the path of the file to read: ")
            print(os.path)
            if file_path and os.path.exists(file_path):
                app.files = file_path
                print(app.files)
            else:
                app.showMessage("Invalid path! Please enter a valid directory.")
                app.files == None
        try:
            
            current_dir = get_current_directory()  # Custom function to get current directory
            output_dir = construct_file_path(current_dir, 'processed')
            os.makedirs(output_dir, exist_ok=True)  # Create output folder if it does not exist
            
            app.images = loadImage(app.files, output_dir)
            
            for image_path in app.images: 
                Item(image_path, "", (0, 0), (200, 200), set(), set(), '', None, image_path)
                
            app.noFiles = False
            setActiveScreen("wardrobe")
        except FileNotFoundError as unfound:
            app.showMessage(f"Error loading folder: {unfound}")

    elif (mouseX >= 50 and mouseX <= 110) and (mouseY >= 60 and mouseY <= 110):
        setActiveScreen("main")


#Wardrobe Screens
def wardrobe_redrawAll(app):
    if app.noFiles:
        # drawRect(0,0,app.width, app.height, fill = app.bgCol)
        drawLine(150, 140, 750, 140, fill="white", lineWidth=2)
        draw_background(app.width, app.height, app.bgCol)
        drawLabel("No clothes right now, click to upload!", 450, 120, size = 20, fill = "white", font = "Lora", bold= True)
        drawButton(450 - 30, 300,50, 50, 5, fill = app.lightg)
        drawLine(450 - 30, 325, 500-30, 325, fill = "white")
        drawLine(475 - 30, 300, 475-30, 350, fill = "white")
        drawLabel("Back", 80,80,align = "center", fill = "white", font = "Lora", size = 20)
    else:
        if app.files == None:
            pass
        else:
            for i, item in enumerate([item for temp in Item.instances.values() for item in temp]): #source: https://realpython.com/iterate-through-dictionary-python/
                # print("item name: ", item)
                row, col = get_row_and_col(i, app.numCols)
                itemWidth = 225
                itemHeight = item.size[1] + 50
                x = col * (app.itemSize[0])
                y = row * (itemHeight) + 130 - app.scrollOffset
                if (x + itemWidth > 0 and x < app.width) and (y + itemHeight > 130 and y < app.height):
                    drawRect(x, y, itemWidth, itemHeight, fill=None, border="black", borderWidth=0.5)
                    drawImage(item.image, x + item.size[0] / 2 + 20, y + item.size[1] / 2, 
                            align="center", width=item.size[0], height=item.size[1])
  
                    item.update_bounds(x, y, itemWidth, itemHeight)
        drawRect(0, 0, app.width, 130, fill='white')
        drawLabel("Wardrobe", 450, 50, size = 30, fill = "black", font = "Lora")
        drawLabel("Back", 50+30,50,align = "center", fill = "black", font = "Lora", size = 20)
        drawRect(0, 80, app.width//2, 50,fill = app.lightg, border='black', borderWidth = 0.5)
        drawRect(app.width//2, 80, app.width//2, 50, fill = None, border='black', borderWidth = 0.5)
        drawLabel('Items', app.width//4, 105, align='center', font = "Lora", size = 18, borderWidth = 0.5)
        drawLabel('Outfits', app.width//4*3, 105, align='center', font = "Lora", size = 18, borderWidth = 0.5)

def wardrobe_onMousePress(app, mouseX, mouseY):
    if (mouseX >= 50 and mouseX <= 110) and (mouseY >= 40 and mouseY <= 80):
        setActiveScreen("main") #change to main screen
    elif (mouseX >= 325 and mouseX <= 450) and (mouseY >= 300 and mouseY <= 350):
        if app.noFiles:
            setActiveScreen("item") #redirected to uploading files if no files
    elif (mouseX >= 0 and mouseX <= app.width//2) and (mouseY >= 80 and mouseY <= 130):
        setActiveScreen("wardrobe") #current screen
    elif (mouseX >= app.width//2 and mouseX <= app.width *2) and (mouseY >= 80 and mouseY <= 130):
        #switches to outfit generator screen if there are clothes
        if Item.instances['top'] != set() and Item.instances['bottom'] != set():
            app.my_good_outfits = generateAllGoodOutfits(Item.instances['top'], Item.instances['bottom'])
            if app.my_good_outfits != []:
                print("yreeeeee-------")
                unique_list = list(dict.fromkeys(app.my_good_outfits))
                app.my_good_outfits = unique_list 
                if app.displayed_outfits != []:
                    recycleDisplayedOutfits(app.displayed_outfits, app.recycled)
                get4Outfits(app.my_good_outfits, app.displayed_outfits)
                print("good outfits: ", app.my_good_outfits)
                print("displayedd: ", app.displayed_outfits)
                if app.displayed_outfits != []:
                    unique_list = list(dict.fromkeys(app.displayed_outfits))
                    app.displayed_outfits = unique_list 
            setActiveScreen("gen") #testing
        else:
            app.showMessage("Not enough clothing!")
    else:
        '''
        Iterate through each item to check if the click is within its bounds 
        to update clothing attributes '''
        for item in [item for temp in Item.instances.values() for item in temp]:
            if item.bounds is not None:  # Check if bounds are set
                x1, y1, x2, y2 = item.bounds  # Get the bounds of the item
                if (x1 <= mouseX and mouseX <= x2) and( y1 <= mouseY and mouseY <= y2 and mouseY >= 130):  # Check if mouse is inside the bounds
                    app.curr = item
                    if app.curr.name not in app.seen:
                        app.rename = False
                        app.typeC = ''
                        app.word = "Enter here:"
                        app.seen.append(app.curr.name)
                        setActiveScreen("nameItem") 
                    else:
                        app.rename = True
                        setActiveScreen("temp")

#scrolling through wardrobe
def wardrobe_onKeyPress(app, key):
    scrollStep = 10
    maxScroll = max(0, len(Item.instances) * 300 - (app.height - 150))  # --> chatgpt

    if key == "down":
        app.scrollOffset = min(app.scrollOffset + scrollStep, maxScroll)
    elif key == "up":
        app.scrollOffset = max(app.scrollOffset - scrollStep, 0)

#draws basic background layout
def draw_background(width, height, color):
    drawRect(0,0,width,height, fill = color)
    drawLine(0, 50, 900, 50, fill = "white", lineWidth = 4)
    drawLine(0, 600, 900, 600, fill = "white",lineWidth = 4)
    drawLine(50, 0, 50, 650, fill = "white", lineWidth = 4)
    drawLine(850, 0, 850, 650, fill = "white", lineWidth = 4)

#screen that displays the properties of the clothing that has been clicked
def temp_redrawAll(app):
    draw_background(app.width, app.height, app.bgCol)
    drawButton(200, 100, 500, 350, 20, fill = "white")
    drawButton(205, 105, 390 + 100, 290 + 50, 20, fill = app.bgCol)
    drawLabel("Click on what you wish to modify", 430, 150, size = 25, fill = "white", font= "Lora", bold = True)

    drawLabel(f"Name: {app.curr.name}", 230, 200, size = 20, fill = "white", font = "Lora", align = "left",bold = True)
    drawLabel(f"Color: {','.join(app.curr.color)}", 230, 250, size = 20, fill = "white", font = "Lora", align = "left",bold = True)
    drawLabel(f"Season: {','.join(app.curr.season)}", 230, 300, size = 20, fill = "white", font = "Lora", align = "left",bold = True)
    drawLabel(f"Fit: {app.curr.type}", 230, 350, size = 20, fill = "white", font = "Lora", align = "left",bold = True)

    drawLabel(f"Type: {app.curr.isTop}", 230, 400, size = 20, fill = "white", font = "Lora", align = "left",bold = True)
    drawLabel("Back", 50+30,50+30,align = "center", fill = "white", font = "Lora", size = 20)
    drawButton(497, 497.5, 205,65-10,10, fill = "white")
    drawButton(500,500,200,60-10,10,fill = app.buttonCol)
    drawLabel("Done", 570, 525, fill = "white", size = 25, font = "Lora", align = "center")

#allows user to modify each property
def temp_onMousePress(app, mouseX, mouseY):
    if (mouseX >= 230 and mouseX <= 420) and (mouseY >= 190 and mouseY <= 210):
        setActiveScreen("nameItem")
        app.rename = True
    if (mouseX >= 230 and mouseX <= 400) and (mouseY >= 245 and mouseY <= 260):
        setActiveScreen("colors")
    if (mouseX >= 230 and mouseX <= 450) and (mouseY >= 295 and mouseY <= 310):
        setActiveScreen("season")
    if (mouseX >= 230 and mouseX <= 300) and (mouseY >= 345 and mouseY <= 360):
        setActiveScreen("fit")
    # if (mouseX >= 230 and mouseX <= 300) and (mouseY >= 345 and mouseY <= 360):
    #     setActiveScreen("fit")
    if (mouseX >= 230 and mouseX <= 400) and (mouseY >= 395 and mouseY <= 410):
        setActiveScreen("type")
    if (mouseX >= 50 and mouseX <= 110) and (mouseY >= 60 and mouseY <= 110):
        setActiveScreen("wardrobe")
    if (mouseX >= 497 and mouseX <= 700) and (mouseY >= 500 and mouseY <= 550):
        app.rename = False
        setActiveScreen("wardrobe")

#naming each item
def nameItem_redrawAll(app):
    draw_background(app.width, app.height, app.bgCol)
    drawButton(200, 100, 500, 350, 20, fill = "white")
    drawButton(205, 105, 390 + 100, 290 + 50, 20, fill = app.bgCol)
    drawLabel("What brand is your item?", 430, 180, size = 30, fill = "white", font= "Lora", bold = True)
    drawButton(240, 250, 400, 50, 10, fill = app.buttonCol)
    drawLabel(f"{app.word}", 250, 275, fill = "white", size = 25, font = "Lora", align = "left", bold = True)
    drawStar(170, 180, 20, 4, fill = "white", roundness = 50)
    drawStar(730, 410, 20, 4, fill = "white", roundness = 50)
    drawButton(287.5 +40, 337+10, 205,65-10,10, fill = "white")
    drawButton(290+40,340+10,200,60-10,10,fill = app.buttonCol)
    drawLabel("Next", 380, 375, fill = "white", size = 25, font = "Lora", align = "center")
    drawLabel("Back", 50+30,50+30,align = "center", fill = "white", font = "Lora", size = 20)

def nameItem_onMousePress(app, mouseX, mouseY):
    if (mouseX >= 240 and mouseX <= 640) and (mouseY >= 250 and mouseY <= 300):
        app.type = True
        app.word = ""
    if (mouseX >= 328 and mouseX <= 530) and (mouseY >= 350 and mouseY <= 400):
        if app.word != "Enter here:":
            app.curr.name = app.word
            app.seen[-1] = app.curr.name
            if app.rename:
                setActiveScreen("temp")
            else:
                setActiveScreen("season")
    if (mouseX >= 50 and mouseX <= 110) and (mouseY >= 60 and mouseY <= 110):
        if app.rename:
            # print("new: ", app.word)
            setActiveScreen("temp")
        else:
            setActiveScreen("wardrobe")
        
def nameItem_onKeyPress(app, key):
    if app.type:
        if len(key) == 1 and key.isalpha():
            app.word += key
        if key == "backspace":
            app.word = app.word[:-1]

#selecting the season
def season_redrawAll(app):
    buttonCol = rgb(109, 119, 99)
    # drawRect(0,0,app.width,app.height, fill = app.bgCol)
    # drawLine(0, 50, 900, 50, fill = "white", lineWidth = 4)
    # drawLine(0, 600, 900, 600, fill = "white",lineWidth = 4)
    # drawLine(50, 0, 50, 650, fill = "white", lineWidth = 4)
    # drawLine(850, 0, 850, 650, fill = "white", lineWidth = 4)
    draw_background(app.width, app.height, app.bgCol)
    drawButton(200, 100, 500, 350, 20, fill = "white")
    drawButton(205, 105, 390 + 100, 290 + 50, 20, fill = app.bgCol)
    drawLabel("What season is your item?", 430, 180-30, size = 30, fill = "white", font= "Lora", bold = True)
    drawLabel("(can select multiple)", 430, 220-30, size = 25, fill = "white", font = "Lora", bold=True)
    #drawButton(240, 250, 400, 50, 10, fill = buttonCol)
    drawButton(210 + 50, 337 - 40, 150, 65 - 10, 10, fill="white")
    if "spring" in app.curr.season:
        buttonCol = rgb(173,173,173)
    else:
        buttonCol = rgb(109, 119, 99)
    drawButton(212 + 50, 340 - 40, 147, 60 - 10, 10, fill=buttonCol)
    drawLabel("Spring", 210 + 50 + 75, 337 - 40 + 27, fill="white", font="Lora", size=20)  # Adjusted label position

    # Summer Button
    if "summer" in app.curr.season:
        buttonCol = rgb(173,173,173)
    else:
        buttonCol = rgb(109, 119, 99)
    drawButton(210 + 50, 337 - 110, 150, 65 - 10, 10, fill="white")
    drawButton(212 + 50, 340 - 110, 147, 60 - 10, 10, fill=buttonCol)
    drawLabel("Summer", 210 + 50 + 75, 337 - 110 + 27, fill="white", font="Lora", size=20)  # Adjusted label position

    if "autumn" in app.curr.season:
        buttonCol = rgb(173,173,173)
    else:
        buttonCol = rgb(109, 119, 99)
    drawButton(210 + 250, 337 - 40, 150, 65 - 10, 10, fill="white")
    drawButton(212 + 250, 340 - 40, 147, 60 - 10, 10, fill=buttonCol)
    drawLabel("Autumn", 210 + 250 + 75, 337 - 40 + 27, fill="white", font="Lora", size=20)  # Adjusted label position

    if "winter" in app.curr.season:
        buttonCol = rgb(173,173,173)
    else:
        buttonCol = rgb(109, 119, 99)
    drawButton(210 + 250, 337 - 110, 150, 65 - 10, 10, fill="white")
    drawButton(212 + 250, 340 - 110, 147, 60 - 10, 10, fill=buttonCol)
    drawLabel("Winter", 210 + 250 + 75, 337 - 110 + 27, fill="white", font="Lora", size=20)  # Adjusted label position

    drawStar(170, 180, 20, 4, fill = "white", roundness = 50)
    drawStar(730, 410, 20, 4, fill = "white", roundness = 50)
    drawButton(287.5 +40, 337+30, 205,65-10,10, fill = "white")
    nextCol = rgb(109, 119, 99)
    drawButton(290+40,340+30,200,60-10,10,fill = nextCol)
    drawLabel("Next", 380, 375+20, fill = "white", size = 25, font = "Lora", align = "center")
    drawLabel("Back", 50+30,50+30,align = "center", fill = "white", font = "Lora", size = 20)
    
def season_onMousePress(app, mouseX, mouseY):
    if (mouseX >= 260 and mouseX <= 410) and (mouseY >= 230 and mouseY <= 280):
        if "summer" in app.curr.season:
            app.curr.season.remove("summer")
        else:
            app.curr.season.add("summer")
    if (mouseX >= 260 and mouseX <= 410) and (mouseY >= 300 and mouseY <= 350):
        if "spring" in app.curr.season:
            app.curr.season.remove("spring")
        else:
            app.curr.season.add("spring")
    if (mouseX >= 460 and mouseX <= 610) and (mouseY >= 230 and mouseY <= 280):
        if "Winter" in app.curr.season:
            app.curr.season.remove("winter")
        else:
            app.curr.season.add("winter")
    if (mouseX >= 460 and mouseX <= 610) and (mouseY >= 300 and mouseY <= 350):
        if "Autumn" in app.curr.season:
            app.curr.season.remove("autumn")
        else:
            app.curr.season.add("autumn")
    if app.curr.season != set(): app.moveOn = True
    if (mouseX >= 328 and mouseX <= 530) and (mouseY >= 370 and mouseY <= 420):
        if app.moveOn:
            if app.rename:
                setActiveScreen("temp")
            else:
                setActiveScreen("colors")
    if (mouseX >= 50 and mouseX <= 110) and (mouseY >= 60 and mouseY <= 110):
        if app.rename:
            setActiveScreen("temp")
        else:
            setActiveScreen("nameItem")

#selecting color
def colors_redrawAll(app):
    buttonCol = rgb(109, 119, 99)
    bgCol = rgb(129, 137, 120)  # Sage green
    # drawRect(0,0,app.width,app.height, fill = app.bgCol)
    # drawLine(0, 50, 900, 50, fill = "white", lineWidth = 4)
    # drawLine(0, 600, 900, 600, fill = "white",lineWidth = 4)
    # drawLine(50, 0, 50, 650, fill = "white", lineWidth = 4)
    # drawLine(850, 0, 850, 650, fill = "white", lineWidth = 4)
    draw_background(app.width, app.height, app.bgCol)
    drawButton(200, 100, 500, 350, 20, fill = "white")
    drawButton(205, 105, 390 + 100, 290 + 50, 20, fill = app.bgCol)

    drawLabel("What color is your item?", 430, 180-30, size = 30, fill = "white", font= "Lora", bold = True)
    drawLabel("(can select multiple)", 430, 220-30, size = 25, fill = "white", font = "Lora", bold=True)
    lightBlue = rgb(102, 163, 212)
    gray = rgb(92,92,92)
    beige = rgb(207,195,175)
    lightGray = rgb(194,194,194)
    brown = rgb(74,46,10)
    orange = rgb(215,121,40)
    pink = rgb(215,121,158)
    colors = ["black", brown, "blue",lightBlue, "purple", pink, orange]
    col = ["green", "yellow", "red", gray, beige, "white", lightGray]
    selectedCol = rgb(109, 119, 99)
    j = 0
    for i in range(200, 680, 70):
        drawButton(20 + i, 250, 40, 40, 10, fill = colors[j])
        j += 1
    j = 0
    for i in range(200, 680, 70):
        drawButton(20 + i, 300, 40, 40, 10, fill = col[j])
        j +=1 
    drawStar(170, 180, 20, 4, fill = "white", roundness = 50)
    drawStar(730, 410, 20, 4, fill = "white", roundness = 50)
    drawButton(287.5 +40, 337+30, 205,65-10,10, fill = "white")
    drawButton(290+40,340+30,200,60-10,10,fill = buttonCol)
    drawLabel("Next", 380, 375+20, fill = "white", size = 25, font = "Lora", align = "center")
    drawLabel("Back", 50+30,50+30,align = "center", fill = "white", font = "Lora", size = 20)

#determining which colors the user has clicked on
def colors_onMousePress(app, mouseX, mouseY):
    if (mouseY >= 250 and mouseY <= 290):
        if (mouseX >= 220 and mouseX <= 260):
            if "black" in app.curr.color:
                app.curr.color.remove("black")
            else:
                app.curr.color.add("black")
        if (mouseX >= 290 and mouseX <= 330):
            if "brown" in app.curr.color:
                app.curr.color.remove("brown")
            else:
                app.curr.color.add("brown")
        if (mouseX >= 360 and mouseX <= 400):
            if "blue" in app.curr.color:
                app.curr.color.remove("blue")
            else:
                app.curr.color.add("blue")
        if (mouseX >= 430 and mouseX <= 470):
            if "lightBlue" in app.curr.color:
                app.curr.color.remove("lightBlue")
            else:
                app.curr.color.add("lightBlue")
        if (mouseX >= 500 and mouseX <= 540):
            if "purple" in app.curr.color:
                app.curr.color.remove("purple")
            else:
                app.curr.color.add("purple")
        if (mouseX >= 570 and mouseX <= 610):
            if "pink" in app.curr.color:
                app.curr.color.remove("pink")
            else:
                app.curr.color.add("pink")
        if (mouseX >= 640 and mouseX <= 680):
            if "orange" in app.curr.color:
                app.curr.color.remove("orange")
            else:
                app.curr.color.add("orange")

    if (mouseY >= 300 and mouseY <= 340):
        if (mouseX >= 220 and mouseX <= 260):
            if "green" in app.curr.color:
                app.curr.color.remove("green")
            else:
                app.curr.color.add("green")
        if (mouseX >= 290 and mouseX <= 330):
            if "yellow" in app.curr.color:
                app.curr.color.remove("yellow")
            else:
                app.curr.color.add("yellow")
        if (mouseX >= 360 and mouseX <= 400):
            if "red" in app.curr.color:
                app.curr.color.remove("red")
            else:
                app.curr.color.add("red")
        if (mouseX >= 430 and mouseX <= 470):
            if "gray" in app.curr.color:
                app.curr.color.remove("gray")
            else:
                app.curr.color.add("gray")
        if (mouseX >= 500 and mouseX <= 540):
            if "beige" in app.curr.color:
                app.curr.color.remove("beige")
            else:
                app.curr.color.add("beige")
        if (mouseX >= 570 and mouseX <= 610):
            if "white" in app.curr.color:
                app.curr.color.remove("white")
            else:
                app.curr.color.add("white")
        if (mouseX >= 640 and mouseX <= 680):
            if "lightGray" in app.curr.color:
                app.curr.color.remove("lightGray")
            else:
                app.curr.color.add("lightGray")
    
    if app.curr.color != set():
        app.done = True
    else:
        app.done = False
    if (mouseX >= 328 and mouseX <= 530) and (mouseY >= 370 and mouseY <= 420):
        if app.done:
            if app.rename:
                setActiveScreen("temp")
            else:
                
                setActiveScreen("type")
    elif (mouseX >= 50 and mouseX <= 110) and (mouseY >= 60 and mouseY <= 110):
        if app.rename:
            setActiveScreen("temp")
        else:
            setActiveScreen("season")

#selecting if top or bottom
def type_redrawAll(app):
    buttonCol = rgb(109, 119, 99)
    # drawRect(0,0,app.width,app.height, fill = app.bgCol)
    # drawLine(0, 50, 900, 50, fill = "white", lineWidth = 4)
    # drawLine(0, 600, 900, 600, fill = "white",lineWidth = 4)
    # drawLine(50, 0, 50, 650, fill = "white", lineWidth = 4)
    # drawLine(850, 0, 850, 650, fill = "white", lineWidth = 4)
    draw_background(app.width, app.height, app.bgCol)
    drawButton(200, 100, 500, 350, 20, fill = "white")
    drawButton(205, 105, 390 + 100, 290 + 50, 20, fill = app.bgCol)
    drawLabel("Is your item a top or bottom?", 430, 180-30, size = 30, fill = "white", font= "Lora", bold = True)
    
    if "top" in app.typeC:
        buttonCol = rgb(173,173,173)
    else:
        buttonCol = rgb(109, 119, 99)
    drawButton(210 + 50, 250, 150, 65 - 10, 10, fill="white")
    drawButton(212 + 50, 253, 147, 60 - 10, 10, fill=buttonCol)
    drawLabel("Top", 210 + 50 + 75, 250 + 27, fill="white", font="Lora", size=20)  # Adjusted label position

    if "bottom" in app.typeC:
        buttonCol = rgb(173,173,173)
    else:
        buttonCol = rgb(109, 119, 99)
    drawButton(210 + 250, 250, 150, 65 - 10, 10, fill="white")
    drawButton(212 + 250, 253, 147, 60 - 10, 10, fill=buttonCol)
    drawLabel("Bottom", 210 + 250 + 75, 250 + 27, fill="white", font="Lora", size=20)  # Adjusted label position
    buttonCol = rgb(109, 119, 99)
    drawStar(170, 180, 20, 4, fill = "white", roundness = 50)
    drawStar(730, 410, 20, 4, fill = "white", roundness = 50)
    drawButton(287.5 +40, 337+30, 205,65-10,10, fill = "white")
    drawButton(290+40,340+30,200,60-10,10,fill = buttonCol)
    drawLabel("Next", 380, 375+20, fill = "white", size = 25, font = "Lora", align = "center")
    drawLabel("Back", 50+30,50+30,align = "center", fill = "white", font = "Lora", size = 20)

def type_onMousePress(app, mouseX, mouseY):
    if (mouseX >= 260 and mouseX <= 410) and (mouseY >= 250 and mouseY <= 300):
        app.typeC = ("top")
        #app.finDone = True
    if (mouseX >= 460 and mouseX <= 610) and (mouseY >= 250 and mouseY <= 300):
        app.typeC = ("bottom")
        #app.finDone = True
    if app.typeC != "":
        app.finDone = True
    if (mouseX >= 328 and mouseX <= 530) and (mouseY >= 370 and mouseY <= 420):
        if app.finDone:
            Item.instances[app.curr.isTop].remove(app.curr)
            Item.instances[app.typeC].add(app.curr)
            app.curr.isTop = app.typeC
            if app.rename:
                setActiveScreen("temp")
            else:
                setActiveScreen("fit")

    if (mouseX >= 50 and mouseX <= 110) and (mouseY >= 60 and mouseY <= 110):
        if app.rename:
            setActiveScreen("temp")
        else:
            setActiveScreen("colors")

#selecting fit; baggy, tight, or wellfit
def fit_redrawAll(app):
    draw_background(app.width, app.height, app.bgCol)
    drawButton(200, 100, 500, 350, 20, fill = "white")
    drawButton(205, 105, 390 + 100, 290 + 50, 20, fill = app.bgCol)
    drawLabel("Select the fit", 430, 180-30, size = 30, fill = "white", font= "Lora", bold = True)
    
    if "baggy" in app.curr.type:
        buttonCol = rgb(173,173,173)
    else:
        buttonCol = rgb(109, 119, 99)
    drawButton(210 + 50, 250-50, 150, 65 - 10, 10, fill="white")
    drawButton(212 + 50, 253-50, 147, 60 - 10, 10, fill=buttonCol)
    drawLabel("Baggy", 210 + 50 + 75, 250 + 27-50, fill="white", font="Lora", size=20)

    if "tight" in app.curr.type:
        buttonCol = rgb(173,173,173)
    else:
        buttonCol = rgb(109, 119, 99)
    drawButton(210 + 250, 250-50, 150, 65 - 10, 10, fill="white")
    drawButton(212 + 250, 253-50, 147, 60 - 10, 10, fill=buttonCol)
    drawLabel("Tight", 210 + 250 + 75, 250 + 27-50, fill="white", font="Lora", size=20)  
    
    if "well-fit" in app.curr.type:
        buttonCol = rgb(173,173,173)
    else:
        buttonCol = rgb(109, 119, 99)
    drawButton(210 + 150, 250 + 70-50, 150, 65 - 10, 10, fill="white")
    drawButton(212 + 150, 253 + 70-50, 147, 60 - 10, 10, fill=buttonCol)
    drawLabel("Well-fit", 210 + 150 + 75, 250 + 27 + 70-50, fill="white", font="Lora", size=20) 
    buttonCol = rgb(109, 119, 99)

    drawStar(170, 180, 20, 4, fill = "white", roundness = 50)
    drawStar(730, 410, 20, 4, fill = "white", roundness = 50)
    drawButton(287.5 +40, 337+30, 205,65-10,10, fill = "white")
    drawButton(290+40,340+30,200,60-10,10,fill = buttonCol)
    drawLabel("Next", 380, 375+20, fill = "white", size = 25, font = "Lora", align = "center")
    drawLabel("Back", 50+30,50+30,align = "center", fill = "white", font = "Lora", size = 20)
    
def fit_onMousePress(app, mouseX, mouseY):
    if (mouseX >= 260 and mouseX <= 410) and (mouseY >= 200 and mouseY <= 255):
        app.curr.type = "baggy"
    if (mouseX >= 460 and mouseX <= 610) and (mouseY >= 200 and mouseY <= 255):
        app.curr.type = "tight"
    if (mouseX >= 360 and mouseX <= 510) and (mouseY >= 270 and mouseY <= 325):
        app.curr.type = "well-fit"
    if (mouseX >= 50 and mouseX <= 110) and (mouseY >= 50 and mouseY <= 100):
        if app.rename:
            setActiveScreen("temp")
        else:
            setActiveScreen("type")
    # print(app.curr.type)
    if app.curr.type != "":
        if (mouseX >= 328 and mouseX <= 530) and (mouseY >= 370 and mouseY <= 420):
            if app.rename:
                setActiveScreen("temp")
            else:
                
                app.rename = True
                setActiveScreen("wardrobe")
  

#Generator
def gen_redrawAll(app):
    drawLabel("Generate Outfit!", 150, 50, size = 25, fill = app.gray, bold = True, font = "Lora", align = "left")
    drawLine(0, 90 ,app.width, 90, fill = app.gray, lineWidth = 2)
    drawLabel("Back", 50, 50,align = "center", fill = app.gray, font = "Lora", bold = True, size = 20)
    print("displayed outfits: ", app.displayed_outfits)
    print("recycled: ", app.recycled)
    print("my good outfits: ", app.my_good_outfits)
    #reached the point where there are no more possiblities
    if app.displayed_outfits == [] and app.recycled != []:
        x = (0 * 200) + 200 / 2
        drawButton(650, 503, 155, 50, 10, fill=app.lightg)
        drawButton(650, 500, 150, 50, 10, fill=app.bgCol)
        drawLabel("reset", 700, 525, size = 17, bold = True, fill = "white", font = "Lora")
        drawLabel("No more new outfits! Press reset to restart!", app.width // 2 + 50, app.height // 2, fill = app.gray, size = 20,bold = True, font = "Lora", align = "right")
    else:
        # print("displayed outfits in gen: ", app.displayed_outfits)
        for i, clothing in enumerate(app.displayed_outfits):
            print("clothing: ", clothing)
            row, col = get_row_and_col(i, app.numCols)
            itemWidth = 180 + 45
            itemHeight = 200
            x = (col * app.itemSize[0]) + itemWidth / 2
            y = row * itemHeight + 200

            if clothing.top:
                drawImage(clothing.top.serialNum, x, y + 40, align="center", width=170, height=170)
            if clothing.bottom:
                bottom = y + 170 + 20
                drawImage(clothing.bottom.serialNum, x, bottom, align="center", width=170, height=170)
                # add to outfits button
            drawButton(x - 75, 473, 155, 50, 10, fill=app.lightg)
            drawButton(x - 75, 470, 150, 50, 10, fill=app.bgCol)
            clothing.pos = (x, 550)
            drawLabel("add to outfits", x, 495, size=18, fill = "white" ,font="Lora", bold = True)
            drawImage(app.dislike, x, 550, align = "center", width = 50, height = 40)
    drawButton(650, 603-20, 155, 50, 10, fill = app.lightg)
    drawButton(650, 600-20, 150, 50, 10 ,fill = app.bgCol)
    drawLabel("regenerate", 720, 605, size=17, fill = "white", bold = True, font="Lora")

    drawLabel("My Outfits", 715, 50, size = 20, fill = app.gray, bold = True, font = "Lora")
    if app.displayed_outfits == [] and app.my_good_outfits == []:
        app.showMessage("No more possible outfits!")

def gen_onMousePress(app, mouseX, mouseY):
    buttonWidth, buttonHeight = 150, 50 
    imWidth, imHeight = 50, 40
    if (mouseX >= 30 and mouseX <= 80) and (mouseY >= 40 and mouseY <= 65):
        setActiveScreen("main")
    for clothing in app.displayed_outfits:
        buttonX, buttonY = clothing.pos  # Center position of the button
        imageX, imageY = clothing.pos
        iLeft = imageX - imWidth / 2
        iRight = imageX + imWidth / 2
        iTop = imageY - imHeight / 2
        iBottom = imageY + imHeight/2
        print(iLeft,iRight,iTop,iBottom)

        # Calculate button boundaries
        left = buttonX - buttonWidth / 2
        right = buttonX + buttonWidth / 2
        top = buttonY - buttonHeight / 2
        bottom = buttonY + buttonHeight / 2
        print(left,right,top,bottom)
        
        if (iLeft <= mouseX and mouseX <= iRight )and (iTop <= mouseY and mouseY <= iBottom):
            if clothing in app.saved_outfits:
                app.saved_outfits.remove(clothing)
            
            app.displayed_outfits.remove(clothing)

        # Check if the mouse click is within this button
        if (left <= mouseX and mouseX <= right) and (470 <= mouseY and mouseY <= 520):
            if clothing in app.saved_outfits:
               app.saved_outfits.remove(clothing)
            else:
                app.saved_outfits.append(clothing)
            
    if  app.saved_outfits != []:
        app.userPrefMode = True
    #resetting
    if (mouseX >= 650 and mouseX <= 800) and (mouseY >= 500 and mouseY <= 530):
        app.my_good_outfits = (app.recycled)
        app.recycled = []
        app.displayed_outfits = []
        
        for clothing in app.my_good_outfits:
           if clothing in app.saved_outfits:
              app.my_good_outfits.remove(clothing)
        res = get4Outfits(app.my_good_outfits, app.displayed_outfits)
        
        if res == None:
            app.showMessage("No more possible outfits!")
        if app.my_good_outfits != []:
            unique_list = list(dict.fromkeys(app.my_good_outfits))
            app.my_good_outfits = unique_list
    #regenerated 
    if (mouseX >= 675 and mouseX <= 825) and (mouseY >= 575 and mouseY <= 625):
        
        if app.userPrefMode:
            for outfit in app.saved_outfits:
               app.userPrefColors.append(outfit.getColor())
            res = get4UserPreferredOutfits(app.displayed_outfits, app.saved_outfits, app.userPrefColors)
            if res == None:
                app.showMessage("No more possible outfits for user preference!")
                recycleDisplayedOutfits(app.displayed_outfits, app.recycled)
                get4Outfits(app.my_good_outfits, app.displayed_outfits)
            else:
                for outfit in app.displayed_outfits:
                    if outfit in app.recycled:
                        app.displayed_outfits.remove(outfit)
       

        elif len(app.displayed_outfits) <= 1:
           app.showMessage("No more outfits!")
        else:
            prev = app.displayed_outfits
            recycleDisplayedOutfits(app.displayed_outfits, app.recycled)
            get4Outfits(app.my_good_outfits, app.displayed_outfits)
 

    if (mouseX >= 650 and mouseX <= 800) and (mouseY >= 30 and mouseY <= 80):
        setActiveScreen("outfits")
 
#displays outfits
def outfits_redrawAll(app):
    itemWidth = (app.width) // app.numCols  
    itemHeight = 150 
    overlapOffset = 70 
    
    rectHeight = itemHeight + itemHeight - overlapOffset
    drawLabel("Back", 50+30,50,align = "center", fill = app.gray, font = "Lora", size = 20)
    drawLabel("Outfits", 450, 50, size = 30, fill = app.gray, font = "Lora", bold = True)
    drawLabel("Calendar", 700, 50, size = 25, align = "left", fill = app.gray, font = "Lora")
    drawLine(0, 90, 900, 90, fill = app.gray, lineWidth = 2)
    if app.calendarMode:
       display = app.outfitsAvailable
    else:
       display = app.saved_outfits
    for i, clothing in enumerate(display):
        row, col = get_row_and_col(i, app.numCols)
        x = col * (itemWidth) 
        y = 250 + row * (rectHeight + 20) 
        drawRect(x, y, itemWidth, rectHeight, fill=None, border="black", borderWidth=0.5, align='left')
        drawImage(clothing.top.image, x, y - itemHeight / 2 + 40, align="left", width=itemWidth - 40, height=itemHeight)
        drawImage(clothing.bottom.image, x, y + itemHeight / 2 - overlapOffset + 20, align="left", width=itemWidth - 40, height=itemHeight)

def outfits_onMousePress(app, mouseX, mouseY):
    itemWidth = app.width // app.numCols  
    itemHeight = 150
    overlapOffset = 70
    rectHeight = itemHeight + itemHeight - overlapOffset
    if (mouseX >= 50 and mouseX <= 110) and (mouseY >= 40 and mouseY <= 100):
        app.calendarMode = False
        setActiveScreen("gen")
    if (mouseX >= 700 and mouseX <= 800) and (mouseY >= 40 and mouseY <= 100):
        app.outfitsAvailable = app.saved_outfits.copy()
        app.calendarMode = True
        setActiveScreen("calendar") #testing
    print("add? ", app.addToCalendar)
    print("outfits available: ", app.outfitsAvailable)
    if app.addToCalendar and app.outfitsAvailable != []:
        for i, clothing in enumerate(app.outfitsAvailable):
            row, col = get_row_and_col(i, app.numCols)
            x = col * itemWidth
            y = 250 + row * (rectHeight + 20) - 115
       
            if (x <= mouseX <= x + 225) and (y <= mouseY <= y + 230):
                app.selectedOutfit = clothing
                app.outfitsAvailable.remove(clothing)
                if app.outfitsAvailable == []:
                    app.needsWash = True
                app.outfitsWorn.append(clothing)
                app.added = True
                app.calendarOutfits[app.day] = app.selectedOutfit
                app.selectedOutfit = None
                setActiveScreen("calendar")  
 
#calendar view
def calendar_redrawAll(app):
    #calendar drawig loop and dimensions -> chat gpt
    start_day, total_days = get_calendar_data(app.year, app.month)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    cell_width, cell_height = 100, 110  # Adjusted cell size
    calendar_top = 110
    start_x = 60  # Starting X position of the calendar
    
    day_counter = 1
    
    for row in range(6):  # Max 6 weeks in a month
        for col in range(7):
            x = start_x + col * cell_width
            y = calendar_top +( row * cell_height )
            if (row == 0 and col >= start_day) or (row > 0 and day_counter <= total_days):
                drawRect(x, y, cell_width, cell_height, fill=None, border=app.lightg)
                drawLabel(str(day_counter), x + cell_width // 2 - 30, y + cell_height // 2 - 30, size=14, font = "Lora", fill = app.gray)
                if day_counter in app.calendarOutfits:
                    clothing = app.calendarOutfits[day_counter]
                    
                    drawImage(clothing.top.image, x + 20, y + 50, align="left", width=80, height=80)
                    drawImage(clothing.bottom.image, x + 20, y + 70, align="left", width= 80, height= 80)
                day_counter += 1
    drawRect(0,0, app.width, 110, fill = "white")
    drawLabel(app.title, app.width // 2, 50, size=20, font = "Lora", fill = app.gray)
    #toggling wash
    if app.needsWash:
        color = rgb(80, 85, 90)
    else:
        color = app.lightg
    drawLabel("Wash", 700, 50, size = 20, align = "left", fill = color, font = "Lora")
    drawLabel("Back", 50+30,50,align = "center", fill = app.gray, font = "Lora", size = 20)
    for i, day in enumerate(days):
        drawLabel(day, start_x + i * cell_width + cell_width // 2, calendar_top - 10, size=13, font = "Lora", fill = app.gray, bold=True)


def calendar_onMousePress(app, mouseX, mouseY):

    if (mouseX >= 700 and mouseX <= 800) and (mouseY >= 40 and mouseY <= 100):
        if app.needsWash:
            app.outfitsAvailable = app.outfitsWorn.copy() 
            app.outfitsWorn = [] 
            app.needsWash = False
    if (mouseX >= 50 and mouseX <= 110) and (mouseY >= 40 and mouseY <= 100) :
       app.calendarMode = False #and not app.needsWash:
       setActiveScreen("outfits")
    col = 7
    row = 6
    start_day, total_days = get_calendar_data(app.year, app.month) #  -> chat gpt
    cell_width, cell_height = 100, 110
    calendar_top = 110
    start_x = 60
    x = start_x + 7 * cell_width
    y = calendar_top + 6 * cell_height
    
    col = (mouseX - start_x) // cell_width
    row = (mouseY - calendar_top) // cell_height

    if 0 <= col < 7 and row >= 0:
        day_number = row * 7 + col + 1 - start_day #chat gpt
        if 1 <= day_number and day_number <= total_days:
            app.day = day_number
            if app.selectedOutfit == None:
                if day_number in app.calendarOutfits and app.calendarOutfits[day_number] is not None:
                   
                    setActiveScreen("display")
                else:
                    app.addToCalendar = True
                    app.calendarMode = True
                    setActiveScreen("outfits")

def calendar_onKeyPress(app, key):
    scrollStep = 20 
    maxScroll = max(0, 6 * 300 - (app.height - 110))
    if key == "down":
        app.scrollOffset = min(app.scrollOffset + scrollStep, maxScroll)
    elif key == "up":
        app.scrollOffset = max(app.scrollOffset - scrollStep, 0)
#can view the outfit selected
def display_redrawAll(app):
    clothing = app.calendarOutfits[app.day]
    drawImage(clothing.top.image, app.width//2,app.height//2 - 100, align="center", width=200, height=200)
    drawImage(clothing.bottom.image,app.width//2,app.height//2 + 100, align="center", width= 200, height= 200)
    drawLabel("Back", 50+30,50,align = "center", fill = app.gray, font = "Lora", size = 20)

def display_onMousePress(app, mouseX, mouseY):
    if (mouseX >= 50 and mouseX <= 110) and (mouseY >= 40 and mouseY <= 100):
       setActiveScreen("calendar")

        
def main():
    runAppWithScreens(initialScreen='start')
main()


