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
                users.append(User(info[0], info[1], info[3], info[4:]))
        return users
        
    def verify(self, cardNr, logIn):
        for user in self.users:
            if user.cardNr == cardNr and user.logIn == logIn:
                print("Verify True")
                return user
        print("Verify false")
        return 'False'
                

    
    
                