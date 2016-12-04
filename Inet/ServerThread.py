# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-12-03

# This file is launched when ThreadedServer finds a new connection
# Each connection created a ServerThread object 
# The object handles all communication with the client

import os
import glob
import socket
from Users import User

class ServerThread(object):
    
    def __init__(self, client, address):
        self.client = client
        self.address= address
        self.size   = 10
        self.users  = self.mkClients()

    def listenToClient(self):
        while True:
            try:

                slct_lang = self.recive()
                if slct_lang == 's':
                    print("Client choose Swedish")
                    userInfo = self.logInSwe()
                    self.mainMenuSwe(userInfo)
                    var = self.exitOrNotSwe()
                    
                if slct_lang == 'e':
                    print("Client choose English")
                    userInfo = self.logInEng()
                    self.mainMenuEng(userInfo)
                    var = self.exitOrNotEng()
                
                if var == 1:
                    self.client.close()
                
            except:
                print(self.address, "closed it's session")
                self.client.close()
                return False
    
    # Get users logIn info and verify. If info is correct
    # an object with users details is returned
    def logInEng(self):
        while True:
            self.send("Please enter card number, 4 digits: ")
            cardNr = self.recive()
            self.send("Please enter Pin code, 4 digits: ")
            logIn = self.recive()
            userInfo = self.verify(cardNr, logIn)
            if userInfo != 'False':
                self.send('True')
                return userInfo
            print("User entered invalid information")
            self.send('False')
        return userInfo
    
    def mainMenuEng(self, userInfo):
        self.send("~~~ Welcome to JvA bank! ~~~")
        while True:
            self.mkClients()
            self.pushAdEng()
            self.send("(1)Balance (2)Withdrawal (3)Deposit (4)Exit")
            menuOp = self.recive()
            if menuOp == '1':
                self.send(userInfo.balance)
            if menuOp == '2' or menuOp == '3':
                self.send("Enter amount: ")
                amount = int(self.recive())
                if menuOp == '2':
                    self.send("Enter your PIN: ")
                    amount  = amount * -1
                    pin     = self.recive()
                    print("Recived pin:", pin)
                    if userInfo.verifyPin(pin): 
                        print("verified")
                        self.send("PIN correct")                               
                        userInfo.updateBalance(amount)
                    else:
                        self.send("PIN incorrect") 
                        print("Invalid PIN")
                if menuOp == '3':
                    userInfo.updateBalance(amount)    
            if menuOp == '4':
                return
            if menuOp != '1' and menuOp != '2' and menuOp != '3' and menuOp != '4':
                self.send("Invalid option, try again")

    def exitOrNotEng(self):
        self.send("(1) End session | (2) Change language: ")
        return int(self.recive())
        
    # Send ad to client
    def pushAdEng(self):
        with open(os.path.join("advertisement", "ad_eng.txt"), "r") as f:
            for line in f:
                self.send(line)

    # Recive message from client
    def recive(self):
        data = ''
        while True:
            chunk = self.client.recv(self.size).decode('utf-8')
            # print("Chunk:", chunk)
            data += chunk
            if '¶' in chunk:
                break
        return data[0:len(data)-1]
    
    # Send message to cliend
    def send(self, msg):
        msg += '¶'
        while len(msg) > self.size: 
            chunk = msg[0:self.size]
            self.client.sendto(chunk.encode('utf-8'), ('localhost', 5000))
            msg = msg[self.size:] 
        if len(msg) == self.size:
            self.client.sendto(msg.encode('utf-8'), ('localhost', 5000))  
        elif len(msg) > 0:
            self.client.sendto(msg.encode('utf-8'), ('localhost', 5000))  
    
    def mkClients(self):
        users = []
        for filename in glob.glob(os.path.join("clients", '*.txt')):
            info = []
            with open(filename, "r", encoding = "utf-8") as f:
                for line in f:
                    info.append(line.strip('\n'))
                users.append(User(info[0], info[1], info[2], info[3:]))
        return users
    
    # Search users for anyone with given logIn credentials 
    def verify(self, cardNr, logIn):
        for user in self.users:
            if user.cardNr == cardNr and user.logIn == logIn:
                return user
        return 'False'

###############################################################################
# Menus translated to Swedish    

    def logInSwe(self):
        while True:
            self.send("Ange kortnr, 4 siffror: ")
            cardNr = self.recive()
            self.send("Ange pinkod, 4 siffror: ")
            logIn = self.recive()
            userInfo = self.verify(cardNr, logIn)
            if userInfo != 'False':
                self.send('True')
                break
            print("User entered invalid information")
            self.send('False')
        return userInfo
        
    def mainMenuSwe(self, userInfo):
        self.send("~~~ Valkommen till JvA bank! ~~~")
        while True:
            self.mkClients()
            self.pushAdSwe()
            self.send("(1)Saldo (2)Uttag (3)Insattning (4)Avsluta")
            menuOp = self.recive()
            if menuOp == '1':
                self.send(userInfo.balance)
            if menuOp == '2' or menuOp == '3':
                self.send("Ange belopp: ")
                amount = int(self.recive())
                if menuOp == '2':
                    self.send("Ange pinkod: ")
                    amount  = amount * -1
                    pin     = self.recive()
                    print("Recived pin:", pin)
                    if userInfo.verifyPin(pin): 
                        print("verified")
                        self.send("PIN korrekt")                               
                        userInfo.updateBalance(amount)
                    else:
                        self.send("PIN inkorrekt") 
                        print("Invalid PIN")
                if menuOp == '3':
                    userInfo.updateBalance(amount)    
            if menuOp == '4':
                return
            if menuOp != '1' and menuOp != '2' and menuOp != '3' and menuOp != '4':
                self.send("Ogiltigt val, testa igen")

    def exitOrNotSwe(self):
        self.send("(1) Avsluta session | (2) Byt sprak: ")
        return int(self.recive())
    
    # Send ad to client
    def pushAdSwe(self):
        with open(os.path.join("advertisement", "ad_swe.txt"), "r") as f:
            for line in f:
                self.send(line)
