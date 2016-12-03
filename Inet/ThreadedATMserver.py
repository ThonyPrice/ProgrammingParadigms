# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-12-02

# Info...

import socket
import threading
import os

class ThreadedServer(object):
    
    # Initialize socket
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
    
    # Listen for new connections    
    def listen(self):
        self.sock.listen(5)
        while True:
            # select  = input("Change advertisement? [y/n]\n>>>").lower()
            # if select == "y":
            #     self.swAd()
            print("Listening for connections...")
            client, address = self.sock.accept()
            print("Connected to:", address)
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
            
    # Listen to client
    def listenToClient(self, client, address):
        # Restrict size of messages to 10 bytes
        size = 1024
        while True:
            try:
                # self.pushAd(client)
                # self.getLang(client)
                print("This")
                client.send(str("Enter card number"))
                print("That")
                data = client.recv(size)
                print("Recived:", data)
                # self.getClient(data)
                if data:
                    # Set the response to echo back the recieved data 
                    response = data.upper()
                    client.send(response)
                else:
                    raise error('Client disconnected')
            except:
                print("Exception caught!")
                client.close()
                return False
    
    # Switch the advertisement
    def swAd(self):
        new_ad  = input("Please enter new advertisement:\n>>>")
        with open(os.path.join("files", "ad.txt"), "w") as f:
            f.write(new_ad)
        
    # Send ad to client
    def pushAd(self, client):
        with open(os.path.join("files", "ad.txt"), "r") as f:
            for line in f:
                print("Sending ad...")
                client.send(line)
        print("Ad sent to client")
            
    # This is not functional yet...        
    def getClient(self, data):
        print("getClient")
        # file_name = (str(data) + str('.txt')) % name
        # print(file_name)
        try:
            with open("data.txt" % name, "r", encoding = "utf-8") as sData:
                print("File open")
                for line in sData:
                    print(line)
        except:
            print("False")
    
# if __name__ == "__main__":
#     port_num = input("Port? ")
#     ThreadedServer('127.0.0.1',port_num).listen()