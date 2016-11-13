# Programmeringparadigm     Lab S2 
# Created by:               Thony Price 
# Last revision:            2016-11-12

# To do:                    Make all token Classes
#                           Split tokionary so grouped numbers makes same type objects                           
#

####################################################################
'''
__GRAMMATIK__

<språk>         ::= <instruktion> | <instruktion><språk> | COMMENT <språk>
<instruktion>   ::= <argument> | <rep>
<argument>      ::= <move><space><value><air>.| COLOR<space><color>>air>.|
                    <pen><air>.
                    COLOR | REP <rep> 
<move>          ::= FORW | BACK | LEFT | RIGHT
<pen>           ::= UP | DOWN
<rep>           ::= REP<instruktion> | "<språk>"
<space>         ::= " "
<air>           ::= " "*
<value>         ::= /d*
<color>         ::= #{[\d\w], 6}

__Token__

COMMENT ->  "%" Följd av tecken, slutar vid newline "\n"
FORW    ->  Matcha FORW
BACK    ->  Matcha BACK
LEFT    ->  Matcha LEFT
RIGHT   ->  Matcha RIGHT
UP      ->  Matcha UP
DOWN    ->  Matcha DOWN
COLOR   ->  Matcha COLOR
REP     ->  Matcha "REP s"

'''
####################################################################

import re
import sys
import queue

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
        
####################################################################

class Token:
    
    def __init__ (self, value = None, row = None):
        self.value  = value
        self.row    = row
    
class Comment(Token):
    def __init__(self, row):
        Token.__init__(self, None, row)
        
class Movement(Token):    
    def __init__(self, axis, row):
        Token.__init__(self, None, row)
        self.axis = axis
        
class Space(Token):
    def __init__(self, row):
        Token.__init__(self, None, row)
    

class Pencil(Token):
    
    def __init__(self, value, row):
        Token.__init__(self, value, row)

class Color(Token):
    
    def __init__(self, categ, value, row):
        Token.__init__(self, categ, value, row)
        
####################################################################

# Store each char alone in a queue q, break at newline
def makeQueue(userInput):    
    q = queue.Queue()
    for line in userInput:
        for char in line:
            q.put(char)
    return q

def makeTokens(userInput): 

    # Regex patterns for tokens
    allTokens = re.compile  (r"""
                            (%.*\n)                         # 1. Comments
                            |(forw|back|left|right)         # 2. Movement 
                            |(up|down)                      # 3. Pencil
                            |(color)                        # 4. Color
                            |(\d+)                          # 5. Value
                            |(\#[A-Fa-f0-9]{6})             # 6. Color
                            |(\.)                           # 7. Dot
                            |(\n)                           # 8. Newline 
                            |(")                            # 9. Quote
                            |(REP)                          # 10. Rep 
                            |(\s\s+)                        # 11. Air
                            |(\s)                           # 12. Space
                            """, re.VERBOSE)
    
    # Token types of objects
    tokionary =     {       1:Comment,      2:Movement,     3:"Pencil",     
                            4:"Color",      5:"Value",      6: "Cvalue",    
                            7:"Dot",        8:"Newline",    9:"Quote",      
                            10:"Rep",       11:"Air",       12:"Space"      }   
                    
    elements = re.finditer(allTokens, userInput)
    row = 1
    tokens_ls =     []
    for el in elements:
        kind = tokionary[el.lastindex]
        tokens_ls.append(kind(row))

        if el.lastindex == 8 or el.lastindex == 1:
            row += 1
        # print(tokionary[idx], repr(item.group(item.lastindex)))
    
    return tokens_ls
        

def main():
    # Get input, join to string, make case insensitive
    userInput   = sys.stdin.readlines()     
    userInput   = "".join(userInput)
    userInput   = userInput.lower()

    tokens_ls   = makeTokens(userInput)
    print("--------------------------")
    for token in tokens_ls:
        if isinstance(token, Comment):
            print("Nice", token.row)
        
    # for item in re.finditer(tokens, userInput):
    #     print(item, item.lastindex)


'''
% Det har ar en kommentar
% Nu ritar vi en kvadrat
% Det har ar en kommentar
% Nu ritar vi en kvadrat
DOWN.
FORW 1. LEFT 90.
FORW 1. LEFT 90.
FORW 1. LEFT 90.
FORW 1. LEFT 90.
'''

# Runs main program from this module
if __name__ == "__main__":
    main ()
