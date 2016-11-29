# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-11-29

# Info...

import ThreadedServer

def setup_host():
    
    host    = '127.0.0.1'       # Set up host to be this machine
    print("--- Server interface ---\n")
    port    = int(input("Please enter a port: "))

    s       = socket.socket()   # Create socket object
    s.bind((host, port))        # Bind the socket host to port
    s.listen(2)                 # Tell our server to start listen for 1 connection
    c, addr = s.accept()        # Returns connection and adress
    print("Connection from", str(addr))
    
    # Talk to the person that's trying to send us data (forever)
    while True: 
        data = c.recv(1024)         # Buffer byte size of recived data
        if not data:                # (If ther's no connection)
            break 
        print("From connected user", str(data))
        data = str(data).upper()
        print("Sending", str(data))
        c.send(data)
    c.close()

def Main():
    setup_host()
    

if __name__ == "__main__":
    Main()

