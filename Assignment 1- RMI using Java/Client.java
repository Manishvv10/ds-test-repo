import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Scanner;

public class Client implements Runnable {
    private Service service;

    public Client(Service service) {
        this.service = service;
    }

    public void run() {
        Scanner sc = new Scanner(System.in);
        while (true) {
            int[] num = new int[5];
            int sum=0;
            System.out.println("----------NEW ITERATION----------");
            for(int i=0;i<num.length;i++){
                System.out.print("Enter Number "+(i+1)+": ");
                num[i]=sc.nextInt();
            }
            try {
                sum = service.sendSum(num);
                System.out.println("Sum received from the server: "+sum);
                double avg = (double)sum/5;
                System.out.println("Calculation Average (Sum/5): "+avg);
            } catch (RemoteException e) {
                System.out.println(e);
            }
        }
    }

    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.getRegistry(1099);
            Service service = (Service) Naming.lookup("rmi://localhost/Service");
            Client client = new Client(service);
            Thread thread = new Thread(client);
            thread.start();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}
