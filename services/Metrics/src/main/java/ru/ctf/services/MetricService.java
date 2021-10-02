package ru.ctf.services;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import ru.ctf.dao.DAO;
import ru.ctf.entities.BaseMetric;
import ru.ctf.entities.InnerMetric;
import ru.ctf.entities.Metric;
import ru.ctf.exceptions.MetricException;

import javax.xml.bind.DatatypeConverter;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Timestamp;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

import static ru.ctf.utils.TokenCalculator.calculateToken;

@Component
public class MetricService {
    private final DAO<String, InnerMetric> metricDAO;

    public MetricService(DAO<String, InnerMetric> dao) {
        metricDAO = dao;
    }

    public List<InnerMetric> getMetric(String token) {
        return metricDAO.get(token);
    }

    public List<Metric> getAllMetrics() {
        return innerToBase(metricDAO.getAll());
    }

    public String saveMetric(InnerMetric innerMetric) throws MetricException {
        innerMetric.setToken(calculateToken(innerMetric));
        innerMetric.setCreationTime(Timestamp.valueOf(LocalDateTime.now()));
        metricDAO.save(innerMetric);
        return innerMetric.getToken();
    }

    private List<Metric> innerToBase(List<InnerMetric> innerMetricList) {
        return innerMetricList.stream().map(x -> new BaseMetric(x.getDevice(), x.getType(), x.getValue(), x.getInfo())).collect(Collectors.toList());
    }

    @Scheduled(fixedDelay = Constants.DB_RECORD_TTL)
    private void facilitateTable() {
        metricDAO.facilitateTable(
                Timestamp.valueOf(LocalDateTime.now().minus(Duration.ofMillis(Constants.DB_RECORD_TTL))));
    }

    private static class Constants {
        private static final long DB_RECORD_TTL = 900000;
    }
}
