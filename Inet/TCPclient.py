import socket

def Main():
    host    = '127.0.0.1'
    print("--- Client interface ---\n")
    # port    = int(input("Please enter a port: "))
    size    = 10
    
    s       = socket.socket()
    s.connect((host, 5000))       # Connect to server
    
    message = ">>>"
    while message != 'q':               # q == quit
        message = str(input(">>> "))    # Let user make input
        s.sendto(message.encode('utf-8'), ('localhost', 5000))            # Send message to server
        data = ''
        while True:
            chunk = s.recv(size).decode('utf-8')
            print("Chunk:", chunk)
            data += chunk
            if len(chunk) != size:
                break
        print("Recived from server", data)
    
    s.close()
    
if __name__ == '__main__':
    Main()
        