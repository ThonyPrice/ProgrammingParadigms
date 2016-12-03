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
                verification = self.recive()
                if verification == 'True':
                    break
                print("Invalid, try again")
            
            # Main menu
            print(self.recive())
            while True:
                menuOp = input(">>> ")
                self.send(menuOp)
                if menuOp == '1': 
                    print(self.recive())
                    print(self.recive())
                if menuOp == '2' or menuOp == '3':
                    print(self.recive())
                    amount = input(">>> ")
                    self.send(amount)
                    if menuOp == '2':
                        print(self.recive()) # Enter PIN
                        pinCode = input(">>> ")
                        self.send(pinCode)
                    
                if menuOp == '4':
                    break
                if menuOp != '1' and menuOp != '2' and menuOp != '3' and menuOp != '4':
                    print("Invalid, try again")
                    
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
        