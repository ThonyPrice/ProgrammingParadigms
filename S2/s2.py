# Programmeringparadigm   Lab S2 
# Created by:             Thony Price 
# Last revision:          2016-11-12

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
        
class Space(Token):
    def __init__(self, row):
        Token.__init__(self, None, row)
    
class Movement(Token):
    
    def __init__(self, categ, value, row):
        Token.__init__(self, categ, value, row)

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

def makeTokens(string): 

    # Regex patterns for tokens
    allTokens   = re.compile("%.*\n|DOWN|\.")
    space       = re.compile("\s")                      
    air         = re.compile("\s\s+")
    comment     = re.compile("%.*\n")
    movement    = re.compile("FORW|BACK|LEFT|RIGHT")  
    pen         = re.compile("UP|DOWN")
    dot         = re.compile("\.")

    # Convert userInput to list of Token objects
    row = 1
    tokens_lst = re.findall(tokens, string)
    while len(string) != 0:
        
        # # Remove multiple spaces, tabs and newlines
        # try:
        # line = re.sub("\s\s+|\t", "", line, 1)
        # except:
        #     pass
        #     
        # # Match comments
        comArg  = comment.match(string)
        try:
            comArg.group(0)
            line = re.sub(comment, "", string, 1)
            tokens_lst.append(Comment(row))  
        except:
            pass          
        # 
        # # Match and remove pen arguments
        # penArg  = pen.match(line)
        # try:
        #     value = penArg.group(0)
        #     if value == "DOWN":
        #         tokens_lst.append(Pencil(1, row))  
        #     else:
        #         tokens_lst.append(Pencil(0, row))  
        #     line = re.sub(pen, "", line, 1)            
        # except:
        #     pass          
        #             
        
        # Regex patterns for tokens
        # spaces = re.compile()
        # # Remove more spaces than 2, tabs and newlines
        # line = re.sub("\s\s+", "", line, 1)
        # 
        # # Match and remove single space
        # space = re.search("\s", line)
        # if space != None:
        #     line = re.sub("\s", "", line, 1)
        #     tokens_lst.append(Space(row))
        # # Match and remove Comment from line
        # comment = re.search("%.*\n", line)
        # if comment != None:
        #     line = re.sub("%.*\n", "", line, 1)
        #     tokens_lst.append(Comment(row))
        # Match and remove single space
        # moves = re.("FORW\s\d+|BACK\s\d+", line)
        # if len(moves) != 0:
        #     for move in moves:
        #         tmp1 = Movement(move[0:4], move[5:], row)
        #         tokens_lst.append(tmp1)
        # print("ROW:", row)
        row += 1
        # for token in tokens_lst:
        #     print(token.categ, "@Value", token.value, "@Row", token.row)
        
    return tokens_lst
        

def main():
    # Get input, join to string, make case insensitive
    userInput   = sys.stdin.readlines()     
    userInput   = "".join(userInput)
    userInput   = userInput.lower()

    tokens_lst  = makeTokens(userInput)
    
    tokens      = re.compile("(%.*\n)|(ritar)|(DOWN)|(\.)|(\n)")
    for item in re.finditer(tokens, userInput):
        print(item, item.lastindex)
    # print("--------------------------")
    # 
    # for token in tokens_lst:
    #     print("Row:", token.row, "Value:", token.value, "Type:", type(token))
    # q = makeQueue(userInput)
    # while not q.empty():
    #     tmp = q.get()
    #     print(tmp)
    # global Token
    # Token = ["DOWN", ]
    # -- END -- #

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
    
####################################################################