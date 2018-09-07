# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-12-05

# This file should be used to launch the ATM server. Server GUI initializes
# one thread listening for connections and one thread where server admin
# can change the advertisement

import os
import socket
import threading
from ServerThread import ServerThread

# This class initializes a socket and starts listening for connections
class ThreadedServer(threading.Thread):
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.listen()
    
    # If a connection is found, make a ServerThread it
    def listen(self):
        print("Waiting for connections...")
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print("Connected to:", address)
            client.settimeout(120)
            threading.Thread(target =   ServerThread(client, address). \
                                        listenToClient, args = ()).start()

# Make one thread listening for connections (ThreadedServer) and 
# one thread that handles the server administration
class ServerGUI(threading.Thread):
    
    def __init__(self):
        self.listen = threading.Thread( target = ThreadedServer, \
                                        args = ('localhost', 5000)).start()
        threading.Thread(target = self.mkOpsThread(), args = ()).start()
    
    # Present option of changing ads 
    def mkOpsThread(self):
        while True:
            var = input("Adjust advertisement? Press [y/n] anytime...\n")
            if var == 'y':
                self.swAd()

    # Adjust the ad file kept in directory "advertisements"   
    def swAd(self):
        while True:
            slct = (input("(S) Svenska | (E) English: ")).lower()
            if slct == 's' or slct == 'e':
                break
        new_ad  = input("Please enter new advertisement:\n>>>")
        if slct == 's':
            with open(os.path.join("advertisement", "ad_swe.txt"), "w") as f:
                f.write(new_ad)
        if slct == 'e':
            with open(os.path.join("advertisement", "ad_eng.txt"), "w") as f:
                f.write(new_ad)
        print("Advertisement succesfully changed")
        
def Main():
    print("--- Server interface ---\n")
    ServerGUI()

if __name__ == "__main__":
    Main()
