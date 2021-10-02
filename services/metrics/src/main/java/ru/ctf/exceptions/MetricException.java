package ru.ctf.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.server.ResponseStatusException;

@ResponseStatus(value = HttpStatus.INTERNAL_SERVER_ERROR)
public class MetricException extends Exception {

    public MetricException(String message) {
        super(message);
    }
}
