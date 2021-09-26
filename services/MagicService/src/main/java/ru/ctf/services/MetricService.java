package ru.ctf.services;

import org.springframework.stereotype.Component;
import ru.ctf.dao.DAO;
import ru.ctf.entities.Metric;
import ru.ctf.exceptions.MetricException;

import java.util.List;

@Component
public class MetricService {
    private final DAO<Long, Metric> metricDAO;

    public MetricService(DAO<Long, Metric> dao) {
        metricDAO = dao;
    }

    public Metric getMetric(Long token) {
        return metricDAO.get(token);
    }

    public List<Metric> getAllMetrics() {
        return metricDAO.getAll();
    }

    public Long saveMetric(Metric metric) throws MetricException {
        metric.setToken(calculateToken(metric));
        metricDAO.save(metric);
        return metric.getToken();
    }

    private long calculateToken(Metric metric) {
        return (long) metric.getDevice().hashCode() + metric.getType().hashCode();
    }
}
