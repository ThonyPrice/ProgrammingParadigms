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
                # msg = self.recive()
                data = ''
                while True:
                    chunk = self.client.recv(self.size).decode('utf-8')
                    print("Chunk:", chunk)
                    data += chunk
                    if len(chunk) != self.size:
                        break
                print("This...")
                print("Recived from:", self.address,":", data)
                print("That.")
                # getClient(data)
                if data:
                    # Set the response to echo back the recieved data 
                    response = data.upper()
                    print("Ja")
                    self.client.sendto(response.encode('utf-8'), ('localhost', 5000))
                    print("Nej")
                else:
                    raise error('Client disconnected')
            except:
                print("Exception caught!")
                self.client.close()
                return False
    
    def recive(self):
        data = ''
        while True:
            chunk = self.client.recv(self.size).decode('utf-8')
            print("Chunk:", chunk)
            if len(chunk) == 0:
                break
            data += chunk
        return data