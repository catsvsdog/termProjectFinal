class Item:
    instances = {
        'top': set(),
        'bottom': set(),
        None: set()
    }

    def __init__(self, image, name, pos, size, color, season, types, isTop, serialNum):
        self.image = image
        self.name = name
        self.pos = pos
        self.size = size
        self.color = color
        self.season = season
        self.type = types
        self.isTop = isTop
        self.bounds = None
        self.serialNum = serialNum
        if self.isTop == 'top':
            Item.instances['top'].add(self)
        elif self.isTop == 'bottom':
            Item.instances['bottom'].add(self)
        else:  # None
            Item.instances[None].add(self)
    def getColor(self):
        return self.color

    def __eq__(self, other):
        return isinstance(other, Item) and self.image == other.image and self.name == other.name and self.pos == other.pos and self.size == other.size and self.color == other.color and self.season == other.season and self.type == other.type and self.isTop == other.isTop and self.serialNum == other.serialNum

    def __hash__(self):
        return hash(self.serialNum) 

    def update_bounds(self, x, y, width, height):
        self.bounds = (x, y, x + width, y + height)
        
    def __repr__(self):
        return f"Item: {self.name}, Type: {self.isTop}, Color: {self.color}, Season: {self.season}, Size: {self.size}, Position: {self.pos}, Bounds: {self.bounds}, Serial Number: {self.serialNum}"


        

class Top(Item):
    def __init__(self, name, color, season, type, serialNum = 0):
        self.super()
        self.name = name
        self.color = color
        self.season = season
        self.type = type #baggy or not
        self.serialNum = serialNum
        self.isTop = "Top"
    def getSize(self):
        return self.size
    
    def getType(self):
        return self.type
    def getSeason(self):
        result = list(self.season)
        final = ", ".join(result) 
        return final
    
    def changeName(self, other):
        self.name = other
    def changeSeason(self, other):
        self.season = other
    def changeColor(self, other):
        self.color = other
    def changeType(self, other):
        self.type = other
        
    def getColor(self):
        return self.color
    
    def __eq__(self, other):
        if ((self.serialNum == other.serialNum) and (self.color == other.color) and (self.season == other.season) and (self.type == other.type)):
            return True
        else:
            return False

    def __repr__(self):
        return f"Top: {self.name}"

class Bottom(Item):
    def __init__(self, name, color, season, type, serialNum = 0):
        self.name = name
        self.color = color
        self.season = season
        self.type = type
        self.serialNum = serialNum
        self.isBottom = "bottom"

    def getSize(self):
        return self.size
    def getType(self):
        return self.type
    def changeName(self,other):
        self.name = other
    def changeSeason(self, other):
        self.season = other
    def changeColor(self, other):
        self.color = other
    def changeType(self, other):
        self.type = other
    
    def getSeason(self):
        return self.season
    
    def getColor(self):
        return self.color
    def __repr__(self): 
        return f"Bottom: {self.name}"#, color: {self.color}, season: {self.season}"
    def __eq__(self, other):
        if (self.serialNum == other.serialNum) and (self.color == other.color) and (self.season == other.season) and (self.type == other.type):
            return True
        else:
            return False
        
#key ->bottoms, values are tops
types = {
    "baggy": ["tight", "baggy", "well-fit"],
    "tight": "baggy",
    "well-fit" : ["baggy", "tight"]
}

colorsThatGoWith = {
    "red": ["black", "white", "blue", "lightBlue", "beige", "gray"],
    "orange": ["white", "brown", "beige","blue", "lightGray", "black"],
    "yellow": ["gray", "white", "blue", "beige"],
    "green": ["brown", "white","blue", "lightBlue","black", "beige", "gray","lightGray"],
    "blue": ["white", "gray", "beige", "brown", "green", "black"],
    "lightBlue": ["white", "beige", "red", "green", "gray", "black", "pink"],
    "purple": ["white", "black", "beige", "gray"],
    "pink": ["white", "gray", "blue", "lightBlue", "brown"],
    "beige": ["brown", "white", "black", "pink"],
    "white": ["black", "gray", "beige", "navy","lightBlue", "brown", "white"],
    "black": ["white", "gray", "beige","lightBlue", "blue", "red", "black"],
    "gray": ["white", "black", "blue", "pink", "green", "yellow"],
    "brown": ["white", "beige", "blue", "green", "black"],
    "lightGray": ["white", "beige", "blue", "pink", "green"]
}

class Outfit:
    def __init__(self, top, bottom):
        self.top = top
        self.bottom = bottom
        self.userPrefColors = set()
        self.color = self.top.color | self.bottom.color
        self.style = [self.top.type] + [self.bottom.type]

    def getSize(self):
        return self.top.size

    def updatePref(self, other):
        self.userPrefColors.add(tuple(other))

    def getColor(self):
      top_color = self.top.getColor()
      bottom_color = self.bottom.getColor()
      if top_color:
        return top_color
      else:
        return bottom_color
    def isColorMatch(self):
        # try using top to match bottom first
        topColors = self.top.color
        bottomColors = self.bottom.color
        for topColor in topColors:
            if topColor in colorsThatGoWith:  # Check if the top color is in the dictionary
                matchedColors = set(colorsThatGoWith[topColor])  # Convert to set for easier comparison
                if matchedColors & bottomColors:  # Intersection: any common element
                    print(' Found bottom that matches top')
                    return True

        # check if  color from bottom matches any from top's compatible colors
        for bottomColor in bottomColors:
            if bottomColor in colorsThatGoWith:
                matchedColors = set(colorsThatGoWith[bottomColor])
                if matchedColors & topColors:
                    print(' Found top that matches bottom')
                    return True
        print('Info, No match find.')
        return False
    
    def isTypeMatch(self):
        print("top type: ", self.top.type)
        return self.bottom.type in types[self.top.type]

    def __repr__(self):
        return f"{self.top}, {self.bottom}"
    
    def __eq__(self, other):
        if not isinstance(other, Outfit):
            return False
        return (self.top.serialNum == other.top.serialNum) and (self.bottom.serialNum == other.bottom.serialNum)
    
    def __hash__(self):
        return hash(str(self))
    
