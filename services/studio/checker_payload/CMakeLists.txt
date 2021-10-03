cmake_minimum_required(VERSION 3.11)
project(checker_payload C)

set(CMAKE_C_STANDARD 99)

add_executable(checker_payload main.c)
TARGET_LINK_LIBRARIES(checker_payload rt)
