package ru.ctf.dao;

import org.hibernate.Session;
import org.hibernate.Transaction;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import ru.ctf.entities.Metric;
import ru.ctf.exceptions.MetricException;
import ru.ctf.utils.HibernateSessionFactoryUtil;

import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import java.util.List;


@Component
public class MetricDAO implements DAO<Long, Metric> {

    @Override
    public void save(Metric metric) throws MetricException {
        try (Session session = openHibernateSession()) {
            Transaction transaction = session.beginTransaction();
            session.save(metric);
            transaction.commit();
        } catch (Exception e) {
            throw new MetricException(HttpStatus.INTERNAL_SERVER_ERROR, "Internal fatal kernel die error");
        }
    }

    @Override
    public Metric get(Long token) {
        return openHibernateSession().get(Metric.class, token);
    }

    @Override
    public List<Metric> getAll() {
        try (Session session = openHibernateSession()) {
            CriteriaBuilder builder = session.getCriteriaBuilder();
            CriteriaQuery<Metric> query = builder.createQuery(Metric.class);
            query = query.select(query.from(Metric.class));
            //session.createQuery("SELECT a FROM Metric a", Metric.class).getResultList();
            return session.createQuery(query).list();
        }
    }

    @Override
    public void delete(Metric metric) {
        try (Session session = openHibernateSession()) {
            Transaction transaction = session.beginTransaction();
            session.delete(metric);
            transaction.commit();
        }
    }

    @Override
    public void update(Metric metric) {
        try (Session session = openHibernateSession()) {
            Transaction transaction = session.beginTransaction();
            session.update(metric);
            transaction.commit();
        }
    }

    private Session openHibernateSession() {
        return HibernateSessionFactoryUtil.getSessionFactory().openSession();
    }
}
