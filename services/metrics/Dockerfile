FROM maven:3.8.2-openjdk-16-slim
RUN mkdir /app
WORKDIR /app
COPY ./pom.xml ./pom.xml
RUN mvn dependency:go-offline -B
COPY . /app
RUN mvn package spring-boot:repackage
CMD "java" "-jar" "target/app.jar" "-Xmx1G"
