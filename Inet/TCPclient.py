import socket

def Main():
    host    = '127.0.0.1'
    print("--- Client interface ---\n")
    port    = int(input("Please enter a port: "))
    
    s       = socket.socket()
    s.connect((host, port))       # Connect to server
    
    message = input("-> ")          # Let user make input
    while message != 'q':           # q == quit
        s.send(message)             # Send message to server
        data = s.recv(1024)         # Recive data from server 
        print("Recived from server", str(data))
        message = input("-> ")          # Let user make input
    
    s.close()
    
if __name__ == '__main__':
    Main()
        