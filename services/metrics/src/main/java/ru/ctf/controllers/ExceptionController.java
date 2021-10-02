package ru.ctf.controllers;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import ru.ctf.exceptions.InvalidJsonException;
import ru.ctf.exceptions.MetricException;

import java.util.Map;

@ControllerAdvice
public class ExceptionController {

    @ExceptionHandler(MetricException.class)
    public ResponseEntity<Map<String, String>> handleMetricException(MetricException metricException) {
        return new ResponseEntity<>(Map.of("message", metricException.getMessage()), HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @ExceptionHandler(InvalidJsonException.class)
    public ResponseEntity<Map<String, String>> handleJsonException(InvalidJsonException metricException) {
        return new ResponseEntity<>(Map.of("message", metricException.getMessage()), HttpStatus.BAD_REQUEST);
    }
}
