# Programmeringparadigm     Lab S2 
# Created by:               Thony Price 
# Last revision:            2016-11-17

import re

####################################################################

class Token():
    
    def __init__ (self, ofType, row, value = None):
        self.ofType     = ofType
        self.value      = value
        self.row        = row
    
    def getType(self):
        return self.ofType
        
    def getVal(self):
        return self.value

    # Debug representation
    def __str__ (self):
        return "Token({ofType}, {value}, {row})".format(
            ofType =self.ofType, 
            value=repr(self.value),
            row=self.row
        )
        
    def __repr__(self):
        return self.__str__()
    
####################################################################

class Lexer():
    
    def __init__ (self, text):
        self.token_ls   = self.tokenize(text)   
        self.prev       = None 
    
    # Use groups to pattern match regex's
    def tokenize(self, userInput): 
        # Regex patterns for tokens
        allTokens = re.compile  (r"""
                                (%.*\n)                         # 1. Comment
                                |(forw|back|left|right)         # 2. Movement 
                                |(up|down)                      # 3. Pencil
                                |([1-9][0-9]*)                  # 4. Value
                                |(\#[A-Fa-f0-9]{6})             # 5. Cvalue
                                |(color)                        # 6. Color
                                |(rep)                          # 7. Rep 
                                |(\.)                           # 8. Dot
                                |(")                            # 9. Quote
                                |(\n)                           # 10. Newline - Space 
                                |(\s+|\t+)                      # 11. Air - Space
                                |(.*)                           # 12. Invalid
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
        # The last token is always invalid, it's made from "end-of-input-char"
        del token_ls[len(token_ls)-1]
        token_ls.append(Token("EOF", 0))
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
        # for el in ls:
        #     print(el)
        return ls    
        
    def peekToken(self):
        return self.token_ls[0]
    
    def popToken(self):
        token = self.token_ls.pop(0)
        if token.ofType != "Space" and token.ofType != "Invalid" and token.ofType != "EOF":
            self.prev = token
        return token
    
    def hasNext(self):
        if len(self.token_ls) > 0:          # 
            return True
        return False