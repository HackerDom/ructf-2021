package ru.ctf.controllers;

import org.json.JSONObject;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.ctf.entities.Metric;
import ru.ctf.exceptions.MetricException;
import ru.ctf.services.MetricService;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/metrics")
public class MetricsController {

    private final MetricService metricService;

    public MetricsController(MetricService metricService) {
        this.metricService = metricService;
    }

    @PutMapping(path = "/save_metric")
    public Map<String, Long> saveMetric(@RequestBody Metric metric) throws MetricException {
        return Map.of("token", metricService.saveMetric(metric));
    }

    @GetMapping
    public Map<String, List<Metric>> getMetrics() {
        return Map.of("metrics", metricService.getAllMetrics());
    }

    @PostMapping(path = "/metric")
    public Metric getMetric(@RequestBody String jsonString) {
        JSONObject json = new JSONObject(jsonString);
        return metricService.getMetric(json.getLong("token"));
    }

    @ExceptionHandler(MetricException.class)
    public ResponseEntity<Object> handleException(MetricException e) {
        return new ResponseEntity<>(e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
