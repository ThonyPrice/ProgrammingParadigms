import java.io.*;   
import java.net.*;  
import java.util.Scanner;

/**
   @author Snilledata
*/
public class ATMClient {
    private static int connectionPort = 8989;
    
    public static void main(String[] args) throws IOException {
        
        Socket ATMSocket = null;
        PrintWriter out = null;
        BufferedReader in = null;
        String adress = "";

        try {
            adress = args[0];
        } catch (ArrayIndexOutOfBoundsException e) {
            System.err.println("Missing argument ip-adress");
            System.exit(1);
        }
        try {
            ATMSocket = new Socket(adress, connectionPort); 
            out = new PrintWriter(ATMSocket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader
                                    (ATMSocket.getInputStream()));
        } catch (UnknownHostException e) {
            System.err.println("Unknown host: " +adress);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't open connection to " + adress);
            System.exit(1);
        }

        System.out.println("Contacting bank ... ");
        System.out.println(in.readLine()); 

        Scanner scanner = new Scanner(System.in);
        System.out.print("> ");
        int menuOption = scanner.nextInt();
        int userInput;
        out.println(menuOption);
        while(menuOption < 4) {
                if(menuOption == 1) {
                        System.out.println(in.readLine()); 
                        System.out.println(in.readLine());
                        System.out.print("> ");
                        menuOption = scanner.nextInt();
                        out.println(menuOption);           
                } else if (menuOption > 3) {
                    break;
                }	
                else {
                    System.out.println(in.readLine()); 
                    userInput = scanner.nextInt();
                    out.println(userInput);
                    String str;
                    do {
                        str = in.readLine();
                        System.out.println(str);
                    } while (! str.startsWith("(1)"));
                    System.out.print("> ");
                    menuOption = scanner.nextInt();
                    out.println(menuOption);           
                }	
        }		
		
        out.close();
        in.close();
        ATMSocket.close();
    }
}   
