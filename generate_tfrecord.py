#Code reference
#Author(s) name:Dat Tran
#Date: 01/03/2018
#Title of program/source code: generate_tfrecord.py
#Code version: -
#Type: computer program
#Web address or publisher: https://github.com/datitran/raccoon_dataset/blob/master/generate_tfrecord.py
#Modified: Yes
#Modified lines: 40-93, 132-133, 122-125, 148, 150


"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=path/datasets/flickr_logos_27_dataset/training_set.csv  --output_path=path/fyp_logo_dec/train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=path/datasets/flickr_logos_27_dataset/test_set.csv  --output_path=pathfyp_logo_dec/test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

def class_text_to_int(row_label):
    if row_label == 'Adidas':
        return 1
    elif row_label == 'Apple':
        return 2
    elif row_label == 'BMW':
        return 3
    elif row_label == 'Citroen':
        return 4
    elif row_label == 'Cocacola':
        return 5
    elif row_label == 'DHL':
        return 6
    elif row_label == 'Fedex':
        return 7
    elif row_label == 'Ferrari':
        return 8
    elif row_label == 'Ford':
        return 9
    elif row_label == 'Google':
        return 10
    elif row_label == 'Heineken':
        return 11
    elif row_label == 'HP':
        return 12
    elif row_label == 'Intel':
        return 13
    elif row_label == 'McDonalds':
        return 14
    elif row_label == 'Mini':
        return 15
    elif row_label == 'Nbc':
        return 16
    elif row_label == 'Nike':
        return 17
    elif row_label == 'Pepsi':
        return 18
    elif row_label == 'Porsche':
        return 19
    elif row_label == 'Puma':
        return 20
    elif row_label == 'RedBull':
        return 21
    elif row_label == 'Sprite':
        return 22
    elif row_label == 'Starbucks':
        return 23
    elif row_label == 'Texaco':
        return 24
    elif row_label == 'Unicef':
        return 25
    elif row_label == 'Vodafone':
        return 26
    elif row_label == 'Yahoo':
        return 27

    else:
        None


def split(df, group):
    data = namedtuple('data', ['im_filename', 'object'])
    gb = df.groupby(group)
    return [data(im_filename, gb.get_group(x)) for im_filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.im_filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    im_filename = group.im_filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['x_min'] / width)
        xmaxs.append(row['x_max'] / width)
        ymins.append(row['y_min'] / height)
        ymaxs.append(row['y_max'] / height)
        classes_text.append(row['classname'].encode('utf8'))
        classes.append(class_text_to_int(row['classname']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/im_filename': dataset_util.bytes_feature(im_filename),
        'image/source_id': dataset_util.bytes_feature(im_filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/classname/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/classname/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(os.getcwd(), 'flickr_logos_27_dataset_images')
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'im_filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()