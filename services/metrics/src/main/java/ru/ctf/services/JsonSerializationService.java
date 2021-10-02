package ru.ctf.services;

import ru.ctf.entities.InnerMetric;

public class JsonSerializationService implements SerializationService<InnerMetric, Long> {
    @Override
    public Long serialize(InnerMetric innerMetric) {
        return null;
    }

    @Override
    public InnerMetric deserialize(Long token) {

        return null;
    }
}
