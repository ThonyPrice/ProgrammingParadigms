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
                pick = input("(S) Svenska | (E) English: ")
                if pick == 's' or pick == 'e':
                    self.send(pick)
                    break
            
            # Log in process
            while True:
                print(self.recive(), end="")        # "Enter cardNr"
                self.send(input())                  # Input and send
                print(self.recive(), end="")        # "Enter pinCode"
                self.send(input())                  # Input and send
                verification = self.recive()        # Server verification
                if verification == 'True':
                    break
                print("Error")

            # Main menu
            print(self.recive())                    # Greeting
            while True:
                print(self.recive())                # Options
                menuOp = input(": ")
                self.send(menuOp)                   # Send op
                
                if menuOp == '1':                   # Balance
                    print(self.recive())
                if menuOp == '2' or menuOp == '3':  # Withdrawal/deposit
                    print(self.recive(), end="")
                    self.send(input())
                    if menuOp == '2':
                        print(self.recive(), end="") # Enter PIN (withdraw)
                        self.send(input())
                        print(self.recive())
                if menuOp == '4':
                    break
                if menuOp != '1' and menuOp != '2' and menuOp != '3' and menuOp != '4':
                    print(self.recive())
            
            # Exit or restart        
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
        