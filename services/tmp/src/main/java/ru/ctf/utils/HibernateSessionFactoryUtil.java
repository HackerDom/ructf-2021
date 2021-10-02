package ru.ctf.utils;

import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import ru.ctf.app.Application;
import ru.ctf.entities.InnerMetric;

import java.io.IOException;
import java.util.Properties;

public class HibernateSessionFactoryUtil {
    private static SessionFactory sessionFactory;
    private static final String HIBERNATE_PROPS = "hibernate.properties";

    public static SessionFactory getSessionFactory() {
        if (sessionFactory == null) {
            Configuration configuration = new Configuration();
            Properties properties = new Properties();
            try {
                properties.load(Application.class.getClassLoader().getResourceAsStream(HIBERNATE_PROPS));
            } catch (IOException e) {
                throw new IllegalArgumentException("Troubles with '%s' file".formatted(HIBERNATE_PROPS), e);
            }
            configuration.addProperties(properties);
            configuration.addAnnotatedClass(InnerMetric.class);
            StandardServiceRegistryBuilder builder = new StandardServiceRegistryBuilder()
                    .applySettings(configuration.getProperties());

            sessionFactory = configuration.buildSessionFactory(builder.build());
        }

        return sessionFactory;
    }
}
