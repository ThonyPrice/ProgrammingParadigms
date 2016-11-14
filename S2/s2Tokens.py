# Programmeringparadigm     Lab S2 
# Created by:               Thony Price 
# Last revision:            2016-11-14

####################################################################

import re

def makeTokens(userInput): 

    # Regex patterns for tokens
    allTokens = re.compile  (r"""
                            (%.*\n)                         # 1. Comment
                            |(forw|back|left|right)         # 2. Movement 
                            |(up|down)                      # 3. Pencil
                            |(\d+)                          # 4. Value
                            |(\#[A-Fa-f0-9]{6})             # 5. Cvalue
                            |(color)                        # 6. Color
                            |(rep)                          # 7. Rep 
                            |(\.)                           # 8. Dot
                            |(")                            # 9. Quote
                            |(\n)                           # 10. Newline - Space 
                            |(\s+)                          # 11. Air - Space
                            """, re.VERBOSE)
    
    # Token types of objects
    tokionary =         {   1:Space,        2:Movement,     3:Pencil,       
                            4:Value,        5:Cvalue,       6:Color,        
                            7:Rep,          8:Dot,          9:Quote,        
                            10:Space,       11:Space,                   }   
    
    # Split input into tokens                
    elements = re.finditer(allTokens, userInput)
    row = 1
    token_ls = []
    
    # Iterate throught tokens and put token objects in array
    for el in elements:
        kind = tokionary[el.lastindex]
        val = repr(el.group(el.lastindex))
        if el.lastindex in range(2,6):
            token_ls.append(kind(val, row))
        if el.lastindex in range(6,12) or el.lastindex == 1:
            token_ls.append(kind(row))
        if el.lastindex == 1 or el.lastindex == 10:
            row += 1

    return token_ls
    
# Remove multiple following whitespaces
def rmSpaces(ls):
    try:
        for idx in range((len(ls)-1)):
            while isinstance(ls[idx], Space) and isinstance(ls[idx+1], Space):
                del ls[idx+1]
    except:
        pass
    return ls    
    
####################################################################

class SyntaxError(Exception):
    pass

class Token:
    def __init__ (self, value = None, row = None):
        self.value  = value
        self.row    = row
    
class Movement(Token):    
    def __init__(self, axis, row):
        Token.__init__(self, None, row)
        self.axis = axis

class Pencil(Token):
    def __init__(self, value, row):
        Token.__init__(self, value, row)

class Value(Token):    
    def __init__(self, value, row):
        Token.__init__(self, value, row)
        
class Cvalue(Token):    
    def __init__(self, value, row):
        Token.__init__(self, value, row)
    
class Color(Token):
    def __init__(self, row):
        Token.__init__(self, None, row)
        
class Rep(Token):
    def __init__(self, row):
        Token.__init__(self, None, row)
        
class Dot(Token):
    def __init__(self, row):
        Token.__init__(self, None, row)
        
class Quote(Token):
    def __init__(self, row):
        Token.__init__(self, None, row)
        
class Space(Token):
    def __init__(self, row):
        Token.__init__(self, None, row)
        
####################################################################

class Lenoa:
    
    # All information about Leona
    def __init__ (self):
        self.x      = None
        self.y      = None
        self.angle  = None
        self.color  = None
        self.pen    = False
    
    # Calculate Leonas new position moving FORW or BACK
    def move(self, direction, value):
        pass
        
    # Change Leonas angle LEFT or RIGHT
    def turn(self, direction, value):
        pass
    
    # Update the state of Leonas pen, UP or DOWN
    def changePen(self, value):
        pass