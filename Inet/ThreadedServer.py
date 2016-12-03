# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-12-03

# This file should be used to launch the ATM server and start listening
# for connections. When a connection is found a ServerThread is created.
# This is where the server GUI is implemented.

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
        threading.Thread(target = self.mkOpsThread, args = ()).start()
        ServerThread(client, address).listenToClient()
    
    def mkOpsThread(self):
        while True:
            var = input("Adjust advertisement? Press [y/n] anytime:\n")
            if var == 'y':
                print("Yey!")

    # Switch the advertisement
    def swAd(self):
        while True:
            slct = (input("(S) Svenska | (E) English: ")).lower()
            if slct == 's' or slct == 'e':
                break
        new_ad  = input("Please enter new advertisement:\n>>>")
        if slct == 's':
        with open(os.path.join("files", "ad_swe.txt"), "w") as f:
            f.write(new_ad)
        if slct == 'e':
        with open(os.path.join("files", "ad_eng.txt"), "w") as f:
            f.write(new_ad)
            
def Main():
    print("--- Server interface ---\n")
    # port    = int(input("Please enter a port: "))
    print("Waiting for connections...")
    ThreadedServer('localhost', 5000).listen()

if __name__ == "__main__":
    Main()

