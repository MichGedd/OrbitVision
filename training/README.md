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
    |   model_name_edgetpu.tflite
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


## Original Models

The `/original_models` folder contains base models from the 
[TF2 model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md).


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
Note - Currently this tutorial is aimed at SSD networks. Adjustments may be needed for other models.

1) Create a new project by calling `python scripts/generate_project.py --name=<project name>` from the 
`OrbitVision/training` directory. Until stated otherwise, all paths are assumed to be relative to 
`OrbitVision/training/workspace/<project_name>`
2) Place a zip file of your images in the `/images` folder and rename it to `imgs_orig.zip`. Unzip the folder to 
`images/imgs`. Note - You want as many annotations per object class as possible (an image with two objects of the same
class count as two annotations), ideally over 1000 per object. You can totally get away with les than that (I've done 
~200) but for competition do as many as possible. Idk, get the media team to do it for you or something.
3) Run `python ../../scripts/pad_images.py` to pad all the images to a square.
4) Run `labelImg` in the `images/imgs` directory to annotate all your images. Ensure you use Pascal VOC format.
5) Run `python ../../scripts/partition_dataset.py` to partition the dataset into 90% train images and 10% test images
6) Create a file in `annotations/` called `label_map.pbtxt`. A generic `label_map.pbtxt` is shown below. You must add
an item for each object type you annoted. The `name` should be the name used in labelImg.  

        item {
            id: 1
            name: 'object_name_1'
        }
        
        item {
            id: 2
            name: 'object_name_2'
        }
        
        item {
            ...
        }
        
        ...
        
7) Run `python ../../scripts/create_tf_record.py` to create the `train.record` and `test.record` in `annotations/`
8) Copy a model from `original_models/` into `models/`. Delete everything inside `models/<copied model name>/` except for
the `pipeline.config` file.
9) Edit the `pipeline.config` file in the following areas:
    1) Change `num_classes` to the number of items in your `label_map.pbtxt`
    2) Change `fine_tune_checkpoint` to `../../original_models/<original model name>/checkpoint/ckpt-0`
    3) Change `fine_tune_checkpoint_type` to `detection`
    4) Change `label_map_path` to `annotations/label_map.pbtxt` (Theres two of them).
    5) Change `input_path` to `annotations/train.record` for `train_input_reader` and `annotations/test.record` for
    `eval_input_reader`
10) Run `python ../../scripts/model_main_tf2.py --model_dir=models/<model name> --pipeline_config_path=models/<model name>/pipeline.confg`.
Monitor the training process by running `tensorboard --logdir=models/<model name>`

## Evaluating

To evaluate the model, run `python ../../scripts/model_main_tf2.py --model_dir=models/<model name> --pipeline_config_path=models/<model name>/pipeline.confg
--checkpoint_dir=models/<model name>`. Its a good idea to run the model for a low number of training steps (10k for example)
and then evaluating the model to make sure training is going as expected. If the initial evaluation looks ok, rerun the model
for the full training steps.

## Exporting for TFLite (TODO)

This currently only works for SSD-based models. 

1) Export the model running export_tflite_graph_tf2.py
2) Create the .tflite for the PTIQ and non-PTIQ versions using convert_to_tflite.py
3) Use tflite_model_validate to figure out the equation needed for generating bounding boxes (This converts the [0, 255]
range of the output to [0, 1], which is then multiplied by the input dimensions to get the pixel location
of the bounding box)

## Exporting for Edge TPU (TODO)

Instructions from Coral docs [can be found here](https://coral.ai/docs/edgetpu/compiler/). Use the Edge TPU Compiler to compile the PTIQ .tflite model. You must be running 64-bit Debian 6.0 and be on x86-64
architecture (If you don't have a linux system on hand use Ubuntu 20.04 for WSL).  Install the compiler by running the 
following:

```shell script
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
sudo apt-get update
sudo apt-get install edgetpu-compiler
``` 

Next, export the model by running the following:

```shell script
edgetpu_compiler <model name>.tflite
```