cmake_minimum_required(VERSION 3.10)

project(TideSurf)
set(THREADS_PREFER_PTHREAD_FLAG ON)
set(SOURCES ${PROJECT_SOURCE_DIR}/src/server.cpp ${PROJECT_SOURCE_DIR}/src/main.cpp)


find_package(Threads REQUIRED)
find_package(Arrow REQUIRED)

add_executable(tidesurf ${SOURCES})

target_link_libraries(tidesurf PRIVATE arrow_shared)
target_link_libraries(tidesurf PRIVATE Threads::Threads)
target_include_directories(tidesurf PRIVATE ${PROJECT_SOURCE_DIR}/includes/tidesurf)

find_package(GTest REQUIRED)
enable_testing()
include(GoogleTest)
set(TestArgs --foo 1 --bar 2)
add_executable(unit_tests ./test/float_value_test.cpp)
target_link_libraries(unit_tests GTest::GTest GTest::Main)
gtest_add_tests(TARGET unit_tests "${TestArgs}" AUTO)
