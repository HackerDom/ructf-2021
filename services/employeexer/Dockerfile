FROM hseeberger/scala-sbt:8u222_1.3.5_2.13.1

COPY . /build
WORKDIR /build
RUN sbt dist || sbt dist

FROM openjdk:13-jdk-alpine3.10
WORKDIR /build
COPY --from=0 /build/target/universal/employeexer-1.0-SNAPSHOT.zip /build
RUN apk add bash && unzip employeexer-1.0-SNAPSHOT.zip && mv employeexer-1.0-SNAPSHOT /app
WORKDIR /app

CMD rm RUNNING_PID || true && ./bin/employeexer -Dplay.http.secret.key='Q0hBTkdFIE1F'
