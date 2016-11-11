# Programmeringparadigm   Lab S2 
# Created by:             Thony Price 
# Last revision:          2016-11-10

import re
import sys
import queue

'''
__GRAMMATIK__

<språk>         ::= <instruktion> | <instruktion><språk> | COMMENT <språk>
<instruktion>   ::= FORW | BACK | LEFT | RIGHT | UP | DOWN |
                    COLOR | REP <rep> 
<rep>           ::= <instruktion> | "<språk>"

__TOKENS__

COMMENT ->  "%" Följd av tecken, slutar vid newline "\n"
FORW    ->  Matcha "FORW d s" där d är ett positivt heltal och 
            s godtyckligt antal whitespaces
BACK    ->  Matcha "BACK d s"
LEFT    ->  Matcha "LEFT d s"
RIGHT   ->  Matcha "RIGHT d s"
UP      ->  Matcha "UP d s"
DOWN    ->  Matcha "DOWN d s"
COLOR   ->  Matcha "COLOR #xxxxxx" där x är positivt heltal eller char
REP     ->  Matcha "REP s"

'''

# Store each char alone in a queue q, break at newline
def makeQueue(userInput):    
    q = queue.Queue()
    for line in userInput:
        for char in line:
            q.put(char)
    return q

def main():
    userInput   = sys.stdin.readlines()
    # q = makeQueue(userInput)
    # while not q.empty():
    #     tmp = q.get()
    #     print(tmp)
    # global tokens
    # tokens = ["DOWN", ]
    # -- END -- #

'''    
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
    
#######################################################

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
    