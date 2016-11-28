import java.net.*;
import java.io.*;

/**
   @author Viebrapadata
*/
public class ATMServer {
  
    // Hårdkodat -> Lägg i fil eller ange port i kommandoraden
    private static int connectionPort = 8989; 
    
    // args -> anges i kommandoraden
    public static void main(String[] args) throws IOException {
        
        ServerSocket serverSocket = null;
       
        // Används i System.out
        boolean listening = true;
        
        try {
            serverSocket = new ServerSocket(connectionPort); 
        } catch (IOException e) {
            System.err.println("Could not listen on port: " + connectionPort);
            System.exit(1);
        }
	
        System.out.println("Bank started listening on port: " + connectionPort);
        while (listening)
            // Starta tråd
            new ATMServerThread(serverSocket.accept()).start();

        serverSocket.close();
    }
}
