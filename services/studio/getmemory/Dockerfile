FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /app
RUN dpkg --add-architecture i386 && apt update && apt install --yes --no-install-recommends --no-install-suggests build-essential gcc libssl-dev:i386 libc-dev libc6-dev gcc-multilib cmake
