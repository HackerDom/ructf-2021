package ru.ctf.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import ru.ctf.dao.MetricDAO;
import ru.ctf.entities.Metric;

@SpringBootApplication
@ComponentScan("ru.ctf.*")
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
