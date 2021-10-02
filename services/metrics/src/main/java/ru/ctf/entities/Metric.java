package ru.ctf.entities;

public interface Metric {

    void setDevice(String device);

    void setType(String type);

    String getDevice();

    String getType();

    int getValue();

    void setValue(int value);

    String getInfo();

    void setInfo(String info);
}
