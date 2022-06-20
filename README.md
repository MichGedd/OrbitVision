# OrbitVision

---
Orbit Vision is an Object Detection project developed by FRC Team 1360

---

### Prerequisites

Before you begin: Running this project is super annoying on Windows. MinGW toolchain isn't compatable with Tensorflow, and
I haven't found a way to switch the C++ version when using MSVC with CMake. TODO - Figure out how to run OpenCV + CUDA
toolkit on WSL2.

Development Support

| Feature   | Operating System | Toolchain / Environment | CUDA                                                        | Build                   | Run                                                           |
|-----------|------------------|-------------------------|-------------------------------------------------------------|-------------------------|---------------------------------------------------------------|
| Training  | Windows          | Command Prompt          | Yes                                                         | N/A                     | N/A                                                           |
| Training  | Windows          | WSL2                    | Apperently Yes, but I haven't figured it out                | N/A                     | N/A                                                           |
| Training  | Linux            | Terminal                | I haven't tried it, but there's no reason it shouldn't work | N/A                     | N/A                                                           |
| Inference | Windows          | MinGW                   | N/A                                                         | No                      | No                                                            |
| Inference | Windows          | MSVC                    | N/A                                                         | Need to figure this out | Need to figure this out                                       |
| Inference | Windows          | gcc (WSL2)              | N/A                                                         | Yes                     | Should be good for Win11, need to figure out OpenCV for Win10 |
| Inference | Linux            | gcc                     | N/A                                                         | Yes                     | Yes                                                           |

- Python >= 3.5 (Training Only)
- CMake >= 3.16 (App Only)
- CUDA Compatable GPU (Highly Recommended, Training Only)

Steps:

1) Create a python virtual environment in project root directory called "venv"
2) Run the setup script to initialize the git submodules, set up your venv, and copy some files from Tensorflow
3) ???
4) Proft

---

### Setup

---