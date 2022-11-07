import tensorflow as tf
import cv2 as cv
import numpy as np
import glob
import random


def representative_dataset():
    image_names = [f for f in glob.glob("images/imgs/*.jpg")]
    random.shuffle(image_names)

    for name in image_names[:100]:
        img = cv.imread(name)
        img = cv.resize(img, (300, 300), interpolation=cv.INTER_AREA)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = (2.0 / 255.0) * img - 1.0
        img = np.float32(img)
        yield [img[tf.newaxis, ...]]


if __name__ == "__main__":
    converter = tf.lite.TFLiteConverter.from_saved_model("exported_models/FRC_2022_model_nofpn/saved_model")
    post_training_quantization = True

    if post_training_quantization:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = representative_dataset
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8, tf.lite.OpsSet.SELECT_TF_OPS]
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
        converter.allow_custom_ops = True
    else:
        converter.target_spec.supported_ops = [
            tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
            tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
        ]

    tflite_model = converter.convert()

    # Save the model.
    with open('FRC_2022_nofpn.tflite', 'wb') as f:
        f.write(tflite_model)
