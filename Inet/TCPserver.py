# Programmeringparadigm     Lab Inet 
# Created by:               Thony Price 
# Last revision:            2016-11-29

# Description:
# This file should be used to launch the ATM server.

from ThreadedATMserver import ThreadedServer

def setup_host():
    
    host    = '127.0.0.1'       # Set up host to be this machine
    print("--- Server interface ---\n")
    port    = int(input("Please enter a port: "))
    
    listening = True
    try:
        print("Bank started listening on port:", port)
        while listening:
            ThreadedServer(host, port).listen()
            
    except:
        print("Could not listen on port", port)
        print("Please restart server and try again")  

def Main():
    setup_host()

if __name__ == "__main__":
    Main()

