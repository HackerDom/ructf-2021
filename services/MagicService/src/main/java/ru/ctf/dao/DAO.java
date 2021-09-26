package ru.ctf.dao;

import ru.ctf.exceptions.MetricException;

import java.util.List;

public interface DAO<Key, Entity> {
    void save(Entity entity) throws MetricException;
    Entity get(Key key);
    List<Entity> getAll();
    void delete(Entity entity) throws MetricException;
    void update(Entity entity) throws MetricException;
}
