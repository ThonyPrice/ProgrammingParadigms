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
    tokionary =         {   1:"Comment",    2:Movement,     3:Pencil,       
                            4:Value,        5:Cvalue,       6:Color,        
                            7:Rep,          8:Dot,          9:Quote,        
                            10:Space,       11:Space,                   }   
    
    # Split input into tokens                
    elements = re.finditer(allTokens, userInput)
    row = 1
    token_ls = []
    # Iterate throught tokens and enqueue token objects
    for el in elements:
        kind = tokionary[el.lastindex]
        val = repr(el.group(el.lastindex))
        if el.lastindex in range(2,6):
            token_ls.append(kind(val, row))
        if el.lastindex in range(6,12):
            token_ls.append(kind(row))
        if el.lastindex == 1 or el.lastindex == 10:
            row += 1

    return token_ls

####################################################################

# Remove following whitespaces
def rmSpaces(ls):
    try:
        for idx in range((len(ls)-1)):
            if isinstance(ls[idx], Space) and isinstance(ls[idx+1], Space):
                del ls[idx+1]
    except:
        pass
    return ls
    
def parser(ls, last):
    try:         
        sTree   = exp(ls)               # Syntax tree
        return ("Formeln ar syntaktiskt korrekt")
    except SyntaxError as error:                            
        return "SyntaxError on line", ls[0].row   

def exp(ls):
    if len(ls) != 0:
        if isinstance(ls[0], Space):
            ls.pop(0)
            exp(ls)
            return
        if isinstance(ls[0], Quote):    # Jump back to rep function
            return
        if isinstance(ls[0], Rep):
            ls.pop(0)
            if isinstance(ls[0], Space):
                ls.pop(0)
                if isinstance(ls[0], Value):
                    ls.pop(0)
                    if isinstance(ls[0], Space):
                        ls.pop(0)
                        rep(ls)
                        exp(ls)
                        return
        else:
            instruction(ls)
            exp(ls)
            return
    return                              # End of input

# Syntax check for instructions
def instruction(ls):
    # Check syntax for Movement command
    if isinstance(ls[0], Movement):
        ls.pop(0)
        if isinstance(ls[0], Space):
            ls.pop(0)
            if isinstance(ls[0], Value):
                ls.pop(0)
                crtlEnd(ls)
                return
    # Check syntax for Color command              
    if isinstance(ls[0], Color):
        ls.pop(0)
        if isinstance(ls[0], Space):
            ls.pop(0)
            if isinstance(ls[0], Cvalue):
                ls.pop(0)
                crtlEnd(ls)
                return
    # Check syntax for Pencil command
    if isinstance(ls[0], Pencil):
        ls.pop(0)
        crtlEnd(ls)
        return
    raise SyntaxError                

# Check that following tokens are Dot or Space Dot
def crtlEnd(ls):
    if isinstance(ls[0], Dot):
        ls.pop(0)
        return 
    elif isinstance(ls[0], Space) and isinstance(ls[1], Dot) :
        ls.pop(0)
        ls.pop(0)
        return
    raise SyntaxError    

def rep(ls):
    if isinstance(ls[0], Quote):
        ls.pop(0)
        exp(ls)
        try:
            if isinstance(ls[0], Quote):
                ls.pop(0)
                return
        except:
            raise SyntaxError                
    else:
        instruction(ls)
        return
    raise SyntaxError                
        
    
def main():
    # Get input, join to string, make case insensitive
    userInput   = sys.stdin.readlines()     
    userInput   = "".join(userInput)
    userInput   = userInput.lower()

    token_ls    = makeTokens(userInput)
    tokens      = rmSpaces(token_ls)

    # Print tokens_ls -> For debugging purposes
    print("--------------------------")
    for token in tokens:
        try:
            print("Type:", type(token), "@Row:", token.row, "@Value:", token.value)
        except:
            print("Type:", type(token), "@Row:", token.row)    
    
    # Parse the list and create syntaxTree
    sTree       = parser(tokens)
    print(sTree)
    
    
# Runs main program from this module
if __name__ == "__main__":
    main ()
