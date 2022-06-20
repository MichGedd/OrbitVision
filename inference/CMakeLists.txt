cmake_minimum_required(VERSION 3.16)

project(Orbit_Vision C CXX)

set(OpenCV_DIR "${CMAKE_SOURCE_DIR}/external/opencv_build")
set(CMAKE_CXX_FLAGS "-O3")

find_package(OpenCV REQUIRED)

add_subdirectory("${CMAKE_SOURCE_DIR}/external/tensorflow/tensorflow/lite"
	"${CMAKE_CURRENT_BINARY_DIR}/external/tensorflow-lite")

include_directories(${OpenCV_INCLUDE_DIR})

add_executable(Orbit_Vision main.cpp)

target_link_libraries(Orbit_Vision tensorflow-lite)
target_link_libraries(Orbit_Vision ${OpenCV_LIBS})
