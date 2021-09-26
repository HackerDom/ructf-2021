package ru.ctf.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

public class MetricException extends ResponseStatusException {

    public MetricException(HttpStatus status, String reason) {
        super(status, reason);
    }
}
