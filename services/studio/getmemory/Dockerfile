FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive
RUN mkdir -p /app && dpkg --add-architecture i386 && apt update && apt install --yes --no-install-recommends --no-install-suggests build-essential gcc libssl-dev:i386 libc-dev libc6-dev gcc-multilib cmake
COPY main.c /app
COPY CMakeLists.txt /app
COPY private.key /app
WORKDIR /app
RUN cmake --configure . && cmake --build . && ls
