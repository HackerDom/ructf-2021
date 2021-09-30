cmake_minimum_required(VERSION 3.16)
project(deallocmemory C)

set(CMAKE_C_STANDARD 99)

#add_executable(deallocmemory main.c)
SET(CMAKE_LIBRARY_PATH "/usr/lib/i386-linux-gnu")
include_directories(BEFORE /usr/include/i386-linux-gnu)

add_executable(deallocmemory main.c)

#set_target_properties(deallocmemory PROPERTIES COMPILE_FLAGS "-m32 -I/usr/local/opt/openssl/include" LINK_FLAGS "-m32 -L/usr/local/opt/openssl/lib")
set_target_properties(deallocmemory PROPERTIES COMPILE_FLAGS "-m32" LINK_FLAGS "-m32")

#set(OPENSSL_ROOT_DIR /usr/local/opt/openssl/*)
find_package(OpenSSL REQUIRED)
target_link_libraries(deallocmemory OpenSSL::SSL)

TARGET_LINK_LIBRARIES(deallocmemory rt)
