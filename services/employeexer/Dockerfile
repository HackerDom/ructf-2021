FROM hseeberger/scala-sbt:8u222_1.3.5_2.13.1

COPY . /build
WORKDIR /build
RUN sbt dist || sbt dist

FROM openjdk:13-jdk-alpine3.10
WORKDIR /app
COPY --from=0 /build/target/universal/employeexer-1.0-SNAPSHOT.zip /app
RUN apk add bash && unzip employeexer-1.0-SNAPSHOT.zip
WORKDIR /app/employeexer-1.0-SNAPSHOT

CMD ["./bin/employeexer", "-Dplay.http.secret.key='Q0hBTkdFIE1F'"]
