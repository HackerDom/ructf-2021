package ru.ctf.udp;

import java.io.IOException;
import java.net.*;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

public class ServerUDP {
    private static ServerUDP instance;
    private static final int PORT = 8585;

    private final ThreadPoolExecutor pool;
    private final DatagramSocket socket;

    public static void main(String[] args) {
        ServerUDP a = ServerUDP.getInstance();
        a.run();
    }

    private ServerUDP()  {
        pool = (ThreadPoolExecutor) Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors() + 1);
        try {
            InetAddress addr = InetAddress.getLocalHost();
            socket = new DatagramSocket(PORT, addr);
        } catch (SocketException | UnknownHostException e) {
            throw new RuntimeException(e);
        }
    }

    public void run() {
        try (socket){
            while (true) {
                pool.execute(() -> {
                    try {
                        talk();
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                });
            }
        }
    }

    private void talk() throws IOException {
        DatagramPacket pack = new DatagramPacket(new byte[512], 512);
        socket.receive(pack);
        socket.send(pack);
    }

    public static ServerUDP getInstance() {
        if (instance == null) {
            instance = new ServerUDP();
        }

        return instance;
    }
}
