# Programmeringparadigm     Lab S2 
# Created by:               Thony Price 
# Last revision:            2016-11-19

####################################################################

class Parser():
    
    # When parser is called the lexer initializes immeadeatly
    def __init__ (self, lexer):
        self.tree   = self.parse(lexer)  
    
    def parse(self, lexer):
        try:       
            global quotes                               # Keep track of quote-depth
            quotes = 0
            sTree   = self.exp(lexer)
            # print("Formeln är syntaktiskt korrekt")
            return sTree
        except SyntaxError as error:                            
            print("Syntaxfel på rad", error)
            return None
    
    # "Top level" of parsing
    def exp(self, lexer):
        global quotes
        # Until a valid node is found, create a "pass" node
        sTree = ParseNode("Pass")
        if lexer.hasNext():
            token = lexer.peekToken()
            # At end of file quotes must be balanced
            if token.getType() == "EOF":
                if quotes != 0:
                    raise SyntaxError(lexer.prev.row)
                return sTree
            # Break if invalid token is found
            if token.getType() == "Invalid":
                raise SyntaxError(token.row)
            # Remove spaces and exp again
            if token.getType() == "Space":
                lexer.popToken()
                sTree.right = self.exp(lexer)
                return sTree
            # Check for unbalanced quotes, jump back to rep function
            if token.getType() == "Quote":
                if quotes != 0:
                    quotes -= 1
                    return sTree
                raise SyntaxError(token.row)
            # Check syntax for rep
            if token.getType() == "Rep":
                keep = lexer.popToken()
                if not lexer.popToken().getType() == "Space":
                    raise SyntaxError(lexer.prev.row)
                if not lexer.popToken().getType() == "Value":
                    raise SyntaxError(lexer.prev.row)
                keep.value = lexer.prev.value
                sTree = ParseNode(keep)                 # Create rep node
                if not lexer.popToken().getType() == "Space":
                    raise SyntaxError(lexer.prev.row)
                sTree.left  = self.rep(lexer)           # Branch left
            # Call instruction function if an instruction is found
            if  token.getType() == "Left" or token.getType() == "Right" or \
                token.getType() == "Forw" or token.getType() == "Back" or \
                token.getType() == "Up" or token.getType() == "Down" or \
                token.getType() == "Color": 
                sTree = self.instruction(lexer) 
            # Invalid tokens at this state
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
            self.ctrlSpaceDot(lexer)
        if  token.getType() == "Left" or token.getType() == "Right" or \
            token.getType() == "Forw" or token.getType() == "Back":
            keep = lexer.popToken()
            if not lexer.popToken().getType() == "Space":
                raise SyntaxError(lexer.prev.row)
            if not lexer.popToken().getType() == "Value":
                raise SyntaxError(lexer.prev.row)
            keep.value = lexer.prev.value
            sTree = ParseNode(keep)
            self.ctrlSpaceDot(lexer)
        if token.getType() == "Color":
            keep = lexer.popToken()
            if not lexer.popToken().getType() == "Space":
                raise SyntaxError(lexer.prev.row)
            if not lexer.popToken().getType() == "Cvalue":
                raise SyntaxError(lexer.prev.row)   
            keep.value = lexer.prev.value  
            sTree = ParseNode(keep)
            self.ctrlSpaceDot(lexer)
        return sTree    
        
    def rep(self, lexer):
        global quotes
        sTree = ParseNode("Pass")
        token = lexer.peekToken()
        if token.getType() == "Quote":
            quotes += 1                                 # Add quotation depth
            keep = lexer.popToken()                     # Pop quoatation mark 
            # Make sure rep's not double quoted
            if lexer.peekToken().getType() == "Quote":
                raise SyntaxError(lexer.peekToken().row)
            if lexer.peek2Tokens().getType() == "Quote":
                raise SyntaxError(lexer.peek2Tokens().row)
            sTree.right = self.exp(lexer)
            # When returned from instructions inside rep
            try:
                if not lexer.popToken() == "Quote":
                    raise SyntaxError(lexer.prev.row)
            except: 
                if lexer.hasNext():
                    return sTree
                raise SyntaxError(lexer.prev.token)
        # Check syntax for nested reps 
        if token.getType() == "Rep":
            keep = lexer.popToken()
            if not lexer.popToken().getType() == "Space":
                raise SyntaxError(lexer.prev.row)
            if not lexer.popToken().getType() == "Value":
                raise SyntaxError(lexer.prev.row)
            keep.value = lexer.prev.value
            sTree = ParseNode(keep)
            if not lexer.popToken().getType() == "Space":
                raise SyntaxError(lexer.prev.row)
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
