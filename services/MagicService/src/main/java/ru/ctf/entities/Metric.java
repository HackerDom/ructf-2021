package ru.ctf.entities;

import org.apache.logging.log4j.util.Strings;

import javax.persistence.*;

@Entity
@Table(name = "tbl_metric")
public class Metric {
    @Id
    private Long token;

    private String device;
    private String type;
    private String metainfo;


    public Metric(Long token, String device, String type, String metainfo) {
        this.device = device;
        this.token = token;
        this.type = type;
        this.metainfo = metainfo;
    }

    public Metric() {
        device = Strings.EMPTY;
        type = Strings.EMPTY;
        metainfo = Strings.EMPTY;
    }

    public String getDevice() {
        return device;
    }

    public Long getToken() {
        return token;
    }

    public void setToken(Long token) {
        this.token = token;
    }

    public void setDevice(String device) {
        this.device = device;
    }

    public void setMetainfo(String metainfo) {
        this.metainfo = metainfo;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getMetainfo() {
        return metainfo;
    }

    public String getType() {
        return type;
    }
}
