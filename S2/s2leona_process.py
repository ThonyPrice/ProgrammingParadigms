# Programmeringparadigm     Lab S2 
# Created by:               Thony Price 
# Last revision:            2016-11-17

import math

####################################################################

class Leona():
    
    # All information about Leona
    def __init__ (self):
        self.x      = 0
        self.y      = 0
        self.angle  = 0
        self.color_ = "#0000FF"
        self.pen    = False
    
    # Call relevant method for each argument in list
    def process(self, args):
        for arg in args:
            op = arg.getType().lower()
            func = getattr(self, op)
            func(arg)
    
    def down(self, token):
        self.pen = True
        
    def up(self, token):
        self.pen = False
        
    def left(self, token):
        self.angle += int(token.value)

    def right(self, token):
        self.angle -= int(token.value)
        
    def color(self, token):
        self.color_ = token.getVal().upper()

    # Caluculate and print Leonas new position
    def forw(self, token):
        old_x   = self.x
        old_y   = self.y
        angle   = self.angle
        move    = token.value
        self.x  = old_x + float(move) * math.cos((math.pi*angle)/180)
        self.y  = old_y + float(move) * math.sin((math.pi*angle)/180)
        if abs(self.x) < 0.00001:
            self.x = 0
        if abs(self.y) < 0.00001:
            self.y = 0
        if self.pen == True:
            print(self.color_, " ", end="")
            print("{0:.4f}".format(old_x,4), " ", end="")
            print("{0:.4f}".format(old_y,4), " ", end="")
            print("{0:.4f}".format(self.x,4), " ", end="")
            print("{0:.4f}".format(self.y,4))
    
    # Same as above but moving back    
    def back(self, token):
        old_x   = self.x
        old_y   = self.y
        angle   = self.angle
        move    = token.value
        self.x  = old_x - float(move) * math.cos((math.pi*angle)/180)
        self.y  = old_y - float(move) * math.sin((math.pi*angle)/180)
        if abs(self.x) < 0.00001:
            self.x = 0
        if abs(self.y) < 0.00001:
            self.y = 0
        if self.pen == True:
            print(self.color_, " ", end="")
            print("{0:.4f}".format(old_x,4), " ", end="")
            print("{0:.4f}".format(old_y,4), " ", end="")
            print("{0:.4f}".format(self.x,4), " ", end="")
            print("{0:.4f}".format(self.y,4))

    def rep(self, token):
        pass

class Process():
    
    def __init__ (self, tree):
        self.result = self.process(tree)
    
    # Process the binTree by first converting the tree to a list of arguments    
    # Then create a turtle Leona that processes all arguments in list
    def process(self, tree):
        args = []
        args = self.mkArgs(tree, args)
        args1 = []
        for arg in args:
            if arg != "Pass":
                args1.append(arg)
                # print(arg)
        leona = Leona()
        leona.process(args1)
        return 
        
    def mkArgs(self, tree, args):
        # print(tree.op)
        args.append(tree.op)
        
        if tree.left != None:
            repeat = tree.op.value
            for i in range(int(repeat)):
                self.mkArgs(tree.left, args)
        if tree.right != None:
            self.mkArgs(tree.right, args)
        return args
        