package sploits;

public class HashCodeCalculator {
    public static long calculateHash(String device, String type) {
        return (long) device.hashCode() + type.hashCode();
    }
}
