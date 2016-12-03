# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-12-03

# This file is launched when ThreadedServer finds a new connection
# Each connection created a ServerThread object 
# The object handles all communication with the client

import socket

class ServerThread(object):
    
    def __init__(self, client, address):
        self.client = client
        self.address= address
        self.size   = 10

    def listenToClient(self):
        size = 1024
        while True:
            try:
                # client.send("Enter card number")
                data = self.client.recv(size)
                print("Recived:", data.decode('utf-8'))
                # getClient(data)
                if data:
                    # Set the response to echo back the recieved data 
                    response = data.upper()
                    self.client.send(response)
                else:
                    raise error('Client disconnected')
            except:
                self.client.close()
                return False
