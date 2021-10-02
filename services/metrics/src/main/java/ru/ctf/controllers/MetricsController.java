package ru.ctf.controllers;

import org.json.JSONObject;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.ctf.entities.InnerMetric;
import ru.ctf.entities.Metric;
import ru.ctf.exceptions.InvalidJsonException;
import ru.ctf.exceptions.MetricException;
import ru.ctf.services.MetricService;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

@RestController
@RequestMapping("/metrics")
public class MetricsController {

    private final MetricService metricService;

    public MetricsController(MetricService metricService) {
        this.metricService = metricService;
    }

    @PutMapping(path = "/save_metric")
    public Map<String, String> saveMetric(@RequestBody String jsonMetricString) throws MetricException, InvalidJsonException {
        JSONObject jsonMetric = new JSONObject(jsonMetricString);
        return Map.of("token", metricService.saveMetric(getMetricFromJson(jsonMetric)));
    }

    @GetMapping
    public Map<String, List<Metric>> getMetrics() {
        return Map.of("metrics", metricService.getAllMetrics());
    }

    @PostMapping(path = "/metric")
    public List<InnerMetric> getMetric(@RequestBody String jsonString) {
        JSONObject json = new JSONObject(jsonString);
        return metricService.getMetric(json.getString("token"));
    }

    private InnerMetric getMetricFromJson(JSONObject jsonMetric) throws InvalidJsonException {
        Set<String> keys = new HashSet<>(jsonMetric.toMap().keySet());
        String fieldDevice = "device";
        String fieldType = "type";
        String fieldValue = "value";
        String fieldMetainfo = "metainfo";
        String fieldInfo = "info";
        if (!keys.contains(fieldDevice) || !keys.contains(fieldType) || !keys.contains(fieldValue) || !keys.contains(fieldInfo)) {
            throw new InvalidJsonException("Invalid json");
        }
        keys.remove(fieldDevice);
        keys.remove(fieldType);
        keys.remove(fieldValue);
        keys.remove(fieldInfo);
        String metainfo = null;
        if (keys.contains(fieldMetainfo)) {
            metainfo = jsonMetric.getString(fieldMetainfo);
            keys.remove(fieldMetainfo);
        }
        if (keys.isEmpty()) {
            try {
                return new InnerMetric(null, jsonMetric.getString(fieldDevice), jsonMetric.getString(fieldType),
                        metainfo, jsonMetric.getInt(fieldValue), null, jsonMetric.getString(fieldInfo));
            } catch (Exception exception) {
                throw new InvalidJsonException("Invalid json");
            }
        }
        throw new InvalidJsonException("Invalid json");
    }
}
