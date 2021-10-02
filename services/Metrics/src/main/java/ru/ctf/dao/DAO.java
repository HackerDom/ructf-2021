package ru.ctf.dao;

import ru.ctf.exceptions.MetricException;

import java.sql.Timestamp;
import java.util.List;

public interface DAO<Key, Entity> {
    void save(Entity entity) throws MetricException;
    List<Entity> get(Key key);
    List<Entity> getAll();
    void delete(Entity entity) throws MetricException;
    void update(Entity entity) throws MetricException;
    void facilitateTable(Timestamp deleteBeforeThis);
}
