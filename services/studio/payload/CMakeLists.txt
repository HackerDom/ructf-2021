cmake_minimum_required(VERSION 3.16)
project(payload C)

set(CMAKE_C_STANDARD 99)

add_executable(payload main.c)
TARGET_LINK_LIBRARIES(payload rt)
