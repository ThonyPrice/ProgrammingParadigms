# Programmeringparadigm     Lab S2 
# Created by:               Thony Price 
# Last revision:            2016-11-19

import sys
from s2lexer import *
from s2parser import *
from s2leona_process import *

####################################################################
'''
__GRAMMATIK__

    <exp>           ::= <instruction> | <instruction><exp> 
                        | REP SPACE VALUE SPACE <rep>
                        | REP SPACE VALUE SPACE <rep> <exp>
    <instruction>   ::= MOVEMENT SPACE VALUE <end>
                        | COLOR SPACE CVALUE <end>
                        | PENCIL <end>
    <end>           ::= DOT | SPACE DOT
    <rep>           ::= <instruction> | QUOTE <exp> QUOTE
                        
__TOKENS__

    MOVEMENT    -> (FORW|BACK|LEFT|RIGHT)  
    PENCIL      -> (UP|DOWN)
    COLOR       -> (COLOR)
    REP         -> (REP)
    VALUE       -> Natural number
    CVALUE      -> Color in hex format
    DOT         -> A period sign
    QUOTE       -> A quotationmark
    SPACE       -> Singe or multiple spaces, tabs, comments and newlines 
'''
#################################################################### 

def main():
    # Raise recursion limit
    sys.setrecursionlimit(1000000000)
    # Get input, join to string, make case insensitive
    userInput   = sys.stdin.readlines()     
    userInput   = "".join(userInput)
    userInput   = userInput.lower()
    # Convert string to list of tokens
    lexer       = Lexer(userInput)
    # Call parser
    sTree       = Parser(lexer).tree
    # If sTree != None -> Syntax accepted 
    if sTree != None:
        # print(sTree)
        result      = Process(sTree)

# Runs main program from this module
if __name__ == "__main__":
    main ()