# Steps
# 1) Install libedgetpu runtime from apt
# 2) Clone tensorflow and libedgetpu from git
# 3) Run cmake and make
# 4) Run libcamerify ./OrbitVision if using the RPi camera

cmake_minimum_required(VERSION 3.16)

project(Orbit_Vision C CXX)

set(OpenCV_DIR "/usr/lib/aarch64-linux-gnu/cmake/opencv4/")
# set(CMAKE_CXX_FLAGS "-O3")

find_package(OpenCV REQUIRED)

add_subdirectory("${CMAKE_SOURCE_DIR}/../tensorflow/tensorflow/lite"
	"${CMAKE_CURRENT_BINARY_DIR}/external/tensorflow-lite")

include_directories(${OpenCV_INCLUDE_DIR})

# Make sure the path is correct

include_directories("../libedgetpu/tflite/public")

add_executable(Orbit_Vision main.cpp)

# target_link_libraries(Orbit_Vision ${CMAKE_DL_LIBS})
# target_link_libraries(Orbit_Vision INTERFACE -ldl)
target_link_libraries(tensorflow-lite INTERFACE -ldl)
target_link_libraries(Orbit_Vision tensorflow-lite)
target_link_libraries(Orbit_Vision ${OpenCV_LIBS})

# Make sure the path is correct

target_link_libraries(Orbit_Vision "/usr/lib/aarch64-linux-gnu/libedgetpu.so.1")
