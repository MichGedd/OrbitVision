import os
import sys
import tensorflow.compat.v1 as tf
import glob
from lxml import etree
import io
import PIL.Image

from object_detection.utils import dataset_util
from object_detection.utils import label_map_util


def dict_to_tfrecord(img_path, data):
    with tf.gfile.GFile(img_path, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = PIL.Image.open(encoded_jpg_io)

    if image.format != 'JPEG':
        raise ValueError('Image format not JPEG')

    width = int(data['size']['width'])
    height = int(data['size']['height'])

    xmin = []
    ymin = []
    xmax = []
    ymax = []
    classes = []
    classes_text = []

    if 'object' in data:
        for obj in data['object']:
            difficult = bool(int(obj['difficult']))

            xmin.append(float(obj['bndbox']['xmin']) / width)
            ymin.append(float(obj['bndbox']['ymin']) / height)
            xmax.append(float(obj['bndbox']['xmax']) / width)
            ymax.append(float(obj['bndbox']['ymax']) / height)
            classes_text.append(obj['name'].encode('utf8'))
            classes.append(label_map_dict[obj['name']])

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(
            data['filename'].encode('utf8')),
        'image/source_id': dataset_util.bytes_feature(
            data['filename'].encode('utf8')),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))

    return tf_example


if __name__ == '__main__':
    print("Starting Train Record")
    writer = tf.python_io.TFRecordWriter('./annotations/train.record')
    label_map_dict = label_map_util.get_label_map_dict('./annotations/label_map.pbtxt')
    os.chdir("./images/train/")
    for file in glob.glob("*.xml"):
        file_name = file.split('.')[:-1]
        file_name = '.'.join(file_name)

        with tf.gfile.GFile(file, 'r') as fid:
            xml_str = fid.read()

        xml = etree.fromstring(xml_str)
        data = dataset_util.recursive_parse_xml_to_dict(xml)['annotation']

        tf_example = dict_to_tfrecord(os.path.abspath(f'{file_name}.jpg'), data)
        writer.write(tf_example.SerializeToString())
    writer.close()

    os.chdir("../../")

    print("Starting Test Record")
    writer = tf.python_io.TFRecordWriter('./annotations/test.record')
    os.chdir("./images/test/")
    for file in glob.glob("*.xml"):
        file_name = file.split('.')[:-1]
        file_name = '.'.join(file_name)

        with tf.gfile.GFile(file, 'r') as fid:
            xml_str = fid.read()

        xml = etree.fromstring(xml_str)
        data = dataset_util.recursive_parse_xml_to_dict(xml)['annotation']

        tf_example = dict_to_tfrecord(os.path.abspath(f'{file_name}.jpg'), data)
        writer.write(tf_example.SerializeToString())
    writer.close()
