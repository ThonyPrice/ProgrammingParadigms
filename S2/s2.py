# Programmeringparadigm     Lab S2 
# Created by:               Thony Price 
# Last revision:            2016-11-12

####################################################################
'''
__GRAMMATIK__

<exp>       ::=

__TOKENS__
Movement,    
Pencil
Value
Cvalue
Color
Rep
Comment      
Dot
Quote
Space 

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
from s2Classes import * 

####################################################################

def makeTokens(userInput): 

    # Regex patterns for tokens
    allTokens = re.compile  (r"""
                            (\n)                            # 1. Newline 
                            |(\s\s+)                        # 2. Air
                            |(forw|back|left|right)         # 3. Movement 
                            |(up|down)                      # 4. Pencil
                            |(\d+)                          # 5. Value
                            |(\#[A-Fa-f0-9]{6})             # 6. Cvalue
                            |(color)                        # 7. Color
                            |(rep)                          # 8. Rep 
                            |(%.*\n)                        # 9. Comment
                            |(\.)                           # 10. Dot
                            |(")                            # 11. Quote
                            |(\s)                           # 12. Space
                            """, re.VERBOSE)
    
    # Token types of objects
    tokionary =         {   1:"Newline",    2:"Air",        3:Movement,     
                            4:Pencil,       5:Value,        6:Cvalue,    
                            7:Color,        8:Rep,          9:Comment,      
                            10:Dot,        11:Quote,        12:Space    }   
    # Split input into tokens                
    elements = re.finditer(allTokens, userInput)
    row = 1
    token_q = queue.Queue()
    # Iterate throught tokens and enqueue token objects
    for el in elements:
        kind = tokionary[el.lastindex]
        val = repr(el.group(el.lastindex))
        if el.lastindex in range(3,7):
            token_q.put(kind(val, row))
        if el.lastindex in range(7,13):
            token_q.put(kind(row))
        if el.lastindex == 1 or el.lastindex == 9:
            row += 1

    return token_q

def parser(q):
    try:                                  
        sTree = exp(q)         # Syntax tree
        print("Formeln är syntaktiskt korrekt")
        return sTree
    except SyntaxError as error:                            
        return str(error) + radslut(q)    

def main():
    # Get input, join to string, make case insensitive
    userInput   = sys.stdin.readlines()     
    userInput   = "".join(userInput)
    userInput   = userInput.lower()

    token_q     = makeTokens(userInput)
    # Print tokens_ls -> For debugging purposes
    print("--------------------------")
    while not token_q.empty():
        token = token_q.get()
        try:
            print("Type:", type(token), "@Row:", token.row, "@Value:", token.value)
        except:
            print("Type:", type(token), "@Row:", token.row)
    
    # Parse the list and create syntaxTree
    syntaxTree  = parser(token_q)
    

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
