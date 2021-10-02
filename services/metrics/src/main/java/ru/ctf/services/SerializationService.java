package ru.ctf.services;

public interface SerializationService<Entity, Source> {
    Source serialize(Entity obj);

    Entity deserialize(Source source);
}
