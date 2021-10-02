package ru.ctf.udp;

import javax.xml.crypto.Data;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.concurrent.ThreadPoolExecutor;

public class Starter {
    public static void main(String[] args) {
        Thread th1 = new Thread(() -> talk(8484));
        Thread th2 = new Thread(() -> talk(8083));
        th1.start();
        th2.start();

        try {
            th1.join();
            th2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private static void talk(int port) {
        try (DatagramSocket sock = new DatagramSocket(port)) {
            for (int i = 0; i < 25; i++){
                byte[] hWord = "Hello world!".getBytes();
                DatagramPacket pack = new DatagramPacket(hWord, hWord.length);
                pack.setAddress(InetAddress.getLocalHost());
                pack.setPort(8585);
                sock.send(pack);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
