# Programmeringparadigm     Lab S2 
# Created by:               Thony Price 
# Last revision:            2016-11-17

####################################################################

class Parser():
    
    # When parser is called the lexer initializes immeadeatly
    def __init__ (self, lexer):
        self.tree   = self.parse(lexer)  
        self.last   = None                          # Remember last token
    
    def parse(self, lexer):
        try:       
            global quotes
            quotes = 0
            sTree   = self.exp(lexer)
            # print("Formeln är syntaktiskt korrekt")
            return sTree
        except SyntaxError as error:                            
            print("Syntaxfel på rad", error) # 
            return None
    
    # "Top level" of parsing
    def exp(self, lexer):
        global quotes
        sTree = ParseNode("Pass")
        if lexer.hasNext():
            token = lexer.peekToken()
            self.last = token
            if token.getType() == "EOF":
                if quotes != 0:
                    raise SyntaxError(lexer.prev.row)    # lexer.prev.row
                return sTree
            if token.getType() == "Invalid":
                raise SyntaxError(token.row)
            if token.getType() == "Space":
                lexer.popToken()
                sTree.right = self.exp(lexer)
                return sTree
            if token.getType() == "Quote":
                if quotes != 0:
                    quotes -= 1
                    return sTree                         # Jump back to rep
                raise SyntaxError(self.last.row)        # Chg
            if token.getType() == "Rep":
                keep = lexer.popToken()
                self.last = token
                if not lexer.popToken().getType() == "Space":
                    raise SyntaxError(lexer.prev.row)
                self.last = token    
                if not lexer.popToken().getType() == "Value":
                    raise SyntaxError(lexer.prev.row)
                self.last = token
                keep.value = lexer.prev.value
                sTree = ParseNode(keep)
                if not lexer.popToken().getType() == "Space":
                    raise SyntaxError(lexer.prev.row)
                self.last   = token
                sTree.left  = self.rep(lexer)       # Left branch (REP branch)
            if  token.getType() == "Left" or token.getType() == "Right" or \
                token.getType() == "Forw" or token.getType() == "Back" or \
                token.getType() == "Up" or token.getType() == "Down" or \
                token.getType() == "Color": 
                sTree = self.instruction(lexer) 
            if  token.getType() == "Dot" or token.getType() == "Value" or \
                token.getType() == "Cvalue":
                raise SyntaxError(token.row)
            sTree.right = self.exp(lexer)  
        return sTree
    
    # Parse the instruction type arguments
    def instruction(self, lexer):
        sTree = ParseNode("Pass")
        token = lexer.peekToken()
        if token.getType() == "Up" or token.getType() == "Down":
            sTree = ParseNode(lexer.popToken())
            self.last = token
            self.ctrlSpaceDot(lexer)
        if  token.getType() == "Left" or token.getType() == "Right" or \
            token.getType() == "Forw" or token.getType() == "Back":
            keep = lexer.popToken()
            self.last = token
            if not lexer.popToken().getType() == "Space":
                raise SyntaxError(lexer.prev.row)
            self.last = token
            if not lexer.popToken().getType() == "Value":
                raise SyntaxError(lexer.prev.row)
            keep.value = lexer.prev.value
            sTree = ParseNode(keep)
            self.last = token
            self.ctrlSpaceDot(lexer)
        if token.getType() == "Color":
            keep = lexer.popToken()
            self.last = token
            if not lexer.popToken().getType() == "Space":
                raise SyntaxError(lexer.prev.row)
            self.last = token
            if not lexer.popToken().getType() == "Cvalue":
                raise SyntaxError(lexer.prev.row)   
            keep.value = lexer.prev.value  
            sTree = ParseNode(keep)
            self.last = token
            self.ctrlSpaceDot(lexer)
        return sTree    
        
    def rep(self, lexer):
        global quotes
        sTree = ParseNode("Pass")
        token = lexer.peekToken()
        if token.getType() == "Quote":
            quotes += 1
            keep = lexer.popToken()                 # Pop quoatation mark 
            if lexer.peekToken().getType() == "Quote":
                raise SyntaxError(lexer.peekToken().row)
            if lexer.peek2Tokens().getType() == "Quote":
                raise SyntaxError(lexer.peek2Tokens().row)
            sTree.right = self.exp(lexer)
            try:
                if not lexer.popToken() == "Quote":
                    # lexer.prev = keep
                    # print("this?")
                    raise SyntaxError(lexer.prev.row) # token.row
            except: 
                # quotes -= 1
                if lexer.hasNext():
                    # sTree.right = self.exp(lexer)
                    return sTree
                
                raise SyntaxError(self.last.row)    #
        if token.getType() == "Rep":
            keep = lexer.popToken()
            self.last = token
            if not lexer.popToken().getType() == "Space":
                raise SyntaxError(lexer.prev.row)
            self.last = token    
            if not lexer.popToken().getType() == "Value":
                raise SyntaxError(lexer.prev.row)
            self.last = token
            keep.value = lexer.prev.value
            sTree = ParseNode(keep)
            if not lexer.popToken().getType() == "Space":
                raise SyntaxError(lexer.prev.row)
            self.last   = token
            sTree.left  = self.rep(lexer)  
        else:
            sTree.right = self.instruction(lexer)
            return sTree
        return sTree
    
    # Make sure a argument if ended with space and dot or only dot
    def ctrlSpaceDot(self, lexer):
        token = lexer.peekToken()
        if token.getType() == "Dot":
            lexer.popToken()
            return
        if token.getType() == "Space":
            lexer.popToken()
            if not lexer.popToken().getType() == "Dot":
                raise SyntaxError(lexer.prev.row)
            return
        raise SyntaxError(token.row)
    
    def getTree(self):
        return self.tree
        
# The parse tree consists of nodes, the arguments always branches right 
# except when a rep instruction is found then we'll branch left
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
