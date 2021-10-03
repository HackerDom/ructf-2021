cmake_minimum_required(VERSION 3.11)
project(vuln C)

set(CMAKE_C_STANDARD 99)

add_executable(vuln main.c)
TARGET_LINK_LIBRARIES(vuln rt)
