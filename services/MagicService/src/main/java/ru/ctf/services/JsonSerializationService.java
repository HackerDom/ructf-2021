package ru.ctf.services;

import ru.ctf.entities.Metric;

public class JsonSerializationService implements SerializationService<Metric, Long> {
    @Override
    public Long serialize(Metric metric) {
        return null;
    }

    @Override
    public Metric deserialize(Long token) {

        return null;
    }
}
