FROM maven
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN mvn clean package spring-boot:repackage
CMD "java" "-jar" "target/app.jar"
