# Programmeringparadigm     Lab S2 
# Created by:               Thony Price 
# Last revision:            2016-11-14

####################################################################
'''
__GRAMMATIK__

    <exp>           ::= <instruction> | <instruction><exp> 
                        | REP SPACE VALUE SPACE <rep>
                        | REP SPACE VALUE SPACE <rep> <exp>
    <instructtion>  ::= MOVEMENT SPACE VALUE <end>
                        | COLOR SPACE CVALUE <end>
                        | PENCIL <end>
    <end>           ::= DOT | SPACE DOT
    <rep>           ::= <instruction> | QUOTE <exp> QUOTE
                        
__TOKENS__

    MOVEMENT    -> (FORW|BACK|LEFT|RIGHT)  
    PENCIL      -> (UP|DOWN)
    COLOR       -> "COLOR"
    REP         -> (REP)
    VALUE       -> Natural number
    CVALUE      -> Color in hex format
    DOT         -> A period sign
    QUOTE       -> A quotationmark
    SPACE       -> Singe or multiple spaces, tabs, comments and newlines 

'''
####################################################################

import sys
from s2Tokens import * 


def parser(ls):
    global latest
    try:         
        sTree   = exp(ls)               # Syntax tree
        return ("Formeln ar syntaktiskt korrekt")
    except SyntaxError:                            
        return "SyntaxError on line", latest.row


# First "level" of controlling syntax
def exp(ls):
    global latest
    if len(ls) == 0:
        return                          # End of string
    latest = ls[0]                      # ???
    if isinstance(ls[0], Space):
        ls.pop(0)
        exp(ls)
        return
    if isinstance(ls[0], Quote):        # Jump back to rep function
        return
    if isinstance(ls[0], Rep):
        ls.pop(0)
        latest = ls[0]
        if isinstance(ls[0], Space):
            ls.pop(0)
            latest = ls[0]
            if isinstance(ls[0], Value):
                ls.pop(0)
                latest = ls[0]
                if isinstance(ls[0], Space):
                    ls.pop(0)
                    rep(ls)
                    exp(ls)
                    return
                raise SyntaxError
    else:
        instruction(ls)
        exp(ls)
        return
    raise SyntaxError                   # Non exhaustive pattern


# Syntax check for instructions
def instruction(ls):
    try:
        global latest
        # Check syntax for Movement command
        latest = ls[0]
        if isinstance(ls[0], Movement):
            ls.pop(0)
            latest = ls[0]
            if isinstance(ls[0], Space):
                ls.pop(0)
                latest = ls[0]
                if isinstance(ls[0], Value):
                    ls.pop(0)
                    crtlEnd(ls)
                    return
        # Check syntax for Color command              
        if isinstance(ls[0], Color):
            ls.pop(0)
            latest = ls[0]
            if isinstance(ls[0], Space):
                ls.pop(0)
                latest = ls[0]
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
    except:          
        raise SyntaxError             


# Check that following tokens are Dot or Space Dot
def crtlEnd(ls):
    try:
        global latest
        latest = ls[0]
        if isinstance(ls[0], Dot):
            ls.pop(0)
            return 
        if isinstance(ls[0], Space):
            ls.pop(0)
            latest = ls[0]
            if isinstance(ls[0], Dot):
                ls.pop(0)
                return
        raise SyntaxError
    except:
        raise SyntaxError


def rep(ls):
    global latest
    latest = ls[0]
    if isinstance(ls[0], Quote):
        hold = ls.pop(0)
        exp(ls)
        try:
            if isinstance(ls[0], Quote):
                ls.pop(0)
                return
        except:
            latest = hold
            raise SyntaxError             
    else:
        exp(ls)
        return
    raise SyntaxError              
        
    
def main():
    # Get input, join to string, make case insensitive
    userInput   = sys.stdin.readlines()     
    userInput   = "".join(userInput)
    userInput   = userInput.lower()
    # Convert string to list of tokens
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
