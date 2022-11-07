import tensorflow as tf
import numpy as np
import cv2 as cv

# Set Up Image
# img_orig = cv.imread("Tensorflow/workspace/demo/images/imgs/20201101_210901.jpg")
img_orig = cv.imread("../workspace/FRC_2022/images/imgs/20220911_173939.jpg")
img = cv.cvtColor(img_orig, cv.COLOR_BGR2RGB)
img = cv.resize(img, (320, 320), interpolation=cv.INTER_AREA)

# Need these two lines for non-PTIQ. Comment out for PTIQ.
# img = (2.0 / 255.0) * img - 1.0
# img = np.float32(img)
# cv.imshow("img", img)
#cv.waitKey()

# Set Up TFLite
# interpreter = tf.lite.Interpreter(model_path="Tensorflow/workspace/demo/exported-models/demo_model.tflite")
interpreter = tf.lite.Interpreter(model_path="../workspace/FRC_2022/exported_models/FRC_2022_model_2/FRC_2022_2.tflite")
interpreter.allocate_tensors()
input = interpreter.get_input_details()[0]
output = interpreter.get_output_details()

# input_scale, input_zero_point = input['quantization']
# img = img * input_scale + input_zero_point
# img = np.uint8(img)

interpreter.set_tensor(input['index'], img[tf.newaxis, ...])
interpreter.invoke()

'''
# This is outputs for non-PTIQ model
boxes = interpreter.get_tensor(337)
print("Boxes")
print(boxes)

detection_classes = interpreter.get_tensor(338)
print("Detection Classes")
print(detection_classes)

scores = interpreter.get_tensor(339)
print("Scores")
print(scores)

num_boxes = interpreter.get_tensor(340)
print("Num Boxes")
print(num_boxes)
'''


# This is the outputs for PTIQ model
boxes = interpreter.get_tensor(390)
print("Boxes")
print(boxes)

detection_classes = interpreter.get_tensor(392)
print("Detection Classes")
print(detection_classes)

scores = interpreter.get_tensor(389)
print("Scores")
print(scores)

num_boxes = interpreter.get_tensor(391)
print("Num Boxes")
print(num_boxes)


# Bounding boxes are in the form [y_min, x_min, y_max, x_max]

# p1 = (int(0.17067114 * 640), int(0.35713917 * 640))
# p2 = (int(0.3262799 * 640), int(0.54544556 * 640))

'''
This is the dumbest equation I have ever created
I hate this so much
Steps to reproduce the equation:
    1) Get the bounding box values from the tflite model BEFORE doing post-training integer quantization
    2) Get the bounding box values from the tflite model AFTER doing post-training integer quantization
    3) Do linear regression
'''
# x = lambda a : a * 0.00632279 - 0.297684  # 640x540
# x = lambda a : a * 0.0123466 - 1.33652  # 320x320
# x = lambda a : a * 0.00719855 - 0.334155
x = lambda a : a * 0.00652679 - 0.355669

bb = boxes[0][0]

p1 = (int(x(bb[1]) * 320), int(x(bb[0]) * 320))
p2 = (int(x(bb[3]) * 320), int(x(bb[2]) * 320))

'''
p1 = (int((bb[1]) * 320), int((bb[0]) * 320))
p2 = (int((bb[3]) * 320), int((bb[2]) * 320))
'''
cv.rectangle(img, p1, p2, (0, 255, 0), 3)


cv.imshow("img", img)
cv.waitKey()