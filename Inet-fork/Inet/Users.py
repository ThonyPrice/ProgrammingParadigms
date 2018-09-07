# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-12-03

# This file called when a ServerThread creates an object to 
# better handle a customers information. 

import os

# Contains all information for a customer in the bank
# Can update the balance in a customers file
class User(object):
    def __init__(self, cardNr, logIn, balance, pins):
        self.cardNr = cardNr
        self.logIn  = logIn
        self.balance= balance
        self.pins   = pins

    # Update the balance both in object and on file
    def updateBalance(self, amount):
        old = int(self.balance)
        new= old + amount
        self.balance = str(new)
        
        name = self.cardNr + ".txt"
        with open(os.path.join("clients", name), "r") as f:
            data = f.readlines()
        data[2] = str(new) + '\n'
        with open(os.path.join("clients", name), "w") as f:
            f.writelines( data )
        
    def verifyPin(self, pinCode):
        if pinCode in self.pins:
            return True
        return False
