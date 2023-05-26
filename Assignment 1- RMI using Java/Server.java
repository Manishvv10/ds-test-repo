import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;

public class Server implements Service {
    private ArrayList<String> messages = new ArrayList<>();

    public Server() throws RemoteException {
        UnicastRemoteObject.exportObject(this, 0);
    }

    public int sendSum(int[] arr) throws RemoteException {
        int sum =0;
        System.out.println("----------NEW ITERATION----------");
        for(int i=0;i<arr.length;i++){
            System.out.println("Received Number "+(i+1)+" from client: "+arr[i]);
            sum+=arr[i];
        }
        System.out.println("Sum sent to the client: "+sum);
        return sum;
    }

    public static void main(String[] args) {
        try {
            Server server = new Server();
            Registry registry = LocateRegistry.createRegistry(1099);
            Naming.rebind("rmi://localhost/Service", server);
            System.out.println("Server ready");
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}

interface Service extends java.rmi.Remote {
    int sendSum(int[] arr) throws RemoteException;
}

