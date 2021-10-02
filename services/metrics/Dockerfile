FROM maven:3.8.2-openjdk-16-slim as build
LABEL stage=builder
RUN mkdir /app
WORKDIR /app
COPY ./pom.xml ./pom.xml
RUN mvn dependency:go-offline -B
COPY . /app
RUN mvn clean package spring-boot:repackage

FROM openjdk:16-jdk-alpine
COPY --from=build /app/target/app.jar /usr/app/app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/usr/app/app.jar", "-Xmx1G"]