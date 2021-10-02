package ru.ctf.entities;

import org.apache.logging.log4j.util.Strings;

import javax.persistence.*;
import java.sql.Timestamp;

@Entity
@Table(name = "tbl_metric")
public class InnerMetric implements Metric {
    @Id
    private String token;
    private String metainfo;
    private String device;
    private String type;
    private Integer value;
    private Timestamp creationTime;
    private String info;

    public InnerMetric(String token, String device, String type,
                       String metainfo, int value, Timestamp creationTime, String info) {
        this.type = type;
        this.device = device;
        this.token = token;
        this.metainfo = metainfo;
        this.value = value;
        this.creationTime = creationTime;
        this.info = info;
    }

    public InnerMetric() {
        super();
        device = Strings.EMPTY;
        type = Strings.EMPTY;
        metainfo = Strings.EMPTY;
    }

    public String getToken() {
        return token;
    }

    public Timestamp getCreationTime() {
        return creationTime;
    }

    public String getMetainfo() {
        return metainfo;
    }

    @Override
    public String getType() {
        return type;
    }

    @Override
    public String getDevice() {
        return device;
    }

    public int getValue() {
        return value;
    }

    @Override
    public void setValue(int value) {
        this.value = value;
    }

    public String getInfo() {
        return info;
    }

    @Override
    public void setDevice(String device) {
        this.device = device;
    }

    @Override
    public void setType(String type) {
        this.type = type;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public void setMetainfo(String metainfo) {
        this.metainfo = metainfo;
    }

    public void setCreationTime(Timestamp creationTime) {
        this.creationTime = creationTime;
    }

    public void setValue(Integer value) {
        this.value = value;
    }

    public void setInfo(String info) {
        this.info = info;
    }
}
