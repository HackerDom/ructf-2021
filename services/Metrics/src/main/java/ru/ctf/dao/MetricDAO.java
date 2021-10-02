package ru.ctf.dao;

import org.hibernate.Session;
import org.hibernate.Transaction;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import ru.ctf.entities.InnerMetric;
import ru.ctf.exceptions.MetricException;
import ru.ctf.utils.HibernateSessionFactoryUtil;

import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaDelete;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;
import java.sql.Timestamp;
import java.util.List;


@Component
public class MetricDAO implements DAO<String, InnerMetric> {

    @Override
    public void save(InnerMetric innerMetric) throws MetricException {
        try (Session session = openHibernateSession()) {
            Transaction transaction = session.beginTransaction();
            session.save(innerMetric);
            transaction.commit();
        } catch (Exception e) {
            throw new MetricException("Duplicate token");
        }
    }

    @Override
    public List<InnerMetric> get(String token) {
        try (Session session = openHibernateSession()) {
            CriteriaBuilder builder = session.getCriteriaBuilder();
            CriteriaQuery<InnerMetric> query = builder.createQuery(InnerMetric.class);
            Root<InnerMetric> root = query.from(InnerMetric.class);
            query = query.where(builder.like(root.get("token"), token + "%"));
            query = query.select(root);

            return session.createQuery(query).list();
        }
    }

    @Override
    public List<InnerMetric> getAll() {
        try (Session session = openHibernateSession()) {
            CriteriaBuilder builder = session.getCriteriaBuilder();
            CriteriaQuery<InnerMetric> query = builder.createQuery(InnerMetric.class);
            query = query.select(query.from(InnerMetric.class));
            //session.createQuery("SELECT a FROM Metric a", Metric.class).getResultList();
            return session.createQuery(query).list();
        }
    }

    @Override
    public void delete(InnerMetric innerMetric) {
        try (Session session = openHibernateSession()) {
            Transaction transaction = session.beginTransaction();
            session.delete(innerMetric);
            transaction.commit();
        }
    }

    @Override
    public void update(InnerMetric innerMetric) {
        try (Session session = openHibernateSession()) {
            Transaction transaction = session.beginTransaction();
            session.update(innerMetric);
            transaction.commit();
        }
    }

    @Override
    public void facilitateTable(Timestamp deleteBeforeThis) {
        try (Session session = openHibernateSession()) {
            Transaction transaction = session.beginTransaction();
            session.createQuery(createTimeCriteriaDelete(deleteBeforeThis, session)).executeUpdate();

            transaction.commit();
        }
    }

    private CriteriaDelete<InnerMetric> createTimeCriteriaDelete(Timestamp deleteBeforeThis, Session session) {
        CriteriaBuilder cb = session.getCriteriaBuilder();
        CriteriaDelete<InnerMetric> delete = cb.createCriteriaDelete(InnerMetric.class);
        Root<InnerMetric> root = delete.from(InnerMetric.class);
        delete.where(cb.lessThanOrEqualTo(root.get("creationTime"), deleteBeforeThis));
        return delete;
    }

    private Session openHibernateSession() {
        return HibernateSessionFactoryUtil.getSessionFactory().openSession();
    }
}
