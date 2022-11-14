# Overview

This directory contains the code to run the model. This guide builds and runs the model for Raspberry Pi OS 64-bit,
running a MIPI CSI camera and using a Coral Edge USB Accelerator.

## Setup

Install dependencies:

```shell script
sudo apt-get update && sudo apt-get upgrade
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install libedgetpu1-std libopencv-dev cmake
```

## Build

In the project root folder (`OrbitVision/`) make a directory called `build`

```shell script
mkdir build
cd build
```

The CMake paths are dependant on the folder location so make sure it's there.  Next, build the project using CMake. This
will take some time when running on a Raspberry Pi.

```shell script
cmake ../inference
make -j3
```

## Run

Run the file with `libcamerify` to interface with the camera

```shell script
libcamerify ./Orbit_Vision
```

## TODO

- Compile libedgetpu and opencv from source rather than using the debian packages
- Change the executable name from `OrbitVision` to `Orbit_Vision`
- Add WPILib stuff for interfacing with NetworkTables 
- Figure out cross compiling for aarch64

## WPILib

- make sure libgl1-mesa-dev, libxinerama-dev, libxcursor-dev, libxi-dev, libxrandr-dev and libssh-dev are installed via apt (may not need to do this)
- If you get a 403 error when downloading Khronos OpenGL libraries, change the URL to the registery.khronos version rather than khronos.org/registry (probably don't need to do this)
- cmake -DWITH_JAVA=OFF -DWITH_TESTS=OFF -DWITH_CSCORE=OFF -DWITH_WPIMATH=OFF -DWITH_SIMULATION_MODULES=OFF -DWITH_GUI=OFF
