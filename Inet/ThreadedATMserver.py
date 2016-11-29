# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-11-29

# Info...

import socket
import threading

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
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                client.send("Enter card number")
                data = client.recv(size)
                getClient(data)
                if data:
                    # Set the response to echo back the recieved data 
                    response = data.upper()
                    client.send(response)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

# if __name__ == "__main__":
#     port_num = input("Port? ")
#     ThreadedServer('127.0.0.1',port_num).listen()