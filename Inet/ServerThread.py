# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-12-03

# This file is launched when ThreadedServer finds a new connection
# Each connection created a ServerThread object 
# The object handles all communication with the client

import os
import glob
import socket

# A User oject represents all information for a customer in the bank
class User(object):
    def __init__(self, cardNr, logIn, balance, pins):
        self.cardNr = cardNr
        self.logIn  = logIn
        self.balance= balance
        self.pins   = pins
    
    def updateBalance(self, amount):
        tmp = int(self.balance)
        tmp1= tmp + amount
        self.balance = str(tmp1)
        name = self.cardNr + ".txt"
        with open(os.path.join("clients", name), "r") as f:
            data = f.readlines()
        data[2] = str(tmp1) + '\n'
        with open(os.path.join("clients", name), "w") as f:
            f.writelines( data )
        
    def verifyPin(self, pinCode):
        for pin in self.pins:
            if pin == pinCode:
                return True
        return False

class ServerThread(object):
    
    def __init__(self, client, address):
        self.client = client
        self.address= address
        self.size   = 10
        self.users  = self.mkClients()

    def listenToClient(self):
        while True:
            try:
                # Send advertisement
                self.pushAd()           
                
                # Recive client language request
                slct_lang = self.recive()
                if slct_lang == 's':
                    print("Client chose Swedish")
                    
                    # Get clients logIn info
                    while True:
                        cardNr = self.recive()
                        logIn = self.recive()
                        print("Calls verify...")
                        userInfo = self.verify(cardNr, logIn)
                        if userInfo != 'False':
                            self.send('True')
                            break
                        print("User entered invalid information")
                        self.send('False')
                    
                    # Main menu
                    msg = "Welcome to bank\n(1)Balance, (2)Withdrawal, (3)Deposit, (4)Exit"
                    self.send(msg)
                    while True:
                        menuOp = self.recive()
                        if menuOp == '1':
                            self.send(userInfo.balance)
                            self.send(msg) 
                        if menuOp == '2' or menuOp == '3':
                            self.send("Enter amount:")
                            amount = int(self.recive())
                            if menuOp == '2':
                                self.send("Enter your PIN:")
                                amount  = amount * -1
                                pin     = self.recive()
                                print("Recived pin:", pin)
                                if userInfo.verifyPin(pin): 
                                    print("verified")                               
                                    userInfo.updateBalance(amount)
                                else:
                                    print("Invalid PIN")
                            if menuOp == '3':
                                userInfo.updateBalance(amount)    
                        if menuOp == '4':
                            break
                        if menuOp != '1' and menuOp != '2' and menuOp != '3' and menuOp != '4':
                            print("Invalid, try again")
                    
                    print("END")
                if data:
                    # Set the response to echo back the recieved data 
                    response = data.upper()
                    self.client.sendto(response.encode('utf-8'), ('localhost', 5000))
                else:
                    raise error('Client disconnected')
            except:
                print("Exception caught!")
                self.client.close()
                return False
    
    # Recive message from client
    def recive(self):
        data = ''
        while True:
            chunk = self.client.recv(self.size).decode('utf-8')
            # print("Chunk:", chunk)
            data += chunk
            if len(chunk) != self.size:
                break
        return data
    
    # Send message to cliend
    def send(self, msg):
        self.client.sendto(msg.encode('utf-8'), ('localhost', 5000))
    
    # Send ad to client
    def pushAd(self):
        with open(os.path.join("advertisement", "ad.txt"), "r") as f:
            for line in f:
                self.send(line)
            print("Ad sent to client")
    
    def mkClients(self):
        users = []
        for filename in glob.glob(os.path.join("clients", '*.txt')):
            info = []
            with open(filename, "r", encoding = "utf-8") as f:
                for line in f:
                    info.append(line.strip('\n'))
                users.append(User(info[0], info[1], info[2], info[3:]))
        return users
        
    def verify(self, cardNr, logIn):
        for user in self.users:
            if user.cardNr == cardNr and user.logIn == logIn:
                print("Verify True")
                return user
        print("Verify false")
        return 'False'
                

    
    
                