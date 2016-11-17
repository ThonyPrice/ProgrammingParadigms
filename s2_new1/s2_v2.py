# Programmeringparadigm     Lab S2 
# Created by:               Thony Price 
# Last revision:            2016-11-15

####################################################################

import re
import sys
import math

class Token():
    
    def __init__ (self, ofType, row, value = None):
        self.ofType     = ofType
        self.value      = value
        self.row        = row
    
    def getType(self):
        return self.ofType
        
    def getVal(self):
        return self.value

    def __str__ (self):
        return "Token({ofType}, {value}, {row})".format(
            ofType =self.ofType, 
            value=repr(self.value),
            row=self.row
        )
        
    def __repr__(self):
        return self.__str__()

class Lexer():
    
    def __init__ (self, text):
        self.token_ls   = self.tokenize(text)   
        self.prev       = None 
    
    def tokenize(self, userInput): 
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
                                |(.*?)                          # 12. Invalid
                                """, re.VERBOSE)
        # Token types of objects
        tokionary =         {   1:"Space",      2:"Movement",   3:"Pencil",       
                                4:"Value",      5:"Cvalue",     6:"Color",        
                                7:"Rep",        8:"Dot",        9:"Quote",        
                                10:"Space",     11:"Space",     12:"Invalid"    }       
        # Split input into tokens                
        elements = re.finditer(allTokens, userInput)
        row = 1
        token_ls = []
        # Iterate throught tokens and put token objects in array
        for el in elements:
            ofType  = tokionary[el.lastindex]
            if el.lastindex == 1:
                token_ls.append(Token(ofType, row))
            if el.lastindex == 2:
                if el.group(el.lastindex) == "forw":
                    token_ls.append(Token("Forw", row))
                if el.group(el.lastindex) == "back":
                    token_ls.append(Token("Back", row))     
                if el.group(el.lastindex) == "left":
                    token_ls.append(Token("Left", row))
                if el.group(el.lastindex) == "right":
                    token_ls.append(Token("Right", row))       
            if el.lastindex == 3:
                if el.group(el.lastindex) == "up":
                    token_ls.append(Token("Up", row, False))
                if el.group(el.lastindex) == "down":
                    token_ls.append(Token("Down", row, True))
            if el.lastindex in range(4,6):
                value   = el.group(el.lastindex)
                token_ls.append(Token(ofType, row, value))
            if el.lastindex in range(6,13):
                token_ls.append(Token(ofType, row))
            if el.lastindex == 1 or el.lastindex == 10:
                row += 1
        # Remove multiple spaces
        return self.rmSpaces(token_ls)
        
    # Remove multiple following whitespaces
    def rmSpaces(self, ls):
        try:
            for idx in range((len(ls)-1)):
                while ls[idx].getType() == "Space" and ls[idx+1].getType() == "Space":
                    del ls[idx+1]
        except:
            pass
        for el in ls:
            print(el)
        return ls    
        
    def peekToken(self):
        return self.token_ls[0]
    
    def popToken(self):
        token = self.token_ls.pop(0)        # MAYBE SKIP PREV ASSERTION FOR SPACE?
        self.prev = token
        return token
    
    def hasNext(self):
        if len(self.token_ls) > 1:          # MUST CHANGE FOR KATTIS
            return True
        return False

class SyntaxError(Exception):
    pass

####################################################################

class Parser():
    
    def __init__ (self, lexer):
        self.tree   = self.parse(lexer)  
        self.last   = None  
    
    def parse(self, lexer):
        try:       
            sTree   = self.exp(lexer)
            print("Formeln ar syntaktiskt korrekt")
            return sTree
        except SyntaxError as error:                            
            print("SyntaxError on line", self.last.row)
            return None
    
    def exp(self, lexer):
        sTree = ParseNode("Pass")
        if lexer.hasNext():
            token = lexer.peekToken()
            self.last = token
            # print("Token:", token)
            if token.getType() == "Invalid":
                raise SyntaxError()
            if token.getType() == "Space":
                lexer.popToken()
                sTree.right = self.exp(lexer)
                return sTree
            if token.getType() == "Quote":
                return sTree                         # Jump back to rep
            if token.getType() == "Rep":
                keep = lexer.popToken()
                self.last = token
                if not lexer.popToken().getType() == "Space":
                    raise SyntaxError
                self.last = token    
                if not lexer.popToken().getType() == "Value":
                    raise SyntaxError
                self.last = token
                keep.value = lexer.prev.value
                sTree = ParseNode(keep)
                if not lexer.popToken().getType() == "Space":
                    raise SyntaxError
                sTree.left = self.rep(lexer)        # Left branch
                # sTree.right = self.exp(lexer)       # Right branch
                # return sTree
            if  token.getType() == "Left" or token.getType() == "Right" or \
                token.getType() == "Forw" or token.getType() == "Back" or \
                token.getType() == "Up" or token.getType() == "Down" or \
                token.getType() == "Color": 
                sTree = self.instruction(lexer) 
                # sTree.right = self.instruction(lexer) 
            sTree.right = self.exp(lexer)           
        return sTree
    
    def instruction(self, lexer):
        token = lexer.peekToken()
        if token.getType() == "Up" or token.getType() == "Down":
            sTree = ParseNode(lexer.popToken())
            self.ctrlSpaceDot(lexer)
            # sTree.right = self.exp(lexer)
            # return sTree
        if  token.getType() == "Left" or token.getType() == "Right" or \
            token.getType() == "Forw" or token.getType() == "Back":
            keep = lexer.popToken()
            self.last = token
            if not lexer.popToken().getType() == "Space":
                raise SyntaxError
            self.last = token
            if not lexer.popToken().getType() == "Value":
                raise SyntaxError
            keep.value = lexer.prev.value
            sTree = ParseNode(keep)
            self.ctrlSpaceDot(lexer)
            # sTree.right = self.exp(lexer)
            # return sTree
        if token.getType() == "Color":
            keep = lexer.popToken()
            self.last = token
            if not lexer.popToken().getType() == "Space":
                raise SyntaxError
            self.last = token
            if not lexer.popToken().getType() == "Cvalue":
                raise SyntaxError   
            keep.value = lexer.prev.value  
            sTree = ParseNode(keep)
            self.ctrlSpaceDot(lexer)
            # sTree.right = self.exp(lexer)
        return sTree    
        
    def rep(self, lexer):
        sTree = ParseNode("Pass")
        token = lexer.peekToken()
        if token.getType() == "Quote":
            keep = lexer.popToken()
            sTree.right = self.exp(lexer)
            try:
                if not lexer.popToken() == "Quote":
                    lexer.prev = keep
                    raise SyntaxError
            except: 
                if lexer.hasNext():
                    lexer.popToken()
                    return sTree
                raise SyntaxError
        else:
            sTree.right = self.instruction(lexer)
            return sTree


    def ctrlSpaceDot(self, lexer):
        token = lexer.peekToken()
        if token.getType() == "Dot":
            lexer.popToken()
            return
        if token.getType() == "Space":
            lexer.popToken()
            if not lexer.popToken().getType() == "Dot":
                raise SyntaxError
            return
        raise SyntaxError
    
    def getTree(self):
        return self.tree
        
        
class ParseNode():
    
    def __init__ (self, op):
        self.op     = op
        self.left   = None
        self.right  = None
        
    def __str__ (self):
        return "Node({left}, {token}, {right})".format(
            token = self.op, 
            left=repr(self.left),
            right=self.right
        )
        
    def __repr__(self):
        return self.__str__()
        
    def left(self):
        return self.left
        
    def right(self):
        return "Hej"

class Leona():
    
    # All information about Leona
    def __init__ (self):
        self.x      = 0
        self.y      = 0
        self.angle  = 0
        self.color_ = "#0000FF"
        self.pen    = False
    
    # Calculate Leonas new position moving FORW or BACK
    def process(self, args):
        for arg in args:
            op = arg.getType().lower()
            func = getattr(self, op)
            func(arg)
    
    def down(self, token):
        self.pen == True
        
    def up(self, token):
        self.pen == False
        
    def left(self, token):
        self.angle += int(token.value)

    def right(self, token):
        self.angle += int(token.value)
        
    def color(self, token):
        self.color_ = token.getVal()

    def forw(self, token):
        old_x   = self.x
        old_y   = self.y
        angle   = math.radians(self.angle)
        move    = token.value
        new_x   = old_x + int(move) * math.cos((int(math.pi)*angle)/180)
        new_y   = old_y + int(move) * math.cos((int(math.pi)*angle)/180)
        self.x  = new_x        
        self.y  = new_y        
        # if self.pen == True:
        print(self.color_, old_x, old_y, new_x, new_y)

    def back(self, token):
        pass

    def rep(self, token):
        pass

        


class Process():
    
    def __init__ (self, tree):
        self.result = self.process(tree)
        
    def process(self, tree):
        args = []
        args = self.mkArgs(tree, args)
        print("_____________")
        args1 = []
        for arg in args:
            if arg != "Pass":
                args1.append(arg)
                print(arg)
        leona = Leona()
        leona.process(args1)
        return "Hej"
        
    def mkArgs(self, tree, args):
        # if tree.op.getType() != "Pass":
        args.append(tree.op)
        # if isinstance(tree.op, Token):
        #     if tree.op.ofType == "Rep":
        #         print(tree.op.value)
        #         repeat = tree.op.value
        if tree.left != None:
            repeat = tree.op.value
            print(repeat)
            for i in range(int(repeat)):
            # print("left", tree.left.op)
                self.mkArgs(tree.left, args)
        if tree.right != None:
            # print("right", tree.right.op)
            self.mkArgs(tree.right, args)
        return args
        


####################################################################

def main():
    # Get input, join to string, make case insensitive
    userInput   = sys.stdin.readlines()     
    userInput   = "".join(userInput)
    userInput   = userInput.lower()
    # Convert string to list of tokens
    lexer       = Lexer(userInput)
    # Debug
    # while lexer.hasNext():
    #     print(lexer.popToken())
    # Call parser
    sTree       = Parser(lexer).tree
    print("--- Enter Process ---")
    print(sTree)
    if sTree != None:
        result      = Process(sTree)
        print(result)
    print("--- END ---")
    
# Runs main program from this module
if __name__ == "__main__":
    main ()