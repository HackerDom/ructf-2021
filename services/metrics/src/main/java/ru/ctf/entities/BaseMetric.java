package ru.ctf.entities;

import org.apache.logging.log4j.util.Strings;

public class BaseMetric implements Metric {
    protected String device;
    protected String type;
    private int value;
    private String info;

    public BaseMetric(String device, String type, int value, String info) {
        this.device = device;
        this.type = type;
        this.value = value;
        this.info = info;
    }

    public BaseMetric() {
        device = Strings.EMPTY;
        type = Strings.EMPTY;
    }

    public void setDevice(String device) {
        this.device = device;
    }

    public void setType(String type) {
        this.type = type;
    }

    public void setValue(int value) {
        this.value = value;
    }

    public void setInfo(String info) {
        this.info = info;
    }

    public String getDevice() {
        return device;
    }

    public String getType() {
        return type;
    }

    public int getValue() {
        return value;
    }

    public String getInfo() {
        return info;
    }
}
