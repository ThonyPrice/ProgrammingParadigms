import socket

class TCPclient(object):
    
    def __init__ (self):
        self.host   = 'localhost'
        self.port   = 5000
        self.size   = 10
        self.s      = socket.socket()

    def talk(self):
        self.s.connect((self.host, self.port))
        while True:
            
            # Recive advertisement
            data = self.recive()            
            print("Recived:", data)
            
            # Send language request
            while True:                     
                pick = input("Enter 's' for Swedish or 'e' for English: ")
                if pick == 's' or pick == 'e':
                    self.send(pick)
                    break
            
            # Log in process
            while True:
                cardNr = input("Enter your card number, 4 digits: ")
                self.send(cardNr)
                logIn = input("Enter your passcode, 4 digits: ")
                self.send(logIn)
            print("END")
                
            message = str(input(">>> "))    # Let user make input
            print("Send...")
            self.s.sendto(message.encode('utf-8'), ('localhost', 5000))            # Send message to server
            data = self.recive()
            print("Recived from server", data)
        
        s.close()

    def recive(self):
        data = ''
        while True:
            chunk = self.s.recv(self.size).decode('utf-8')
            # print("Chunk:", chunk)
            data += chunk
            if len(chunk) != self.size:
                break
        return data

    def send(self, msg):
        self.s.sendto(msg.encode('utf-8'), (self.host, self.port))

def Main():
    print("--- Client interface ---\n")
    TCPclient().talk()
    
if __name__ == '__main__':
    Main()
        