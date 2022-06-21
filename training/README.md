# Overview

This directory is for training and exporting models to use for the Orbit Vision application.  

**IMPORTANT** : Make sure to set up your python environment!

---

## Scripts

The `/scripts` folder contains scripts used to preprocess, train, and export models.

---

## Workspace

For more information and a walkthrough, see [here](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html).

The `/workspace` directory contains multiple different projects. Each project contains models and training data for a 
specific group of objects. The structure of each project should be as follows:

```
project_name
|___annotations
|___exported_models
|___images
|___models
```

### Annotations

The `project_name/annotations` folder contains the following files

```
annotations
|   label_map.pbtxt
|   test.record
|   train.record
```


### Exported Models

The `project_name/exported_models` folder contains the following

```
exported_models
|___model_name
    |___model_name
        |___checkpoint
        |___saved_model
        |   pipeline.config
    |   model_name.tflite
    |   model_name_PTIQ.tflite
|___model_name_2
    |   ...
```

### Images

The `project_name/images` folder contains the following

```
images
|___imgs
    |   Complete set of preprocessed and annotated images
|___test
    |   Train images and annotations
|___train
    |   Test images and annotations
|   imgs_orig.zip
```

imgs_orig.zip is a zip file of the original, unaltered, unannotated images. We are currently pushing duplicates of 
images, there might be a better way to do this.

### Models

TODO - Write a description here

---

## Original Models

The `/original_models` folder contains base models from the 
[TF2 model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md).

___

# Tutorial

The following tutorial has been adapted from the
[TensorFlow 2 Object Detection API tutorial](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/index.html).
This tutorial covers setup and training an object detection model.

## Setup

Honestly, for the most part I would just follow the link above for setup.

1) If you have not already done so, create a python virtual environment by running `python -m venv venv` in the project
root directory. Next run `source ./venv/bin/activate` if on Linux, or `./venv/Scripts/activate.bat` if on Windows to 
activate the virtual environment. Run `pip -r requirements.txt` to install the proper python packages. If you want GPU
support (highly recommended if you have an Nvidia GPU), follow the instal instructions in the link at the top of the
section.
2) [Download](https://github.com/protocolbuffers/protobuf/releases) and extract protobuf (version 3.20.1 is used in)
this tutorial). Add `<PATH_TO_PROTOBUF>/bin` to Path. In a new terminal window, run `protoc object_detection/protos
/*.proto --python_out=.` from the `OrbitVision/submodules/models/research` folder.
3) Run `python object_detection/builders/model_builder_tf2_test.py` to confirm that everything is working. If you have
an error with protobuf, run `pip install --upgrade protobuf==3.20.1`.

## Training
1) Create a new project by calling `python scripts/generate_project.py --name=<project name>` from the 
`OrbitVision/training` directory. Until stated otherwise, all paths are assumed to be relative to 
`OrbitVision/training/workspace/<project_name>`
2) Place a zip file of your images in the `/images` folder and rename it to `imgs_orig.zip`. Unzip the folder to 
`images/imgs`.


