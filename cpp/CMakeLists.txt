cmake_minimum_required(VERSION 3.10)

project(TideSurf)
include(ExternalProject)
include(FindPkgConfig)
include(GNUInstallDirs)
set(THREADS_PREFER_PTHREAD_FLAG ON)

file(GLOB_RECURSE TIDESURF_EXECUTABLES
    ${PROJECT_SOURCE_DIR}/src/*.cpp
)

file(GLOB_RECURSE TIDESURF_TEST_EXECUTABLES
    ${PROJECT_SOURCE_DIR}/test/*.cpp
)


find_package(Threads REQUIRED)
find_package(Arrow REQUIRED)
find_package(Parquet REQUIRED PATHS /usr/lib/x86_64-linux-gnu/cmake/arrow)

add_executable(tidesurf ${TIDESURF_EXECUTABLES})
target_link_libraries(tidesurf PRIVATE arrow_shared)
target_link_libraries(tidesurf PRIVATE parquet_shared)
target_link_libraries(tidesurf PRIVATE Threads::Threads)
target_include_directories(tidesurf PRIVATE ${PROJECT_SOURCE_DIR}/includes)
target_include_directories(tidesurf PRIVATE ${PROJECT_SOURCE_DIR}/includes)

find_package(GTest REQUIRED)
enable_testing()
include(GoogleTest)
set(TestArgs --foo 1 --bar 2)
add_executable(unit_tests ${TIDESURF_TEST_EXECUTABLES})
target_include_directories(unit_tests PRIVATE ${PROJECT_SOURCE_DIR}/includes/tidesurf)
target_link_libraries(unit_tests GTest::GTest GTest::Main)
gtest_add_tests(TARGET unit_tests "${TestArgs}" AUTO)
