# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-12-03

# This file should be used to launch the ATM server and start listening
# for connections. When a connection is found a ServerThread is created.
# This is where the server GUI should be implemented. (TO-DO)

import socket
import threading
from ServerThread import ServerThread

class ThreadedServer(object):
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print("Connected to:", address)
            client.settimeout(120)
            threading.Thread(target = self.mkServerThread, args = (client,address)).start()
            
    def mkServerThread(self, client, address):
        ServerThread(client, address).listenToClient()
        
def setup_host():
    
    print("--- Server interface ---\n")
    # port    = int(input("Please enter a port: "))
    print("Waiting for connections...")
    ThreadedServer('localhost', 5000).listen()

def Main():
    setup_host()

if __name__ == "__main__":
    Main()

