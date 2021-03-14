cmake_minimum_required(VERSION 3.16)

project(TideSurf)

find_package(Threads REQUIRED)
find_package(Arrow REQUIRED)
find_package(Parquet REQUIRED PATHS /usr/lib/x86_64-linux-gnu/cmake/arrow)
find_package(GTest REQUIRED)


include(ExternalProject)
include(FindPkgConfig)
include(GNUInstallDirs)
include(GoogleTest)
set(THREADS_PREFER_PTHREAD_FLAG ON)

file(GLOB_RECURSE TIDESURF_CPP
    ${PROJECT_SOURCE_DIR}/src/tidesurf/*.cpp
)

file(GLOB_RECURSE TIDESURF_EXECUTABLES
    ${PROJECT_SOURCE_DIR}/src/main/*.cpp
)

file(GLOB_RECURSE TIDESURF_TEST_EXECUTABLES
    ${PROJECT_SOURCE_DIR}/test/*.cpp
)

set(LIBRARY_OUTPUT_PATH "${CMAKE_SOURCE_DIR}/lib/")
include_directories("${PROJECT_SOURCE_DIR}/includes")
link_directories("${CMAKE_SOURCE_DIR}/lib/")


add_library(tidesurf STATIC ${TIDESURF_CPP} src/tidesurf/stock.cpp src/tidesurf/interval_record.cpp includes/tidesurf/interval_record.h src/tidesurf/price_volume_histogram.cpp includes/tidesurf/price_volume_histogram.h)

add_executable(tidesurf_main ${TIDESURF_EXECUTABLES} src/tidesurf/stock.cpp src/tidesurf/interval_record.cpp includes/tidesurf/interval_record.h)
target_link_libraries(tidesurf_main PUBLIC arrow_shared)
target_link_libraries(tidesurf_main PUBLIC parquet_shared)
target_link_libraries(tidesurf_main PUBLIC Threads::Threads)
target_link_libraries(tidesurf_main PUBLIC tidesurf)

enable_testing()
set(TestArgs --foo 1 --bar 2)
add_executable(unit_tests ${TIDESURF_TEST_EXECUTABLES} src/tidesurf/stock.cpp src/tidesurf/interval_record.cpp includes/tidesurf/interval_record.h)
target_link_libraries(unit_tests 
    PUBLIC tidesurf
    PUBLIC GTest::GTest GTest::Main
    PUBLIC arrow_shared
    parquet_shared
    Threads::Threads)
# target_link_directories(unit_tests PUBLIC "${CMAKE_SOURCE_DIR}/lib/")
gtest_add_tests(TARGET unit_tests "${TestArgs}" AUTO)
