package ru.ctf.utils;

import ru.ctf.entities.InnerMetric;

import javax.xml.bind.DatatypeConverter;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class TokenCalculator {
    public static String calculateToken(InnerMetric innerMetric) {
        String stringToHash = innerMetric.getDevice() + innerMetric.getType() +
                innerMetric.getValue() + innerMetric.getInfo();
        MessageDigest md;
        try {
            md = MessageDigest.getInstance("MD5");
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(); //todo: сделать норм ошибку
        }
        md.update(stringToHash.getBytes());
        byte[] digest = md.digest();
        return DatatypeConverter.printHexBinary(digest).toUpperCase();
    }
}
